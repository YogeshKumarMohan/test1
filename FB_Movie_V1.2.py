# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 16:40:31 2016

@author: Yogesh
"""

import codecs
import csv
import pandas
import json
import urllib

import requests
import lxml.html
from bs4 import BeautifulSoup
import re
from time import sleep


#part1
# Code for extracting the movie Ids
x=0
year = "2012"
Ids_year =[]
for x in range(1,800,50):
    url1 = "http://www.imdb.com/search/title?sort=num_votes,desc&start="+str(x)+"&title_type=feature&year=%s"%(year)
    r = requests.get(url1) # where url is the above url    
    bs = BeautifulSoup(r.text)
    tree1 = lxml.html.fromstring(r.content)
    ids = tree1.xpath('//*[@id="main"]/table/tbody/tr[2]/td[3]/span[1]/text()')
    Ids = []
    for movie in bs.findAll('td','title'):
        Id= movie.findAll('a')
        Id = str(Id[0])
        Id = Id.split('/')
        Ids_year.append(Id[2])
    

#######################################################################################
#part2
#Code fir extracting movie details from Imbd

movielist=[]
for id in Ids_year:
    url = "http://www.imdb.com/title/"+ id +"/"
    r = requests.get(url) # where url is the above url    
    bs = BeautifulSoup(r.text)
    tree = lxml.html.fromstring(r.content)
    
    url1 = "http://www.imdb.com/title/"+id+"/business?ref_=tt_dt_bus"
    s = requests.get(url1) # where url is the above url    
    bs1 = BeautifulSoup(s.text)
    tree1 = lxml.html.fromstring(s.content)
    
    # http://www.imdb.com/title/tt0137523/awards?ref_=tt_awd
    # //*[@id="main"]/div[1]/div/div[2]/div/div
    try:
        movie ={}
        
        movie['country'] = str(tree.xpath('//*[@id="titleDetails"]/div[2]/a[1]/text()'))
        movie['country'] = movie['country'].replace("[","").replace("]","").replace("'", "") 
        
        if movie['country'] == "USA":
            movie['title'] = str(bs.find('title').contents[0])
            movie['title']= movie['title'][:-14]
        else:
            continue
    
    except:
       continue
    
    movielist.append(movie)


APP_ID ="216313582060233"
APP_SECRET= "daa140092d583de2ab35bb3b039f230f"

#url11 = "https://graph.facebook.com/"+post_id + "/likes?summary=true&key=value&access_token" + APP_ID + "|" + APP_SECRET

#list_movies = ["Inception","ShutterIsland","BlackSwan","Toy Story 3"]
#movie_name = "inception"
#def movie_post(movie_name):

title11 = []
Title22=[]
Title = []
df1 = pandas.DataFrame(movielist)
for title1 in df1['title']:
    Title22.append(title1.replace(" ","").lower())
for title1 in Title22:
    Title.append(title1.replace(":","").replace("-",""))  


pd_fb_posts1 = pandas.DataFrame()

for movie_name in Title:    
    movie_posts =[]
    pd_fb_post = pandas.DataFrame()
    post_url =  'https://graph.facebook.com/' + movie_name + "/posts/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
    post_url1 = 'https://graph.facebook.com/' + movie_name + "movie/posts/?key=value&access_token=" + APP_ID + "|" + APP_SECRET    
    print(movie_name)  
    
    try:
         reader = codecs.getreader("utf-8")
         response= urllib.request.urlopen(post_url)
    except:
        post_url = post_url1
        
    
    for i in range(15):
        #movie_posts = []
        try:
            
            reader = codecs.getreader("utf-8")
            response= urllib.request.urlopen(post_url)
            obj = json.load(reader(response))
    
            fb_posts= obj['data']
            fb_posts = list(fb_posts)
            fb_posts= list(obj['data'])
        except:
            continue
    
        try:
            fb_nextpage = obj['paging'] ['next']
        except:
            break
    
        for post in fb_posts:
            post_details={}
            
            try:           #try to print out data
                post_details["movie"] = movie_name
                post_details["ID"]=post["id"]
                post_details["Post"]=post["message"]
                post_details["Time"]=post["created_time"]
            except:
                try:
                    post_details["movie"] = movie_name
                    post_details["ID"]=post["id"]
                    post_details ["Story"]= post["story"]
                    post_details["Time"]=post["created_time"]
                except:   
                    continue
            
            movie_posts.append(post_details)
        post_url = fb_nextpage
    try:
        pd_fb_posts = pandas.DataFrame(movie_posts)
    except:
        continue
    pd_fb_posts1 = pd_fb_posts1.append(pd_fb_posts)
    


#######################################################################
#Code to extract no. of likes for each post
# comment_id = "10153689737333701"
import codecs
import csv
import pandas




reader = codecs.getreader("utf-8")

PostIds = list(pd_fb_posts1['ID'])
movielist = list(pd_fb_posts1['movie'])


likes = []
for post_id in PostIds:
    
    url = "https://graph.facebook.com/"+post_id+"/likes/?summary=true&key=value&access_token=" + APP_ID + "|" + APP_SECRET
    try:    
        response= urllib.request.urlopen(url)
    except:
        continue
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(response))
    fb_posts= obj['data']
    fb_posts = list(fb_posts)
    fb_posts= list(obj['data'])
    
    like_details= {}
    
    try:
        like_details['no.oflikes'] = obj['summary']['total_count']
    except:
        like_details['no.oflikes'] = ""
    likes.append(like_details)
    
    
pd_no_likes = pandas.DataFrame(likes)
pd_fb_posts1['No.ofLikes']= pd_no_likes['no.oflikes']
pd_fb_posts1.to_csv("Fb_posts_%s.csv"%(year))

######################################################################################
# Code to extract comments




comments=[] 
for comment_id in PostIds:
    comment_url = 'https://graph.facebook.com/'+ comment_id +"/comments/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
    for i in range(10):    
        try:    
            response= urllib.request.urlopen(comment_url)
        except:
            continue
        obj = json.load(reader(response))
        fb_posts= obj['data']
        fb_posts = list(fb_posts)
        fb_posts= list(obj['data'])
        try:
            fb_nextpage = obj['paging'] ['next']
        except:
            break
    
        for item in fb_posts:
            try:            
                comments_details = {}
                #comments_details['movie'] = movie_name
                comments_details['comment']= item['message']
                comments_details ['user'] = item ['from']['name']
                comments_details['Time'] = item ['created_time']
                comments_details['PostID'] = comment_id
            except:
                continue
            
            comments.append(comments_details)
    
        comment_url = fb_nextpage
       
 
df_comments = pandas.DataFrame(comments) 
df_comments.to_csv("Fb_comments.csv") 
    
       