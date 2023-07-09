# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json

# driver = webdriver.Chrome("./chromedriver")
driver = webdriver.Chrome("C:/Programs_Test/pyDB_030115/chromedriver.exe")
def print_dict( par_dict):
    print(json.dumps(par_dict, indent=4))

# 存放抓取號碼
bingo_no = { }

def bingo():
    global bingo_no

    # 開啟頁面
    driver.get("https://www.taiwanlottery.com.tw/lotto/bingobingo/drawing.aspx")

    # 取得頁面 title
    title = driver.title
    print( "title:", title)
    driver.implicitly_wait(3)
    time.sleep( 3)

    # 按鈕【顯示當日所有期數】
    submit_button = driver.find_element(by=By.ID, value="Button1")
    submit_button.click( )
    # time.sleep( 3)

    len_title = len( "112001219")
    len_no = len( "01 03 07 10 11 17 18 20 23 31 35 42 45 50 52 55 57 70 76 79")

    t_title = ""
    for e in driver.find_elements(by=By.CLASS_NAME, value="tdA_3"):
        t = e.text
        if len(t) == len_title:
            t_title = t
        if len(t) == len_no:
            if t_title != "":
                bingo_no[t_title] = t.replace( " ", ",")

    for e in driver.find_elements(by=By.CLASS_NAME, value="tdA_4"):
        t = e.text
        if len(t) == len_title:
            t_title = t
        if len(t) == len_no:
            if t_title != "":
                bingo_no[ t_title] = t.replace( " ", ",")

    bingo_no = dict(sorted(bingo_no.items()))

    time.sleep(3)
    driver.quit()

if __name__ == '__main__':
    bingo()
    print_dict( bingo_no)
