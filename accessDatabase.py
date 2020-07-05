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
import os
import pandas
import csv
import json
import pymongo 
from bson import json_util


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
		overview : fill a collection.
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

def getCollectionItems(collection) :
	"""
		overview : return a collection.
		inputs : 
			- collection : mongoDB collection.
			- items :  list of item (=list of dictionnary). 
	"""
	return list(collection.find())


def collectionToJson(my_colletion, file_name) :
	"""
		overview : save a collection -> json.
		inputs : 
			- collection : mongoDB collection.
	"""
	collection = json.loads(json_util.dumps(my_colletion.find()))
	if not os.path.exists('./data/'+file_name) :
		with open('./data/'+file_name, 'w', encoding='utf8') as file:
			file.write('[')
			for index, item in enumerate(collection) : 
				file.write(json.dumps(item, ensure_ascii=False))
				if(index+1 != len(collection)) :
					file.write(',')
			file.write(']')
		print('File ./data/'+file_name+' created.')

def deleteFile(file) :
	"""
		overview : delete a  file.
		inputs : 
			- file :  file.
	"""
	if os.path.exists('./data/'+file) :
		os.remove('./data/'+file)
		print('File ',file,' deleted.')

def fromJsonToCsv(json_file) : 
	json_data = pandas.read_json('./data/'+json_file)
	json_data = json_data.astype({'id' : str})
	for index, row in json_data.iterrows() :
		json_data.set_value(index, 'id', row['_id']['$oid'])
	json_data = json_data.drop('_id', axis=1)
	if not os.path.exists('./data/'+json_file.replace('.json', '.csv')) : 
		json_data.to_csv('./data/'+json_file.replace('.json', '.csv'), index=False)
		print('File ./data/',json_file.replace('.json', '.csv'),' created')