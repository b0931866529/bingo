# region 關聯
from datetime import datetime
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import bingo_scrapy.bingo_scrapy.db as db
from pymongo import MongoClient, ASCENDING, DESCENDING
import re
# 10 * 0.2 * 0.5 = 1
# support:0.2
# confidence:0.5
# 只抓取前36期order
# 要是接近現在時間
# 獲得前3組規則(要移除重複)
# 進行組合成12組號碼


if __name__ == '__main__':
    dataset = []

    # region 從db撈出處理成二維array到dataset
    # 宣告資料庫
    db = db.MongoDbContext("localhost", "LotteryTicket")
    table = "Bingo"
    collection = db.getCollection(table)
    queryKey = {'dDate': {'$gte': datetime(2024, 2, 10)}}
    # queryKey = {'dDate': datetime(2024, 2, 8)}
    sortKey = {'drawTerm': -1}
    results = collection.find(
        queryKey, sort=[("drawTerm", DESCENDING)]).limit(50)

    # results = db.Find(table, queryKey)
    # result還算是有db型態list,但若遍歷直接就是字典元素
    twoDatas = []
    beginObjs = []
    for obj in results:
        twoDatas.append(obj['bigShowOrder'])
        beginObjs.append(obj)
    # endregion

    # 36為1個單位去組合
    dataset = twoDatas
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
    frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)

    # 使用 association_rules 找出關聯規則
    rules = association_rules(
        frequent_itemsets, metric="confidence", min_threshold=0.5)

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
    print(len(rules))
    # endregion
    # 若碰到,另外放入一個集合
    threes = []
    productThree = []
    fours = []
    # region 遍歷DataFrame直到找到3列2陣列且不重複

    # 矩陣方法先將其map成list
    # 先將3個column map成list
    # 3個list同時遍歷
    # threes附加元素判別元素是否重複,長度3停下
    # productThree 有逗點則停下

    antecedents = list(rules['antecedents'].map(lambda e: str(e)))
    consequents = list(rules['consequents'].map(lambda e: str(e)))
    lift = list(rules['lift'].map(lambda e: str(e)))
    for a, c, l in zip(antecedents, consequents, lift):
        ants = re.findall(r'\d+', a)
        cons = re.findall(r'\d+', c)
        arr = ants + cons
        if a.find(",") == -1 and c.find(",") == -1:
            qtys = list(map(lambda e: len(set(e + arr)), threes))
            zeros = list(filter(lambda e: e == 2, qtys))
            # 從array判別重複
            if len(threes) < 3 and len(zeros) == 0:
                threes.append(arr)
            if len(zeros) == 0:
                fours.append(arr)
        else:
            qtys = list(map(lambda e: len(set(e + arr)), productThree))
            zeros = list(filter(lambda e: e == 3, qtys))
            if len(zeros) == 0:
                productThree.append(arr)
    fours = fours[:5]
    # endregion

    print("三星組合:")
    print(threes)
    print("關聯三星組合:")
    print(productThree)
    # print(fours)
    signFours = []
    i = 0
    alls = []
    for e in fours:
        j = 0
        for a in fours:
            if i != j:
                alls.append(e + a)
            j += 1

        i += 1
    # print(alls)
    for all in alls:
        if len(signFours) == 0:
            signFours.append(all)
        else:
            qtys = list(map(lambda e: len(set(e + all)), signFours))
            repeats = list(filter(lambda e: e == 4, qtys))
            if len(repeats) == 0:
                signFours.append(all)
    print("四星組合:")
    print(signFours)
# 必要3星12組
# 決策productThree若有3星4倍搭配4星6組
