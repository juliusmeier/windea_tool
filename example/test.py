import matplotlib.pyplot as plt
import numpy as np

bins = np.arange(14)
centers = bins[:-1] + np.diff(bins) / 2
y = np.sin(centers / 2)



plt.stairs(y - 1, bins, baseline=None, label='stairs()')
plt.plot(centers, y - 1, 'o--', color='grey', alpha=0.3)


plt.legend()
plt.title('step() vs. stairs()')
plt.show()