import db
import pandas as pd
from calcu import RelationTerm, ExportFile


if __name__ == '__main__':
    dbContext = db.MSSQLDbContext({'server': 'wpdb2.hihosting.hinet.net', 'user': 'p89880749_p89880749',
                                   'password': 'Jonny1070607!@#$%', 'database': 'p89880749_test'})

    rows = dbContext.select(
        'select drawNumberSize,lotteryDate from Daily539 ORDER BY period')
    inputs = list(map(lambda row: row['drawNumberSize'].split(','), rows))

    relationTerm = RelationTerm(inputs)
    relationTerm.frt = 0
    relationTerm.end = len(inputs)
    relationTerm.min_support = 0.01
    relationTerm.min_threshold = 0.1

    results = relationTerm.calcu()
    dfProfit = pd.DataFrame(
        {'球號': results
         })
    exportFile = ExportFile()
    filename = 'relation_{}.csv'.format('0.01')
    exportFile.exportCsv(
        dfProfit, 'C:/Programs/bingo/bingo_scrapy/539_calcu', filename)
    print('')
