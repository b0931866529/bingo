import json
import numpy as np
import pandas as pd
from pandas import DataFrame


# ready DataFrame [profit,matchPercent] to json
# json add key run parameter
# loop 3 json

if __name__ == '__main__':
    # region df to json
    # df = DataFrame({'profit': [1, 2, 3, 4, 5],
    #                'matchPercent': [2, 4, 6, 8, 10]})
    # df.to_json('test.json', orient='records')
    # endregion
    periods = [10, 20, 30]
    for i in periods:
        for j in range(1, 3):
            dictData = {}
            dictData['period'] = i
            dictData['profit'] = 1000 * j
            dictData['matchPercent'] = 0
            # Write dictionary to JSON file
            with open(f'data_{i}_{j}.json', 'w') as json_file:
                json.dump(dictData, json_file, indent=4)
    pass
