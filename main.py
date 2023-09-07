import pandas as pd
from collections import defaultdict
from itertools import chain
import statistics
from itertools import combinations

numbers = list(range(1, 81))  # 生成 1 到 80 的数字列表
combinations_array = list(combinations(numbers, 4))
valid = len(combinations_array)
bingoData = [
    {'term':'1','balls':[1,2,3,4,5,10]},
    {'term':'2','balls':[1,2,6,9,5,10]},
    {'term':'3','balls':[1,8,3,4,5,10]},
    {'term':'4','balls':[1,8,7,9,6,10]},
    {'term':'5','balls':[9,8,3,6,5,10]},
    {'term':'6','balls':[9,8,3,1,2,10]},
    {'term':'7','balls':[9,8,3,1,2,10]},
    {'term':'8','balls':[9,8,3,4,2,10]},
]
BALL_NUM = 6
support :float
max :int
median_value :float

input = [1,2]
#region concat length filter whether match count support
setConcat = list(map(lambda r:set(r['balls'] + input),bingoData))
arrConcat = list(map(lambda r:list(r),setConcat))
arrTermConcat = list(map(lambda x,y:{'term':y['term'],'balls':x},arrConcat,bingoData))
arrFilter = list(filter(lambda r:len(r['balls']) == BALL_NUM,arrTermConcat))
support = len(arrFilter) / len(bingoData)
#endregion

#region map term array map plus time array,count max、median
arrIntTerm = list(map(lambda r:int(r['term']),arrFilter))
arrIntTime = []
i = 0
for term in arrIntTerm:
  if i !=0:
    temp = arrIntTerm[i] - arrIntTerm[i-1]
    arrIntTime.append(temp)
  i = i+ 1

max = max(arrIntTime)
median_value = statistics.median(arrIntTime)
#endregion




#array group dict key num value times
#map number
dictSupport = {}
arr = list(map(lambda r: r['balls'],bingoData))
arrFlat = list(chain.from_iterable(arr))
for x in arrFlat:
  if x in dictSupport.keys():
    dictSupport[x] = dictSupport[x] + 1
  else:
    dictSupport[x] = 1


print('')
