# data into Raw folder---------------------

import requests
import pandas as pd
import os

# Step 1: Call the API
url = "https://disease.sh/v3/covid-19/countries"
response = requests.get(url)
data = response.json()

#  Step 2: Convert all data (no filtering)
df = spark.createDataFrame(pd.DataFrame(data))

# Step 3: Rename columns (optional)
df = df.withColumnRenamed('country', 'Country') \
       .withColumnRenamed('cases', 'TotalCases') \
       .withColumnRenamed('todayCases', 'TodayCases') \
       .withColumnRenamed('deaths', 'TotalDeaths') \
       .withColumnRenamed('todayDeaths', 'TodayDeaths') \
       .withColumnRenamed('recovered', 'Recovered') \
       .withColumnRenamed('active', 'Active') \
       .withColumnRenamed('critical', 'Critical') \
       .withColumnRenamed('tests', 'TotalTests') \
       .withColumnRenamed('population', 'Population') \
       .withColumnRenamed('continent', 'Continent')

# Step 4: Set up Azure storage access
storagename = os.environ['MY_STORAGE']
my_key = os.environ['MY_KEY']
spark.conf.set(
    f"fs.azure.account.key.{storagename}.blob.core.windows.net",
    my_key
)

# Step 5: Save as Parquet in Azure Blob
df.write.mode("overwrite").parquet(
    f"wasbs://{'coviddata'}@{storagename}.blob.core.windows.net/raw/covid"
)

print(" Data for ALL countries saved successfully.")

-----------------------------------------------------
