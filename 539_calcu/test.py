import pandas as pd

# 假設有兩個數據集
data = {
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 6, 8, 10]
}

# 創建 DataFrame
df = pd.DataFrame(data)

# 計算相關係數
correlation_coefficient = df['x'].corr(df['y'])

print("Correlation Coefficient using pandas:", correlation_coefficient)

# 四分位距算出離散值
# 離散值多久出一次

Q1 = df['x'].quantile(0.25)
Q3 = df['x'].quantile(0.75)
IQR = Q3 - Q1

# 設定離散值範圍
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print("lower_bound:", lower_bound)
print("upper_bound:", upper_bound)
