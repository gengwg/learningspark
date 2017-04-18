## Introduction

batch applications, iterative algorithms, interactive queries, streaming.

spark core is home to the api that defines resilient distributed datasets (rdds, which are spark main programming abstraction.

cluster managers:
hadoop yarn, apache mesos, standalone scheduler.

general-purpose framework for cluster computing

ds:
  * analyze and model data
  * answering a question or discovering insights.

after the initial exploration phase, the work of a data scientist will be 'productized', or extended, hardened (i.e., made fault-tolerant), and tuned to become a production data processing application, which itself is a component of a business application.

for example, initial investigation of a ds might lead to the creation of a production recommender system that is integrated into a web application and used to generate product suggestions to users.

often it is different person or team that leads the process of productizing the work of ds, and that person is often an engineer.

## getting started

spark is written in scala, and runs on the JVM.
to run spark, all you need is an installation of java.
spark does not yet work with py3.

### Load a text file

Python
```python
[vagrant@localhost spark-1.6.0-bin-hadoop2.6]$ bin/pyspark
>>> lines = sc.textFile("README.md")
>>> lines.count()
95
>>> lines.first()
u'# Apache Spark'
```

Scala
```scala
[vagrant@localhost spark-1.6.0-bin-hadoop2.6]$ bin/spark-shell
scala> val lines = sc.textFile("README.md")
lines: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[1] at textFile at <console>:27

scala> lines.count()
res0: Long = 95

scala> lines.first()
res1: String = # Apache Spark
```

every spark app consists of a driver program that launches various parallel operations on a cluster. the spark shell is a driver program.

driver programs access spark through a `SparkContext` object, which represents a connection to a computing cluster. in the shell, a SparkContext is automatically created as the variable `sc`.

to run these operations, driver program typically manage a number of nodes called executors.

Filter operations:
```python
>>> lines = sc.textFile("README.md")
>>> pythonLines = lines.filter(lambda line: "Python" in line)
>>> pythonLines.first()
u'high-level APIs in Scala, Java, Python, and R, and an optimized engine that'
```

spark automatically takes your function and ships it to the executor nodes. htus you can write code in a single driver program and automatically have parts of it run on multiple nodes.

Submit a job:
```bash
[vagrant@localhost spark-1.6.0-bin-hadoop2.6]$ bin/spark-submit \
--class com.oreilly.learningsparkexamples.mini.scala.WordCount ~/learning-spark-examples/mini-complete-example/target/scala-2.10/learning-spark-mini-example_2.10-0.0.1.jar \
./README.md \
./wordcounts
```

## Chapter 3 programming with RDDs


in spark all work is expressed as either creating new RDDs, transforming existing RDDs, or calling operations on RDDs to compute a result.

An RDD is an immutable distributed collection of elements. each RDD is split into multiple `partitions`, which may be computed on different nodes of the cluster. RDDs can contain any type of Python, Java, or Scala objects, including user-defined classes.

users create RDDs in two ways: by loading an external dataset, or by distributing a collection of objects (e.g. list or set) in their driver program.

RDDs offer 2 types of operations: transformation and actions.
transformation construct a new RDD from a previous one.
actions compute a result based on an RDD, and either return it to the driver program or save it to an external storage system (e.g. HDFS).

transformations are operations on rdds that return a new RDD, such as `map()` and `filter()`.
actions are operations that return a result ot the driver program or write it to storage, and kick off a computation, such as `count()` and `first()`.

transformations return rdds, whereas actions return other data type.

by default, entire spark RDDs are recomputed each time you run an action on them. If you would like to reuse an RDD in multiple actions, you can persist it using `RDD.persist()`. after computing it for the first time, spark will store the rdd contents in memory, partitioned across the machines in the cluster, and reuse them in future actions.

in practice you often use `persist()` to load a subset of your data into memory and query it repeatedly:
```python
>>> lines = sc.textFile("README.md")
>>> pythonLines = lines.filter(lambda line: "Python" in line)
>>> pythonLines.persist
<bound method PipelinedRDD.persist of PythonRDD[2] at RDD at PythonRDD.scala:43>
>>> pythonLines.count()
3
>>> pythonLines.first()
u'high-level APIs in Scala, Java, Python, and R, and an optimized engine that'
>>> pythonLines.collect()
[u'high-level APIs in Scala, Java, Python, and R, and an optimized engine that', u'## Interactive Python Shell', u'Alternatively, if you prefer Python, you can use the Python shell:']
```

every spark program and shell session work as follows:
1. create some input RDDs from external data
2. tranform them to define new rdds using transformations like `filter()`
3. ask spark to `persist()` any intermediate RDDs that will need to be reused
4. launch actions such as `count()` and `first()` to kick off a parallel computation, which is optimized and executed by spark

prototyping and testing using SparkContext `paralelize()` method:
```python
>>> l = sc.parallelize(["pandas", "bears"])
>>> l
ParallelCollectionRDD[5] at parallelize at PythonRDD.scala:423```

as you derive new rdds from each other using transformations, spark keeps track of the set of dependencies between diff rdds, `lineage graph`. it uses this information to compute each rdd on demand and to recover lost data if part of a persistent rdd is lost.

ability to always recompute an rdd is why rdd are called 'resilient'. when a machine holding rdd data fails, spark uses this ability to recompute the missing partitions, transparent to user.

### lazy evaluation

when we call a transformation on rdd, the operation is not immediately performed. instead spark internally records metadata to indicate that this operation has been requested. rather than thinking of an rdd as containing specific data, it is best to think of each rdd as consisting of instructions on how to compute the data that we build up through transformations.

loading data into rdd is lazily evaluated in the same way transformation. when we call `sc.textFile()`, data is not loaded until necessary.

in hadoop mapreduce, developers have to spend a lot of time considering how to group together operations to minimize the number of mapreduce passes. in spark, there is no substantial benefit to writing a single complex map instead of chaning together many simple operations. smaller, more managerable operationsself.
