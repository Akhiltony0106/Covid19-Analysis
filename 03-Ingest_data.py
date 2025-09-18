# Data from Raw to Ingest---

import os

# Fetch credentials from environment variables
storage_account_name = os.environ["MY_STORAGE"]
storage_account_key = os.environ["MY_KEY"]

# Set Spark config for accessing Azure Blob Storage
spark.conf.set(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", storage_account_key)

raw_path = f"wasbs://coviddata@{storage_account_name}.blob.core.windows.net/raw/covid"
ingested_path = f"wasbs://coviddata@{storage_account_name}.blob.core.windows.net/Ingest/covidclean"

# List of countries to filter
countries = [
    'India', 'USA', 'UK', 'Germany', 'France', 'Brazil',
    'Italy', 'Canada', 'Australia', 'Russia', 'Mexico',
    'Spain', 'Japan', 'South Korea', 'South Africa',
    'China', 'Argentina', 'Netherlands', 'Turkey', 'Saudi Arabia',
    'Indonesia', 'Pakistan', 'Egypt', 'Bangladesh', 'Thailand'  
]

# Read data from raw folder
df = spark.read.format("parquet").load(raw_path)

# Filter for selected countries
df_filtered = df.filter(df['country'].isin(countries))

# Drop duplicates and null values
df_clean = df_filtered.dropDuplicates().na.drop()

# Write cleaned data to ingested folder
df_clean.write.mode("overwrite").parquet(ingested_path)

--------------------------------------------------------------------------------------------------------
