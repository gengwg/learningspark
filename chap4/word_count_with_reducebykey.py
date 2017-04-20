from pyspark import SparkConf, SparkContext

# local is a special value
# that runs spark on one thread on the local machine,
# without connecting to a cluster
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)

"""
flatMap() "flattens" the iterator returned to it,
so that instead of ending up with an rdd of lists
we have an rdd of the elements in those lists.

called individually for each element in input rdd.
return an iterator with our return values.
rather than producing an rdd of iterators,
we get back an rdd that consists of elements from all
the iterators
"""
lines = sc.textFile("README.md")
words = lines.flatMap(lambda line: line.split(" "))
result = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
print result.collect()

# another way to implement wc
# using countByValue() on first rdd
# result = words.countByValue()
# print result
