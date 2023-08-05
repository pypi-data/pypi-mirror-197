# Lib310-Lite

This Library are the light weight version for some usage.

## Usage
1. Install the library
    ```commandline
    pip install lib310-lite
    ```

2. Import the library
    ```python
    from lib310_lite import BigQueryClient, MLDL, set_gcloud_key_path
    ```

3. If there is no gcloud key file not set in your environment, you can set the path of the key file
    ```python
    set_gcloud_key_path("<path/to/key/file>")
    ```

### BigQueryClient

You can fetch data from BigQuery with fetch method.
```python
bq = BigQueryClient()
bq.fetch("SELECT * FROM `project.dataset.table` LIMIT 10")
```
#### fetch parameters
```
query: str,
job_config=None,
job_id: str = None,
job_id_prefix: str = None,
location: str = None,
project: str = None,
retry=r.DEFAULT_RETRY,
timeout=r.DEFAULT_TIMEOUT,
job_retry=r.DEFAULT_JOB_RETRY,
api_method=enums.QueryApiMethod.QUERY
```

you can Also use the BigQueryClient and cache the result in GCS.
```python
bq = BigQueryClient()
bq.cache_query("SELECT * FROM `project.dataset.table` LIMIT 10", "prefix_name_of_cache_file")
```
#### cache_query parameters
```
query: str,
name: str = None,
destination_format: str or FileFormat = FileFormat.CSV,
days: int = 7,
ignore_hit: bool = False
```

### MLDL
In these module you can get samples from language model. which serves in MongoDB.
```python
mldl = MLDL(<MONGO_URL>)
df = mldl.get_batch(100, 500, 20, 'TRAIN')
```
#### get_batch parameters
```
num: int,
max_length: int,
min_num_feature: int = 0,
stage: str = TRAIN
```

