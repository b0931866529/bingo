# -*- coding:utf-8 -*-
import pandas as pd
from db import MongoDbContext
import random, logging, traceback
import json

# pandas 的相關設定
pd.set_option('display.max_columns', None)               # 顯示寬度
pd.set_option('display.width', 600)                      # 設置列印寬度
pd.set_option( "display.float_format", "{:.3f}".format)  # 浮點數格式

# 是否新增隨機數據
# 需求文件只有二次抽獎，不適合作為分析樣本
# new_data = False
new_data = True

# ball_qty = 5    # 抽出球的數量
# ball_max = 36     # 抽出球的號碼最大值

ball_qty = 20    # 抽出球的數量
ball_max = 80     # 抽出球的號碼最大值

ball_times = 10     # 抽獎次數

lift_top = 30       # 取增益值最大值的筆數
lift_min = 2      # 過濾增益值

is_print = True

# 準備日誌
LogFile = "ball_no.log"
logging.basicConfig(
    filename=LogFile,
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y/%m/%d %I:%M:%S',
)

# 輸出專用函數，用於除了log之外是否也在console輸出
def print_or_log( par_str):
    if is_print:
        print(par_str)
    logging.info( par_str)

# 清除日誌內容
with open(LogFile, 'w'):
    pass

# 取得亂數列表
# par_qty: 數量
def get_random_list(par_qty):
    s_list = []
    for n in range(par_qty):
        rn = random.randint(1, ball_max)
        # 避免重複
        while rn in s_list:
            rn = random.randint(1, ball_max)
        s_list.append(rn)
    s_list.sort()
    return s_list

# 取得亂數列表(字串)
# par_qty: 數量
def get_random_list_str(par_qty):
    par_list = get_random_list(par_qty)
    str_n = ""
    for n in par_list:
        n_str = str(n).zfill(2)
        str_n += n_str if str_n == "" else ("," + n_str)
    return str_n

class Ball_no:
    trans_source = {}   # 資料來源
    trans = None        # 計算中的資料
    trans_result = None  # 計算結果

    # 初始化
    def __init__(self):
        list_index = [ ]
        for r in range(1, ball_max + 1):
            list_index.append( r)
        self.trans = pd.DataFrame(columns=list_index)
        self.trans_result = pd.DataFrame()

    # 插入球號list
    # par_index: 抽獎期數
    # par_list: 球號 list
    def insert_no(self, par_index, par_list):
        i_row = { }
        for c_name in range(1, ball_max + 1):
            i_row[c_name] = 1 if c_name in par_list else 0
        df = pd.DataFrame( i_row, index=[par_index])
        self.trans = self.trans.append( df)

    # 列印 trans, 順便加總統計一下，可確認資料是否正確
    def print_trans(self):
        d = self.trans.sum(axis=1)
        self.trans["sum"] = d
        print_or_log("2.轉換後的數據...")
        print_or_log( self.trans)

        print_or_log("號碼出現頻率分析...")
        trans_sum = self.trans.sum()
        print_or_log( trans_sum.sort_values().head(lift_top))

    # 從資料庫讀入球號，並插入 trans
    def read_from_db(self,find_result):
        # 宣告資料庫
        #db_ball = MongoDbContext("localhost", "ball_no")

        #find_result = db_ball.Find( "bn", {})
        print_or_log("1.資料庫讀出的原始數據...")
        for row in find_result:
            row_id = row[ "_id"]
            row_list = row["no"].split(",")
            row_list = list(map(int, row_list))  # 轉換成整數List
            print_or_log( str(row_id) + ": " + str(row_list))
            self.trans_source[ row_id] = row_list
            self.insert_no( row_id, row_list)

    # 計算某2期配對的所有球號
    def compute_all(self):
        list_all = []
        for a in range( 1, 81, 1):
            for b in range( a+1, 81, 1):
                list_all.append( ( a, b))

        print_or_log( "即將計算的球號配對：%d %s" % (len( list_all), str(list_all)))

        for row_ab in list_all:
            print_or_log( "==== 計算 %s ====" % str(row_ab))
            self.compute( row_ab)

    # 計算某個配對球號 ( a, b)
    def compute(self, par_ab):
        p_a = par_ab[0]
        p_b = par_ab[1]

        # print("\n==== 1. 計算支持度(support) ====")

        trans_all = set(self.trans.index)
        print_or_log("\t抽獎次數(trans_all)：%d" % len(trans_all))

        trans_a = set(self.trans[self.trans[p_a] == 1].index)
        print_or_log("\t球號 %d 的出現次數(trans_a)： %d"
                     % ( p_a, len(trans_a)))

        trans_b = set(self.trans[self.trans[p_b] == 1].index)
        print_or_log("\t球號 %d 的出現次數(trans_b)： %d"
                     % ( p_b, len(trans_b)))

        trans_ab = trans_a & trans_b
        print_or_log( "\t球號 %d 與球號 %d 同時出現的次數(trans_ab)： %d"
                      % ( p_a, p_b, len(trans_ab)))

        support_a = len(trans_a) / len(trans_all)
        support_b = len(trans_b) / len(trans_all)
        support_ab = len(trans_ab) / len(trans_all)
        print_or_log("1.支持度(support_ab=trans_ab/trans_all)：%.3f" % support_ab)
        print_or_log("\t支持度(support_a)：%.3f" % support_a)
        print_or_log("\t支持度(support_b)：%.3f" % support_b)

        # print("\n==== 2. 計算信賴度 ====")

        confidence_ab = len(trans_ab) / len(trans_a)
        print_or_log("2.球號 %d -> %d 信賴度(confidence_ab=trans_ab/trans_a): %.3f"
                     % ( p_a, p_b, confidence_ab))

        # print("\n==== 3. 計算增益值 ====")

        lift_ab = confidence_ab / support_b
        print_or_log("3.球號 %d -> %d 增益值(lift_ab=confidence_ab/support_b): %.3f"
              % ( p_a, p_b, lift_ab))
        # order
        i_row = {
            "support_ab": support_ab,
            "confidence_ab": confidence_ab,
            "lift_ab": lift_ab,
            "frtBall": par_ab[0],
            "afrtBall": par_ab[1],
        }
        df = pd.DataFrame( i_row, index=[par_ab])
        self.trans_result = self.trans_result.append(df)

if __name__ == '__main__':
    print_or_log("ball_no 開始...")

    # 宣告資料庫
    db = MongoDbContext("localhost", "ball_no")
    # 清空數據/產生新數據
    if new_data:

        db.DeleteCollection( "bn")

        insert_list = []
        print_or_log( "0.新增的原始數據...")

        # 從網站抓取當天的開獎資料
        import bingo
        bingo.bingo()
        bingo.print_dict( bingo.bingo_no)
        for i in bingo.bingo_no:
            insert_list.append( {
                    "_id": i,
                    "no": bingo.bingo_no[ i]
                })

        # 插入指定的資料
        # insert_list.append({ "_id": 1, "no": "06,08,19,20,28"})
        # insert_list.append({ "_id": 2, "no": "20,28,29,35,36"})

        # 插入隨機的資料
        # for i in range( 1, ball_times+1, 1):
        #     no_str = get_random_list_str(ball_qty)
        #     print_or_log( str(i) + no_str)
        #     insert_list.append( {
        #         "_id": i,
        #         "no": no_str
        #     })

        db.Insert("bn", insert_list)

    # 讀出數據
    bn = Ball_no()
    bn.read_from_db(insert_list)

    bn.print_trans( )

    # print("\n3.計算過程...")
    print_or_log("3.計算過程...")
    bn.compute_all( )

    # df_lift_sort = bn.trans_result.sort_values(by=['lift_ab'], ascending=False)
    df_lift_sort = bn.trans_result.sort_values(by=['frtBall'], ascending=False)

    # print_or_log( "\n增益值排行前%d名..." % lift_top)
    print_or_log( df_lift_sort)
    #print_or_log( df_lift_sort.head( lift_top))

    # df_lift_filter = df_lift_sort[df_lift_sort['lift_ab'] > lift_min]
    # df_lift_filter = df_lift_sort.sort_values(by=['frtBall'], ascending=False)
    # print_or_log( "增益值大於 %.3f..." % lift_min)
    # print_or_log( df_lift_filter)

    print_or_log( "ball_no 結束")
