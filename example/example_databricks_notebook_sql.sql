-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC 
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img src="./example/yoydyne_data_science_logo.png" alt="Yoydyne Data Science" style="width: 600px">
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 
-- MAGIC 
-- MAGIC Run some code in **SQL**
-- MAGIC 

-- COMMAND ----------

DESCRIBE DETAIL my_table;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC 
-- MAGIC 
-- MAGIC Run same code in `python`
-- MAGIC 

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC table_name = "my_table"
-- MAGIC my_table_location = spark.sql(f"DESCRIBE DETAIL {table_name}").first().location
-- MAGIC print(tbl_locmy_table_locationation)