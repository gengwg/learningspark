from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App")
# local is a special value that runs spark on one thread on the local machine, without connecting to a cluster


sc = SparkContext(conf = conf)

