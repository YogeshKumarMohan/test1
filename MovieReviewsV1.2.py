# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 11:04:44 2016

@author: dulacat
"""
import codecs
import csv
import pandas
import json
import urllib

import requests
import lxml.html
from bs4 import BeautifulSoup
from time import sleep


#part1
# Code for extracting the movie Ids
x=0
year = "2013"
Ids_year =[]
for x in range(1,600,50):
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
    
    
    

#################################################################################
# Part 4: Retrieving Audience Movie Review

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

#importing data to csv    
pd_movielist= pandas.DataFrame(movielist)

    
title11 = []

Title22=[]

Title33 = []

Title44 = []

Title55 = []

df1 = pandas.DataFrame(movielist)



for title1 in  df1['title']:

    Title22.append(title1.replace(" ","_"))

for title1 in Title22:

    Title44.append(title1.replace(":","").replace(".",""))

for title1 in Title44:

    title1 = title1.lower()

    Title55.append(title1)

for title1 in Title55:

    Title33.append(title1.replace("-","_"))



y=0
Audience_review = []
for moviename in Title33[:10]:
    for pageno in range(1,25):
        url = 'http://www.rottentomatoes.com/m/'+moviename+'/reviews/?page=%d&type=user'%(pageno)
        r = requests.get(url) # where url is the above url    
        bs = BeautifulSoup(r.text)
        tree1 = lxml.html.fromstring(r.content)
        
        if tree1.xpath('//*[@id="main_container"]/div[1]/div[1]/div/div[1]/h2/a/text()') == []:
            url = 'http://www.rottentomatoes.com/m/'+moviename+'_%s/reviews/?page=%d&type=user'%(year,pageno)
            r = requests.get(url) # where url is the above url    
            bs = BeautifulSoup(r.text)
            tree1 = lxml.html.fromstring(r.content)
        for i in range(1,20):
            Reviews={}
            try:
                Reviews['Name'] = tree1.xpath('//*[@id="reviews"]/div[3]/div[%d]/div[1]/div[3]/a/text()'%(i))
                Reviews['reviews']=tree1.xpath('//*[@id="reviews"]/div[3]/div[%d]/div[2]/div/text()'%(i))
            except:
                continue
            Reviews['Moviename'] = tree1.xpath('//*[@id="main_container"]/div[1]/div[1]/div/div[1]/h2/a/text()')
            Reviews['Date']= tree1.xpath('//*[@id="reviews"]/div[3]/div[%d]/div[2]/span[2]/text()'%(i))
            try:
                Reviews['Super_Reviewer']= tree1.xpath('//*[@id="reviews"]/div[3]/div[%d]/div[1]/div[2]/div/text()'%(i))
            except:
                Reviews['Super_Reviewer']= " "
            star = 1
            half =""  
            try:
                if str(bs.findAll('span', 'fl')[i-1]).find("½") != -1:
                    half = "½"
            except:
                continue
            try:
                for i in str(bs.findAll('span', 'fl')[i-1]).split("glyphicon glyphicon-star"):
                    if i.find('</span><span') != -1:
                        star += 1
                        Reviews['ratings']= str(star) + half
            except:
    
                continue
            Audience_review.append(Reviews)
        
    y+40
    sleep(180)
            
    
pd3= pandas.DataFrame(Audience_review)
pd3.to_csv("Audience_reviews_%s.csv"%(year))   



###############################################################################################
#Part 5: Retrieving Critic Reviews
Critic_review =  []

for moviename in Title33:
    for pageno in range(1,15):
        url1 = "http://www.rottentomatoes.com/m/"+moviename+"_%s/reviews/?page=%d&sort="%(year,pageno)
        r = requests.get(url1) # where url is the above url    
        bs = BeautifulSoup(r.text)
        tree1 = lxml.html.fromstring(r.content)
        
        if tree1.xpath('//*[@id="main_container"]/div[1]/div[1]/div/div[1]/h2/a/text()') == []:
            url1 = "http://www.rottentomatoes.com/m/"+moviename+"/reviews/?page=%d&sort="%(pageno)
            r = requests.get(url1) # where url is the above url    
            bs = BeautifulSoup(r.text)
            tree1 = lxml.html.fromstring(r.content)
            
            if tree1.xpath('//*[@id="main_container"]/div[1]/div[1]/div/div[1]/h2/a/text()') == []:
                continue 

        for i in range(1,21):
    
            reviews = {}
            try:
                reviews['moviename']= tree1.xpath('//*[@id="main_container"]/div[1]/div[1]/div/div[1]/h2/a/text()')
                reviews['Reviewer_name']=tree1.xpath('//*[@id="reviews"]/div[2]/div[4]/div[%d]/div[1]/div[3]/a/text()'%(i))
                reviews['Company'] = tree1.xpath('//*[@id="reviews"]/div[2]/div[4]/div[%d]/div[1]/div[3]/em/text()'%(i))
                reviews['review']  = tree1.xpath('//*[@id="reviews"]/div[2]/div[4]/div[%d]/div[2]/div[2]/div[2]/div[1]/text()'%(i))
                reviews['ratings']=tree1.xpath('//*[@id="reviews"]/div[2]/div[4]/div[%d]/div[2]/div[2]/div[2]/div[2]/text()'%(i))
                                 
            except:
                continue
        
            Critic_review.append(reviews)
    
pd4 = pandas.DataFrame(Critic_review)
pd4.to_csv("Critic_review_%s.csv"%(year))

