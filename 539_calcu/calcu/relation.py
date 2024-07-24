from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from typing import List
import pandas as pd


class RelationTerm:
    """計算二球之間關聯式規則,參數可透過前幾期、最小支持、信賴度來做關卡,過濾二球以上關聯規則"""
    @property
    def min_support(self):
        return self.__min_support

    @min_support.setter
    def min_support(self, value):
        self._min_support = value

    @property
    def frt(self):
        return self._frt

    @frt.setter
    def frt(self, value):
        self._frt = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def min_threshold(self):
        return self._min_threshold

    @min_threshold.setter
    def min_threshold(self, value):
        self._min_threshold = value

    def __init__(self, inputs: List[str]) -> None:
        self._min_support = 0
        self._min_threshold = 0
        self._inputs = inputs
        pass

    def calcu(self) -> List[List[str]]:

        ball2Ds = self._inputs[self._frt:self._end]
        te = TransactionEncoder()
        te_ary = te.fit(ball2Ds).transform(ball2Ds)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        # 使用apriori找出频繁项集
        frequent_itemsets = apriori(
            df, min_support=self._min_support, use_colnames=True)
        if frequent_itemsets.empty:
            return []
        # 生成关联规则
        rules = association_rules(
            frequent_itemsets, metric="confidence", min_threshold=self._min_threshold)
        dfRelation = rules
        # 空的DataFrame
        if dfRelation.empty:
            return []
        dfRelation['result'] = dfRelation.apply(
            lambda row: self._mapToArrayFilterThree(row), axis=1)

        temps = list(
            filter(self._includeThree, dfRelation['result'].tolist()))
        temps = sorted(
            temps, key=lambda q: q['lift'], reverse=True)
        results = list(map(lambda x: x['arr'], temps))

        # 將每個內部陣列轉換為集合
        set_list = [set(inner_list) for inner_list in results]

        # 使用集合來比較內部陣列是否有重複
        unique_set_list = []

        for s in set_list:
            if s not in unique_set_list:
                unique_set_list.append(s)
        relationShips = [list(item) for item in unique_set_list]
        return relationShips
        pass

    # 過濾掉3個元素
    def _includeThree(self, obj):
        return len(obj['arr']) == 2
        print("")
        pass

    # 因為可能有3個元素存在,所以將frozenset to list and filter len == 2
    def _mapToArrayFilterThree(self, row: pd.Series):
        # 先將其合成一個obj,內含array and lift
        arrAntecedents = list(row['antecedents'])
        arrConsequents = list(row['consequents'])
        arrAntecedents.extend(arrConsequents)
        lift = float(row['lift'])
        return {'lift': lift, 'arr': arrAntecedents}
        print('')
        pass
