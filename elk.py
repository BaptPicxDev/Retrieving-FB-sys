#############################################
# author : Baptiste PICARD 		 			#
# date : 06/07/2020				 			#
# 								 			#
# overview : Retrieving Facebook posts 		#
# and comments.								#
# Facebook posts and comments scraper 		#
# Functiosn to link MongoDB data to 		#
# Elastic Search.							# 
#############################################

# Imports 
import json
from bson import json_util
from elasticsearch import Elasticsearch

def setUpESConnection() :
	"""
		overview : create a connection with ElasticSearch (localhost:9200 by default).
		returns :
			- ElasticSearch : ElasticSearch connector.
	"""
	print("Starting the MongoDB -> Elastic Search connector.")
	return Elasticsearch() # Set-up for localhost:9200


def createESIndex(ES_connector, data) :
	"""
		overview : using the ElasticSearch connector, I will add data to a specific index of EL.
		entries :
			- ES_connector : Elastic Szearch connector created by the function below.
			- data : mongoDB cursor.
	"""
	print('Adding data to ElasticSearch index.')
	for index, row in enumerate(data) :
		if('_id' in row.keys()) :
			row.pop('_id')
		ES_connector.index(index="my-test-index", doc_type="test-type", id=index, body=row)