# Spark parquet demo 

## 启动 

```shell
docker compose up -d
```

## 访问 notebook

打开 localhost:8888

关键代码
```python
dfall = spark.read.parquet("/home/iceberg/warehouse/bsc/traces")
dfall.count()
```