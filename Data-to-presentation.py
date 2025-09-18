# Data from Ingest to Presentation-----------

import os
from pyspark.sql.functions import countDistinct, col

storage_account_name = os.environ["MY_STORAGE"]
storage_account_key = os.environ["MY_KEY"]


spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
    storage_account_key
)

ingested_path = f"wasbs://coviddata@{storage_account_name}.blob.core.windows.net/Ingest/covidclean"
presentation_path = f"wasbs://coviddata@{storage_account_name}.blob.core.windows.net/presentation/summary.parquet"

df = spark.read.format("parquet").load(ingested_path)

country_count = df.select(countDistinct(col("Country")).alias("total_countries"))

summary_df = df.agg(
    {"TotalDeaths": "sum", "TotalCases": "avg"}
).withColumnRenamed("sum(TotalDeaths)", "total_deaths") \
 .withColumnRenamed("avg(TotalCases)", "avg_total_cases")

summary_df.write.mode("overwrite").parquet(presentation_path)
print(f'successfully wrote to {presentation_path}')

-------------------------------------------------------------------------------------