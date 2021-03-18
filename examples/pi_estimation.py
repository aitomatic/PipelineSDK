from pyspark import SparkContext

import sys
import random

sc = SparkContext(appName="PiEstimation")

num_samples = int(sys.argv[1])


def inside():
    x, y = random.random(), random.random()
    return x * x + y * y < 1


count = sc.parallelize(range(0, num_samples)) \
    .filter(inside).count()
print("Pi is roughly %f" % (4.0 * count / num_samples))
