import matplotlib.pyplot as plt
import random

rand = [random.randint(0,20) for i in range(0,20)]

n, bins, patches = plt.hist(rand, 20)
plt.show()
