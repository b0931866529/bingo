from db.db import MSSQLDbContext
from algorithm.numMark import NumMark
if __name__ == '__main__':

    # region select top 30
    dbContext = MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})
    rows = dbContext.select(
        'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
    inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))
    # endregion

    # NumMark method ok
    # NumMark test method ok
    numMark = NumMark()
    numMark.loadStds(39, 1)

    # DeferCalcu ref NumMark method
    # DeferCalcu ref Quantile method
    # DeferCalcu output 普通、冷、熱
    # DeferCalcu test method

    # --convert to times
    # --分類普通、冷、熱
    # --研究 unit test
    # --quantitle 封裝能算出普通、冷、熱
    # --outlier cold、hot、中位數
    # --用生成式AI提問
    print("")
    pass
