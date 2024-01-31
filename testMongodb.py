from datetime import datetime
from bingo_scrapy.bingo_scrapy.db import MongoDbContext

# region
db = MongoDbContext("localhost", "LotteryTicket")
collectionBingo = db.getCollection("Bingo")
collectionOddEven = db.getCollection("OddEven")

# Where Select
objWhere = {}
objSelect = {"dDate": 1, "drawTerm": 1, "_id": 0}
data = list(collectionBingo.find(objWhere, objSelect))


# Join
# objLookup = {"from": "OddEven", "localField": "drawTerm",
#              "foreignField": "drawTerm", "as": "oddEven"}
# pipline = [{"$lookup": objLookup}, {"$project": {"oddEven": 1}}]

# Where Group Sort
# objMatch = {'dDate': {'$gte': datetime(2024, 1, 1)}}
# objCount = {"$sum": 1}
# objGroup = {"_id": "$dDate", "count": objCount}
# objSort = {"_id": 1}
# pipline = [{"$match": objMatch},
#            {"$group": objGroup},
#            {"$sort": objSort}]
condObj = {"$cond": {

}}
projectObj = {"drawTerm": 1, "flag": condObj}
pipline = [{"$project": projectObj}]

arr = list(collectionOddEven.aggregate(pipline))

print("")
# endregion


# db = MongoDbContext("localhost", "LotteryTicket")
# table = "Bingo"
# queryKey = {}

# queryKey = {"bigShowOrder": {"$all": ["05", "06"]}, "dDate": {
#     "$gte": datetime(2024, 1, 24)}}

# collection = db.getCollection(table)
# result = collection.find(queryKey)
# executionStats = result.explain()
# print(executionStats['executionStats']['executionTimeMillis'])
# indexes = collection.list_indexes()

print("")
# pipline = [{"$count": "total"}]
# pipline = [{"$group": {"_id": "$dDate", "count": {"$sum": 1}}}]
# collection = db.getCollection(table)
# result = collection.aggregate(pipline)

# region
# lists = []
# for item in result:
#     obj = {}
#     for pair in item.keys():
#         if pair == 'drawTerm':
#             obj['drawTerm'] = item['drawTerm']
#         elif pair == 'bigShowOrder':
#             odds = filter(lambda e: e % 2 == 0, item['bigShowOrder'])
#             evens = filter(lambda e: e % 2 != 0, item['bigShowOrder'])
#             obj['odd'] = len(list(odds))
#             obj['even'] = len(list(evens))
#     lists.append(obj)
# db.Insert("OddEven", lists)
# print(len(lists))
# endregion
