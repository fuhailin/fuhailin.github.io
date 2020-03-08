#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyspark import SparkContext


if __name__ == "__main__":
    sc = SparkContext( 'local', 'test')
    logFile = "file:///Users/vincent/opt/spark/spark-2.4.5-bin-without-hadoop-scala-2.12/README.md"
    logData = sc.textFile(logFile, 2).cache()
    numAs = logData.filter(lambda line: 'a' in line).count()
    numBs = logData.filter(lambda line: 'b' in line).count()
    print('Lines with a: %s, Lines with b: %s' % (numAs, numBs))