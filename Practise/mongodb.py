import pymongo

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
test = mydb['test']
test.insert_one({'name': 'Jan', 'gender': '男', 'grade': 89})

