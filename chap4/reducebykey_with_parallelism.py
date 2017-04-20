from pyspark import SparkConf, SparkContext

# local is a special value
# that runs spark on one thread on the local machine,
# without connecting to a cluster
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)

data = [("a", 3), ("b", 4), ("a", 2)]
wc = sc.parallelize(data).reduceByKey(lambda x, y: x + y)
# reduceByKey() with custom parallelism
wc = sc.parallelize(data).reduceByKey(lambda x, y: x + y, 10)
print wc.collect()  # [('a', 5), ('b', 4)]
