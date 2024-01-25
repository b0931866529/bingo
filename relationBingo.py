# region 關聯
from datetime import datetime
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import db as db


if __name__ == '__main__':
    dataset = []

    # region 從db撈出處理成二維array到dataset
    # 宣告資料庫
    db = db.MongoDbContext("localhost", "LotteryTicket")
    table = "Bingo"
    # queryKey = {'dDate': {'$gte': datetime(2024, 1, 1)}}
    queryKey = {'dDate': datetime(2024, 1, 24)}
    results = db.Find(table, queryKey)
    # result還算是有db型態list,但若遍歷直接就是字典元素
    twoDatas = []
    for obj in results:
        arr = obj['bigShowOrder'].split(',')
        twoDatas.append(arr)
    # endregion

    dataset = twoDatas[50:100]
    # 假設我們有一個購物籃數據集
    # dataset = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
    #            ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
    #            ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
    #            ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
    #            ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]

    print("")

    # 使用 TransactionEncoder 進行 one-hot 編碼
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # 使用 apriori 找出頻繁項集
    frequent_itemsets = apriori(df, min_support=0.15, use_colnames=True)

    # 使用 association_rules 找出關聯規則
    rules = association_rules(
        frequent_itemsets, metric="confidence", min_threshold=0.6)

    # DataFrame刪除不需要輸出在excel欄位
    del rules['antecedent support']
    del rules['consequent support']
    del rules['support']
    del rules['confidence']
    del rules['leverage']
    del rules['conviction']
    del rules['zhangs_metric']
    # DataFrame按照指定爛位做排序
    rules = rules.sort_values(by=['lift'], ascending=False)
    # DataFrame轉成csv檔
    rules.to_csv('rules.csv', index=False, encoding='utf-8-sig')
    # 查看規則
    print(rules)
    # endregion
