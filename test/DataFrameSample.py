import matplotlib.pyplot as plt
from tokenize import group
import pandas as pd
import numpy as np
import random
dates = pd.date_range('20210101', periods=60)
data = np.random.randint(0, 10, size=(60, 1))
# 生成亂數時間序列天數
df = pd.DataFrame(data, index=dates, columns=['value'])
df['Month'] = df.index.month
print(df)
grouped = df.groupby('Month')['value'].mean()
# 將其Group成月份
print(grouped)

plt.figure(figsize=(10, 6))
plt.plot(df)
plt.title('Monthly Airline Passengers')
plt.show()
