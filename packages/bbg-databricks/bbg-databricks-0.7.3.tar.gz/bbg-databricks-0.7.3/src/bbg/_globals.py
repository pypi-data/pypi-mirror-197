import pyspark.sql

variables = {"spark": pyspark.sql.SparkSession.getActiveSession()}

get_global = variables.__getitem__
set_globals = variables.update
