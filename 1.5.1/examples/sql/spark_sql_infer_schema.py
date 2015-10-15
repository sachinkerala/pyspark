from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, Row

conf = SparkConf().setAppName("spark_sql_infer_schema")

sc = SparkContext(conf=conf)

hc = HiveContext(sc)

lines = sc.parallelize(["a,1", "b,2", "3,c"])

people = lines.map(lambda line: line.split(",")).map(
    lambda words: Row(name=words[0], age=words[1]))

schemaPeople = hc.createDataFrame(people)

schemaPeople.registerTempTable("people")

rows = hc.sql("select * from people where name = 'a'").collect()

sc.stop()

for row in rows:
    print row.name, row.age