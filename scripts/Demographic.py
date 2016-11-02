
# coding: utf-8

# In[5]:

import pandas as pd


# In[6]:

#bx_ratings = pd.read_csv("../newData/df_ratings.csv")
#bx_books = pd.read_csv("../newData/df_bookss.csv")
#bx_users = pd.read_csv("../newData/df_userss.csv")


# In[7]:

import operator
def find_best_books(listofBooks, cnt):    
    book_rate = {}
    book_count = {}
    for book,rate in listofBooks:
        if( book_rate.get(book) == None):
            book_rate[book] = 0
            book_count[book] = 0
        book_rate[book] += float(rate)
        book_count[book] += 1
    best_books = []
    limit = ( max(book_count.iteritems(), key=operator.itemgetter(1))[1] ) * 0.2
    for keys in book_count.iterkeys():
        if( book_count[keys] >= limit):
            best_books.append( ( round(book_rate[keys]/book_count[keys] , 2) , keys))
    #print book_count['439139597']
    cnt = min(cnt, len(best_books) )
    return sorted(best_books, reverse=True)[:cnt]
    


# In[8]:

#find_best_books( book_country_map[0][' usa'])


# In[9]:

def getUserAgeMap(bx_users):
    map_user_age = {}
    #bx_users = pd.read_csv("newData/df_userss.csv")
    for i,item in bx_users.iterrows():
        map_user_age[ item['User-ID'] ] = item['Age']
    return map_user_age

def getUserCountryMap(bx_users):
    map_user_country = {}
    #bx_users = pd.read_csv("newData/df_userss.csv")
    for i,item in bx_users.iterrows():
        map_user_country[ item['User-ID'] ] = item['Location']
    return map_user_country


# In[10]:

def getAgeGroup( age ):
    if( age <= 30):
        return 0
    elif ( age > 30 and age <= 60):
        return 1
    return 2


# In[11]:

def getDictionaryOfGroupByBooks(user, bx_ratings, bx_users):
    ageMap = getUserAgeMap(bx_users)
    countryMap = getUserCountryMap(bx_users)
    
    group = getAgeGroup( ageMap[user] )
    country = countryMap[ user ]
    
    #bx_ratings = pd.read_csv("newData/df_ratings.csv")
    listOfBooks = []
    for i,item in bx_ratings.iterrows():
        user = item['User-ID']
        if( countryMap[ user ] == country and getAgeGroup( ageMap[ user ] ) == group ):
            listOfBooks.append( (item['ISBN'], item['Book-Rating']) )
    return listOfBooks


# In[12]:

def getRecommendationByDemographic(user):
    bx_ratings = pd.read_csv("../newData/df_ratings.csv")
    bx_books = pd.read_csv("../newData/df_bookss.csv")
    bx_users = pd.read_csv("../newData/df_userss.csv")
    listofBooks = getDictionaryOfGroupByBooks(user, bx_ratings, bx_users)
    recommended_books = find_best_books(listofBooks, 5)
    return recommended_books


# In[13]:

getRecommendationByDemographic(276925)


# In[ ]:



