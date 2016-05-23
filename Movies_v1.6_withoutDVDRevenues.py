# -*- coding: utf-8 -*-

"""

Created on Wed Mar 23 19:54:02 2016



@author: Yogesh

"""

# Part 1 Importing packages

import requests

import lxml.html

from bs4 import BeautifulSoup

import pandas

import re

from time import sleep



#part1

# Code for extracting the movie Ids

x=0

year = "2016"

Ids_year =[]

for x in range(1,1000,50):

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









print("Extracting Data from IMDB")

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

    #try:

    movie ={}
    movie1={}





    movie1['Language'] = str(tree.xpath('//*[@id="titleDetails"]/div[3]/a[1]/text()'))

    movie1['Language'] = movie1['Language'].replace("[","").replace("]","").replace("'", "")



    if movie1['Language'] in ["English"]:
                
        movie['country'] = str(tree.xpath('//*[@id="titleDetails"]/div[2]/a[1]/text()'))    
        movie['title'] = str(bs.find('title').contents[0])
        
        movie['title']= movie['title'][:-14]
        movie['Language'] = "English"


        movie['year'] = str(tree.xpath('//*[@id="titleYear"]/a/text()'))

        movie['year']= movie['year'].replace("['","")

        movie['year']= movie['year'].replace("']","")

        #//*[@id="titleDetails"]/div[4]/text()

        movie['story_description'] = tree.xpath('//*[@id="titleStoryLine"]/div[1]/p/text()')

        movie['id'] = id

        movie['releasedate'] = str(tree.xpath('//*[@id="titleDetails"]/div[4]/text()')[1])

        movie['releasedate'] = re.sub(r"\(.*\)", "", movie['releasedate']).strip()

        try:
            index_Gross =str(bs.findAll('div', 'txt-block')).find("Gross")
            if index_Gross != -1:            
                movie['movie_revenue']= str(bs.findAll('div', 'txt-block'))[index_Gross+13:index_Gross+40].strip()
                BoxOfficeLastUpdate = str(bs.findAll('div', 'txt-block'))[index_Gross+90:index_Gross+130]
                index_start = BoxOfficeLastUpdate.find("(")
                index_end = BoxOfficeLastUpdate.find(")")
                movie['BoxofficeLastUpdate']= BoxOfficeLastUpdate[index_start+1:index_end]
            else:
                movie['movie_revenue']= ""
                movie['BoxofficeLastUpdate']=""
                
        except:
            movie['movie_revenue']= ""
            movie['BoxofficeLastUpdate']=""
        try:

            Index_Budget = str(bs.findAll('div', 'txt-block')).find("Budget")
            if Index_Budget != -1:           
                movie['budget']= str(bs.findAll('div', 'txt-block'))[Index_Budget+15:Index_Budget+40].strip()
            else:
                movie['budget'] = ""
           #movie['budget'] = str(tree.xpath('//*[@id="titleDetails"]/div[7]/text()')[1].strip())

           # movie['releasedate'] =str(bs.find("div", "comment-meta").contents[0]).split('|')[0].replace("\n","")

            #movie['movie_revenue']=str(tree.xpath('//*[@id="titleDetails"]/div[9]/text()')[1].strip())



        except:
            movie['budget'] = ""
       # movie['releasedate'] = ""

            
            #movie['movie_revenue'] = ""

            #movie['releasedate'] = ""



        movie['ratings'] = str(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()'))

        movie['ratings'] = movie['ratings'].replace("['", "")

        movie['ratings'] = movie['ratings'].replace("']", "")





        movie['duration'] = str(tree.xpath('//*[@id="titleDetails"]/div[12]/time/text()'))

        movie['duration'] = movie['duration'].replace("['", "")
        
        movie['duration'] = movie['duration'].replace("']", "")



        movie['production_company']= []

        movie['production_company'].append(tree.xpath('//*[@id="titleDetails"]/div[10]/span[1]/a/span/text()'))

        movie['production_company'].append(tree.xpath('//*[@id="titleDetails"]/div[10]/span[2]/a/span/text()'))

        movie['production_company'].append(tree.xpath('//*[@id="titleDetails"]/div[10]/span[3]/a/span/text()'))

        movie['production_company'] = str(movie['production_company']).replace("[","").replace("]","").replace("'", "")



        movie['genre'] = []

        movie['genre'].append(str(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/a[1]/span/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")",""))

        movie['genre'].append(str(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/a[2]/span/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")",""))

        movie['genre'].append(str(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/a[3]/span/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")",""))



        movie['director']= str(tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[2]/span/a/span/text()')).replace("[","").replace("]","").replace("'", "")



        movie['cast'] =[]

        movie['cast'].append(str(tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[4]/span[1]/a/span/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")",""))
        
        movie['cast'].append(str(tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[4]/span[2]/a/span/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")",""))

        movie['cast'].append(str(tree.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[4]/span[3]/a/span/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")",""))





   # movie['Opening Weekend Collection'].append(tree1.xpath('//*[@id="tn15content"]/text()[5]

        #movie['Opening Weekend Collection']=(str(tree1.xpath('//*[@id="tn15content"]/text()[5]')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")","").replace("\\n",""))[:-5]

    #movie['no.ofScreens']=(str(tree1.xpath('//*[@id="tn15content"]/text()[7]')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")","").replace("\\n","").replace("Screens", ""))
        try:
            index_OpeningWeekend =str(bs.findAll('div', 'txt-block')).find("Opening Weekend")
            if index_OpeningWeekend != -1 :           
                movie['Opening Weekend Collection']=str(bs.findAll('div', 'txt-block'))[index_OpeningWeekend+22:index_OpeningWeekend+50].strip()
            else:
                movie['Opening Weekend Collection']= ""
        except:
            movie['Opening Weekend Collection']= ""
        try:

            movie['no.ofScreens']= str(bs1.findAll("div")).split("Screens")[0][-7:-1].replace(">","").replace("a","").replace(")","").replace("(", "").replace("</div","")
            movie['poster_url']= str(bs.find('div','poster').contents[1]).split("src=")[1].split("title")[0]
        except:

            movie['no.ofScreens']= ""
            movie['poster_url']= ""


        
       # movie['BoxofficeLastUpdate']= str(tree.xpath('//*[@id="titleDetails"]/div[9]/span[2]/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")","")
                

        #if movie['BoxofficeLastUpdate'] == " " :

         #   try:

          #      movie['BoxofficeLastUpdate']= str(bs.findAll("span", "attribute")).split(",")[3].split(">")[1].split("<")[0]

           # except:

            #    movie['BoxofficeLastUpdate']= " "



        movie['Oscar_information'] = str(tree.xpath('//*[@id="titleAwardsRanks"]/span[1]/b/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")","").replace("\\n","").replace("    ", " ")


        Other_awards = str(tree.xpath('//*[@id="titleAwardsRanks"]/span[2]/text()')).replace("[","").replace("]","").replace("'", "").replace("(","").replace(")","").replace("\\n","").replace("    ", " ")



        try:

            movie['Other_awards_wins'] =  Other_awards.replace("Another   ","").split("&")[0].replace("wins","")

            movie['Other_awards_nominations'] =  Other_awards.replace("Another   ","").split("&")[1].replace("nominations","")



        except:

            movie['Other_awards_wins'] =  ""

            movie['Other_awards_nominations'] = ""

        movielist.append(movie)

    else:
        continue

#importing data to csv

pd_movielist= pandas.DataFrame(movielist)



print("Extracting oscar information from Box office mojo")

###################################################################

#Part 3

#Boxoffice mojo Oscar Information:





title11 = []

Title22=[]

movie33 = []

Title44 = []

Title55=[]

df1 = pandas.DataFrame(movielist)

for title1 in df1['title']:

    Title22.append(title1.replace(" ",""))

for title1 in Title22:

    Title44.append(title1.replace(":",""))

for title1 in Title44:

    title1 = title1.lower()

    Title55.append(title1.replace("the",""))

for title1 in Title55:

    movie33.append(title1.replace("-",""))



Oscar_Wins = []

for moviename in movie33:

    url = "http://www.boxofficemojo.com/oscar/movies/?id="+moviename+".htm"

    r = requests.get(url) # where url is the above url

    bs = BeautifulSoup(r.text)

    tree = lxml.html.fromstring(r.content)



    movie = {}

    index_nomin = 0

    index_wins = 0

    try:



        index_nomin = str(bs.findAll('div')).find('Total Nominations')

        movie['Oscar_Nominations'] = str(bs.findAll('div'))[index_nomin:index_nomin+27].split("<b>")[1].replace("</b","").replace(">","")



        index_wins = str(bs.findAll('div')).find('Total Wins')

        movie['Oscar_Wins'] = str(bs.findAll('div'))[index_wins:index_wins+16].split("<b>")[1].replace(">","")



        index_wins = str(bs.findAll('div')).find('Total Wins')



        if  movie['Oscar_Nominations'] == "414</":

            movie['Oscar_Nominations'] = ""

            movie['Oscar_Wins'] = ""





    except:

        movie['Oscar_Nominations'] = str(" ").replace("[","").replace("]","")

        movie['Oscar_Wins'] = str(" ").replace("[","").replace("]","")



    Oscar_Wins.append(movie)





pd_Oscar_Wins = pandas.DataFrame(Oscar_Wins)

pd_movielist['Oscar_Nominations']= pd_Oscar_Wins['Oscar_Nominations']

pd_movielist['Oscar_Wins']= pd_Oscar_Wins['Oscar_Wins']



print("Extracting DVD information from rotten tomatoes")

#############################################################################################################

# # part4

#importing DVD release  Data from rotten tomatoes

#from dateutil import parser





# # part4
#importing DVD release  Data from rotten tomatoes
#from dateutil import parser


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
    

DVD_release =[]
DVD_release1 =[]
for moviename in Title33:
    url = "http://www.rottentomatoes.com/m/"+ moviename +"/"
    r = requests.get(url) # where url is the above url    
    url1 = "http://www.rottentomatoes.com/m/"+ moviename +"_%s/"%(year)
    s = requests.get(url1)
    bs = BeautifulSoup(r.text)
    bs1 = BeautifulSoup(s.text)
    tree = lxml.html.fromstring(r.content)
    
    movie={}
    movie1 ={}
    
    
    try:
        movie1['title']= moviename
        movie1['rottentomatoes_rating']= str(bs.findAll('tr')[-8]).split('>')[-3].replace("</td", "")
        #movie['DVD_release_date/BoxOffice']= (str(bs.findAll('tr')[-2]).split('>')[-3])
        #movie['DVD_release/release_date']=str(bs.findAll('tr')[-3]).split('>')[-3]
        
        #if  (movie['DVD_release_date/BoxOffice'].find('M') != -1) or (movie['DVD_release_date/BoxOffice'].find('$') != -1) :
        #    movie1['DVD_release']= movie['DVD_release/release_date'].replace("Wide", "").replace("</td", "")
        #else:
        #    movie1['DVD_release']= movie['DVD_release_date/BoxOffice'].replace("Wide", "").replace("</td", "")
        
        index_DVD= str(bs.findAll('tr')).find("On DVD")
        if index_DVD != -1:    
            movie1['DVD_release']=   str(bs.findAll('tr'))[index_DVD+16:index_DVD+42].replace(">","").replace("td","").replace("tr","").replace("<","").replace("/","").replace(",","")      
        elif str(bs1.findAll('tr')).find("On DVD") != -1:
            movie1['DVD_release']=   str(bs1.findAll('tr'))[index_DVD+16:index_DVD+42].replace(">","").replace("td","").replace("tr","").replace("<","").replace("/","").replace(",","")
        else:
            movie1['DVD_release']= " "
            
            
        index_rating= str(bs.findAll('tr')).find('contentRating')
        
        if index_rating != -1:
            index_rating_end = str(bs.findAll('tr'))[index_rating:index_rating+300].find(")")        
            movie1['rottentomatoes_rating']=  str(bs.findAll('tr'))[index_rating:index_rating+index_rating_end].replace('contentRating">',"")            
        elif str(bs1.findAll('tr')).find('contentRating') != -1:
            index_rating_end = str(bs1.findAll('tr'))[index_rating+13:index_rating+300].find(")")        
            movie1['rottentomatoes_rating']=  str(bs1.findAll('tr'))[index_rating:index_rating+index_rating_end].replace('contentRating">',"")         
        else:
            movie1['rottentomatoes_rating']= "" 
         
    except:
        movie1['title']= moviename
        movie1['rottentomatoes_rating']=""
        movie1['DVD_release']= ""
        #try:
            #movie1['title']= moviename
            #movie1['rottentomatoes_rating']= str(bs1.findAll('tr')[-8]).split('>')[-3].replace("</td", "")
           # movie['DVD_release_date/BoxOffice']= str(bs1.findAll('tr')[-2]).split('>')[-3]
            #movie['DVD_release/release_date']=str(bs1.findAll('tr')[-3]).split('>')[-3]
            
           # if  (movie['DVD_release_date/BoxOffice'].find('M') != -1) or (movie['DVD_release_date/BoxOffice'].find('$') != -1) :
            #    movie1['DVD_release']= movie['DVD_release/release_date'].replace("Wide", "").replace("</td", "")
            #else:
             #   movie1['DVD_release']= movie['DVD_release_date/BoxOffice'].replace("Wide", "").replace("</td", "")
            #index_DVD= str(bs.findAll('tr')).find("On DVD")
            #movie1['DVD_release']=   str(bs.findAll('tr'))[index_DVD+16:index_DVD+42].replace(">","").replace("td","").replace("tr","").replace("<","").replace("/","").replace(",","")      

            #index_rating= str(bs.findAll('tr')).find('contentRating')
            #index_rating_end = str(bs.findAll('tr'))[index_rating:index_rating+300].find(")")        
            #movie1['rottentomatoes_rating']=  str(bs.findAll('tr'))[index_rating:index_rating+index_rating_end] 
        
        
        #except:    
         #   movie1['title']= moviename
          #  movie1['rottentomatoes_rating']=" "
           # movie['DVD_release_date/BoxOffice']= " "
            #movie['DVD_release/release_date'] = " "
            #movie1['DVD_release']=" "
    
   # DVD_release1.append(movie)    
    DVD_release.append(movie1)

#pd_DVD_release= pandas.DataFrame(DVD_release)
pd_DVD_release = pandas.DataFrame(DVD_release)
pd_movielist['rottentomatoes_rating']= pd_DVD_release['rottentomatoes_rating']
pd_movielist['DVD_release']= pd_DVD_release['DVD_release']  
pd_movielist.to_csv("Movies_data_%s.csv"%(year))

   
   
   
   