#############################################
# author : Baptiste PICARD 		 			#
# date : 02/07/2020				 			#
# 								 			#
# overview : Retrieving Facebook posts 		#
# and comments.								#
# Facebook posts and comments scraper 		#
# Main file.								#
#############################################

# Imports
import json # Reading .json files
import datetime # Time computation
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options # Webdriver options

# Modules 
from accessDatabase import * 

# Constants
DATA_PATH = './data/variables.json'

if __name__ == "__main__" :
	start = datetime.datetime.now()
	variables = json.load(open(DATA_PATH)) # open private data to setup the system
	db = openDatabase(variables["mongoDB"])
	db_posts = getCollection(db, variables["mongoDB"]["collections"]["posts"])
	db_comments = getCollection(db, variables["mongoDB"]["collections"]["comments"])
	eraseCollection(db_posts)
	eraseCollection(db_comments)
	options = Options() # Set up the option
	options.binary_location = variables['chrome_path'] # Give the chrome path 
	driver = webdriver.Chrome(chrome_options=options, executable_path=variables['chrome_webdriver_path']) # Creating the Web driver
	driver.get("https://www.facebook.com/") # Load the facebook page
	time.sleep(5)
	username= driver.find_element_by_id("email") 
	password = driver.find_element_by_id("pass") 
	bt_log = driver.find_element_by_id("u_0_b") 
	n_posts, n_comments = [], []
	try : # Logging session
		username.send_keys(variables['facebook_id'])
		password.send_keys(variables['facebook_pwd'])
		bt_log.click()
		time.sleep(10)
		driver.get("https://www.facebook.com/jchirac") # Get the fan page of Jacques Chirac
		time.sleep(5)
		posts = driver.find_elements_by_class_name("du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
		if(len(posts)!=0) :
			for index_post, post in enumerate(posts) :
				print("Post number : ",index_post)
				post_text = post.text.split('\n')
				post_date = post_text[1]
				post_resume = post_text[4]
				post_n_likes = post_text[7]
				post_n_comments = post_text[8].split(' ')[0]
				post_n_shares = post_text[9].split(' ')[0]
				post_href = post.find_element_by_xpath("//a[@aria-labelledby='jsc_c_2m' or 'jsc_c_1g']").get_attribute('href')
				n_posts.append({'resume' : post_resume, 'date' : post_date, 'n_likes' : post_n_likes, 'n_comments' : post_n_comments, 'n_shares' : post_n_shares, 'link' : post_href, 'id' : index_post})
				try : 
					post.find_element_by_xpath("//span[contains(text(), 'View comments')]").click()
					time.sleep(10)
					comments = post.find_element_by_class_name("stjgntxs.ni8dbmo4.l82x9zwi.uo3d90p7.h905i5nu.monazrh9").find_elements_by_tag_name("li")
					cmpt = 0
					for com in comments :
						if(len(com.text)>10) :
							print("Post number : ",index_post," / Comment number : ", cmpt)
							com_username = com.text.split('\n')[0]
							com_comment = com.text.split('\n')[1]
							if(('Likes' and 'Like') in com.text.split('\n')[-2]) :
								if(com.text.split('\n')[-3].isdigit()) :
									com_likes = com.text.split('\n')[-3]
								else : 
									com_likes = '0'
							elif(('Likes' and 'Like') in com.text.split('\n')[-3]):
								if(com.text.split('\n')[-4].isdigit()) :
									com_likes = com.text.split('\n')[-4]
								else : 
									com_likes = '0'
							else : 
								com_likes = '0' 
							if("·" in com.text.split('\n')[-1]) :
								if(com.text.split('\n')[-1].split(" · ")[-1] != "Edited") :
									com_date = com.text.split('\n')[-1].split(' · ')[-1]  
								else :
									com_date = com.text.split('\n')[-1].split(' · ')[-2] 
							elif("·" in com.text.split('\n')[-2]) :
								if(com.text.split('\n')[-2].split(" · ")[-1] != "Edited") :
									com_date = com.text.split('\n')[-2].split(' · ')[-1]  
								else :
									com_date = com.text.split('\n')[-2].split(' · ')[-2] 
							else : 
								com_date = "No date"
							if("·" not in com.text.split('\n')[-1]) :
								com_n_replies = com.text.split('\n')[-1].split(' ')[0] 
							else :
								com_n_replies = '0'
							cmpt = cmpt + 1
							comment = {'user' : com_username, 'comment' : com_comment,  'likes' : com_likes, 'date' : com_date, 'n_replies' : com_n_replies, 'id_post' : index_post, 'id' : cmpt}
							n_comments.append(comment)
						else :
							pass
					fillCollection(db_posts, n_posts)
					fillCollection(db_comments, n_comments)
					break
				except Exception as exc_btn :
					print("Can't load the data")
					print(exc_btn)
		else : 
			print('No posts')
		driver.close()
		print(n_posts)
	except Exception as exc :
		print("Error while logging")
		print(exc)
	print("It takes {} seconds to reach the end of the script.".format(datetime.datetime.now()-start))