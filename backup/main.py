from bingoModel import BingoInfo
from prize import Prize
from db import MSSQLDbContext


if __name__ == '__main__':
    # 撈取要計算的期數
    curSQL = "select drawTerm,bigShowOrder from Bingo WHERE dDate = \'2024-06-28\' ORDER BY drawTerm DESC"
    dbContext = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    rows = dbContext.select(curSQL)
    print(rows)
    prize = Prize(dbContext)
    signs = ['13', '23', '79']
    # loop計算是否命中
    results = []
    for row in rows:
        curBingo = row['bigShowOrder'].split(',')
        arr = curBingo + signs
        isMatch = (len(set(arr)) == 20)
        if isMatch:
            results.append(row['drawTerm'])
    overs = []
    for index, item in enumerate(results):
        if index == 0:
            overs.append({'drawTerm': item, 'over': item})
        else:
            overs.append({'drawTerm': item, 'over': item - results[index-1]})
    print('')
    pass
