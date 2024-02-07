# 何謂平穩性:
# 資料分布不會隨時間改變,
# 平均數、變異數、白燥音

# 變異數:資料分布的離散程度
# 要使用平方原因:消除負數、放大差異
# 白燥音:不和觀察值有關的雜訊、和時間無關

# ARIMA模型
# 自迴歸項(可以有多個)
# 差分
# 移動平均

# 自迴歸項:調整可透過PACF圖(偏自相關函數圖)

# 要劃分訓練集和測試集
# 預測RMSE(均方根誤差)

import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

# 创建一个时间序列数据
data = pd.Series([1, 2, 3, 4, 5], index=pd.date_range('2020-01-01', periods=5))


# 创建一个 ARIMA 模型
model = ARIMA(data, order=(1, 0, 0))

# 拟合模型
model_fit = model.fit()

# 打印模型的摘要
print(model_fit.summary())
