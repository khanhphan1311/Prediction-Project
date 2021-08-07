from datetime import date
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from stockMarketReader import readDataSet
from bestStock import bestStockStrategy
from ubah import ubah
from CRP import UCRP

data = readDataSet()
# bestStock = np.log(bestStockStrategy(data))
# ubahPort = np.log(ubah(data))
# crpPort = np.log(UCRP(data))

# bestStock = bestStockStrategy(data)
ubahPort = ubah(data)
crpPort = UCRP(data)

plt.title("Comparison of Strategies")
plt.xlabel("Number of Days")
plt.ylabel("Total Return")
# plt.plot(bestStock, label="Best Stock")
plt.plot(ubahPort, label="UBAH")
plt.plot(crpPort, label="CRP")
plt.legend()
plt.show()