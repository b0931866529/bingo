import os
from turtle import pd
from typing import List
from pandas import DataFrame
import pandas as pd


class ExportFile:
    """注入ICalcu子類別結果產出DataFrame To Csv"""

    def __init__(self) -> None:
        pass

    def exportCsv(self, df: DataFrame, path: str, filename: str) -> None:
        file = os.path.join(path, filename)
        # 檢查文件是否存在
        if os.path.exists(file):
            os.remove(file)  # 刪除已存在的文件
        df.to_csv(file, index=False, encoding='utf-8-sig')
        pass

    def exportExcel(self, dfs: List[DataFrame], sheets: List[str], path: str, filename: str) -> None:
        file = f'{path}/{filename}'
        # 檢查文件是否存在
        if os.path.exists(file):
            os.remove(file)  # 刪除已存在的文件

        zipped = list(zip(dfs, sheets))
        with pd.ExcelWriter(file, engine='openpyxl') as writer:
            for df, sheet in zipped:
                # Write each DataFrame to a separate sheet
                df.to_excel(writer, sheet_name=sheet, index=True)
        pass
