#############################################
# author : Baptiste PICARD 		 			#
# date : 03/07/2020				 			#
# 								 			#
# overview : Retrieving Facebook posts 		#
# and comments.								#
# Facebook posts and comments scraper 		#
# Main file.								#
# Functions to access collections in python #
#############################################

# Imports
import pymongo 

# Functions 
def openDatabase(json_mongoDB) : 
	"""
		overview : return the database (using pymongo) which contains all the collection.
		entries :
			- json_file : The data loaded are data in json format. This data provide information about the connection.
		returns :
			- database : database NoSql (mongoDB) with all collections.
	"""
	link = json_mongoDB['link']
	link = link.replace('<user>', json_mongoDB['id']).replace('<password>', json_mongoDB['pwd']).replace('<dbname>', json_mongoDB['database'])
	client = pymongo.MongoClient(link)
	return client[json_mongoDB['database']]

def getCollection(db, collection_name) :
	"""
		overview : return the collection with all the datas in, using a database and the collection_name.
		inputs :
			- database :  database NoSql which contains all the collection.
			- collection_name : string which represents the name of the collection.
		returns :
			- collection : collection with all its datas.
	"""
	return db[collection_name] 

def eraseCollection(collection) :
	"""
		overview : Erase all the elements of the collection.
		entries :
			- collection : collection of our database.
	"""
	print('Deleting all the datas in the database : ',str(collection.name))
	collection.delete_many({})

def fillCollection(collection, items) : 
	"""
		overview : fill our collection.
			Each item is a dictionnary.
		inputs : 
			- collection : mongoDB collection.
			- items :  list of item. 
	"""
	print('Fill the collection : ', str(collection.name))
	cmpt = 0
	for item in items : 
		collection.insert_one(item)
		cmpt += 1
	print('Collection filled with ',cmpt,' items.')