from pyspark import SparkConf, SparkContext

# local is a special value that runs spark on one thread on the local machine,
# without connecting to a cluster
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)

nums = sc.parallelize([1, 2, 3, 4])
squared = nums.map(lambda x: x * x).collect()
for num in squared:
    print num