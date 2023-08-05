import numpy as np
from pymongo import MongoClient, ASCENDING
import random
import time
import pandas as pd
from threading import Thread, Event
from queue import Queue
import concurrent.futures
from bounded_pool_executor import BoundedThreadPoolExecutor
import dask.dataframe as dd
from ..bigquery.client import Client as BigQueryClient
from ..bigquery.constants import FileFormat


TRAIN = 'TRAIN'
TEST = 'TEST'
MAIN = 'MAIN'
INTERACTION = 'INTERACTION'


class MLDL:
    def __init__(self, mongo_url: str, cache_size: int = 50, num_threads: int = 10):
        random.seed(time.time())
        self.client = MongoClient(mongo_url)
        self.bq_client = BigQueryClient()
        self.db = self.client['A310']
        self.collections = {
            TRAIN: {
                MAIN: self.db['seq_lang5_train'],
                INTERACTION: self.db['interactions_lang5_train'],
            },
            TEST: {
                MAIN: self.db['seq_lang5_test'],
                INTERACTION: self.db['interactions_lang5_test'],
            }
        }

        self.cache = {TRAIN: {}, TEST: {}}
        self.sample_cache = []
        self.max_queue_size = cache_size
        self.num_threads = num_threads
        self.queue_key = None
        self.pool_key = None
        self.queue = Queue(self.max_queue_size)
        self.filler_thread = None
        self.kill_event = Event()
        self.retry = 0


        # Cache the data with regard to length of sequence
        tmp = self.db['length_freq_lang5_train'].find().sort('len', ASCENDING)
        for item in tmp:
            self.cache[TRAIN][item['len']] = {'freq': item['freq'], 'maxi': item['maxi'], 'mini': item['mini']}
        tmp = self.db['length_freq_lang5_test'].find().sort('len', ASCENDING)
        for item in tmp:
            self.cache[TEST][item['len']] = {'freq': item['freq'], 'maxi': item['maxi'], 'mini': item['mini']}

    def get_batch(self, num: int, max_length: int, min_num_feature: int = 0, stage: str = TRAIN):
        """
        Get a batch of data from the database with regard to the length of the sequence and the number of features
        It also start the background thread to fill the caches and queue
        :param num: number of samples
        :param max_length: maximum length of the sequence
        :param min_num_feature: minimum number of features
        :param stage: TRAIN or TEST
        :return: a pandas dataframe
        """
        stage = stage.upper()
        if stage == TRAIN:
            col = self.collections[TRAIN]
        elif stage == TEST:
            col = self.collections[TEST]
        else:
            raise ValueError('Stage must be either TRAIN or TEST')

        if max_length not in self.cache[stage.upper()].keys():
            arr = [i for i in self.cache[stage.upper()].keys() if i <= max_length]
            if len(arr) == 0:
                return pd.DataFrame()
            max_length = max(arr)

        hit = self.queue_key == f'{num}_{max_length}_{min_num_feature}_{stage}'
        if hit:
            # HIT
            return pd.DataFrame(self.queue.get())

        # MISS
        maxi = self.cache[stage.upper()][max_length]['maxi']
        if min_num_feature > 11:
            table = '1_uniprot.mongo_lang5_train'
            if stage == TEST:
                table = '1_uniprot.mongo_lang5_test'
            if len(self.sample_cache) == 0 or not self.pool_key or self.pool_key != f'{max_length}_{min_num_feature}_{stage}':
                self.pool_key = f'{max_length}_{min_num_feature}_{stage}'
                res = self.bq_client.cache_query(
                    query=f"SELECT row_id FROM `{table}` WHERE len <= {max_length} and token_size >= {min_num_feature}",
                    name=f'{max_length}_{min_num_feature}_{stage}',
                    destination_format=FileFormat.CSV,
                )
                ddf = dd.read_csv(res['uri'])
                df = ddf.compute()
                self.sample_cache = df['row_id'].tolist()
        else:
            self.sample_cache = range(1, maxi)

        if self.filler_thread is not None:
            self.kill_event.set()
            self.queue.get()
            self.filler_thread.join()
            self.kill_event.clear()
            self.queue = Queue(self.max_queue_size)

        self.queue_key = f'{num}_{max_length}_{min_num_feature}_{stage}'

        self.filler_thread = Thread(target=self.filler, args=(num, col))
        self.filler_thread.start()
        time.sleep(3)
        return self.fetch_sample(num, col)

    def filler(self, num: int, col):
        """
        This function is used to fill the queue with data then get batch read data from the queue
        :param num: number of samples
        :param col: collections of the data
        """
        with BoundedThreadPoolExecutor(max_workers=self.num_threads) as executor:
            while not self.kill_event.is_set():
                # print(f'filler thread started {self.kill_event.is_set()}')
                executor.submit(self.filler_worker, num, col)
            # print(f'filler thread ended {self.kill_event.is_set()}')
            while not self.queue.empty():
                self.queue.get()
            # print('queue emptied')
            executor.shutdown(wait=True)
            # print('executor shutdown')

    def filler_worker(self, num: int, col):
        df = self.fetch_sample(num, col)
        self.queue.put(df)
        return

    def fetch_sample(self, num: int, collections):
        """
        This function is used to fetch the data from the database
        Run two threads to fetch the data from the database
        :param num: number of samples
        :param collections: collections of the data
        :return: dataframe of the data
        """
        try:
            index_list = random.sample(self.sample_cache, min(num, len(self.sample_cache)))
            with concurrent.futures.ThreadPoolExecutor() as executor:
                main_thread = executor.submit(self.fetch_sample_main, index_list, collections[MAIN])
                interaction_thread = executor.submit(self.fetch_sample_interaction, index_list, collections[INTERACTION])

                main_df = main_thread.result()
                interaction_df = interaction_thread.result()

                if len(interaction_df) == 0:
                    main_df['interactions'] = np.nan
                    self.retry = 0
                    return main_df
                df = pd.merge(main_df, interaction_df, on='row_id', how='left')
                self.retry = 0
                return df
        except Exception as e:
            print(e)
            if self.retry == 0:
                time.sleep(1)
            else:
                time.sleep(self.retry * 10)
            self.retry += 1
            print(f'Cannot fetch data from database, retry number {self.retry} times')
            if self.retry > 7:
                raise Exception('Cannot fetch data from database')
            return self.fetch_sample(num, collections)

    def fetch_sample_main(self, index_list: list, col):
        """
        This function is used to fetch the main data from the database
        :param index_list: list of row_ids
        :param col: main collection
        :return: dataframe of main data
        """
        cursor = col.find({'row_id': {'$in': index_list}}, {'_id': 0, 'row_id': 1, 'sequence': 1, 'token_ids': 1})
        return pd.DataFrame(list(cursor))

    def fetch_sample_interaction(self, index_list: list, col):
        """
        This function is used to fetch the interaction data from the database
        :param index_list: list of row_ids
        :param col: interaction collection
        :return: dataframe of interaction data
        """
        cursor = col.find({'row_id': {'$in': index_list}}, {'_id': 0, 'row_id': 1, 'interactions': 1})
        return pd.DataFrame(list(cursor))

    def terminate(self):
        """
        Terminate the filler threads and clear the queue
        """
        # Terminate the filler thread
        if self.filler_thread is not None:
            self.kill_event.set()
            self.queue.get()
            self.filler_thread.join()
            self.kill_event.clear()
            self.queue = Queue(self.max_queue_size)
