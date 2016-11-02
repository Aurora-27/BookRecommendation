
# coding: utf-8

# In[11]:

import pandas as pd


# In[12]:

ratings = pd.read_csv('../newData/df_ratings.csv')


# In[13]:

ratings.head()


# In[14]:

def makeDictUser():
    ratings = pd.read_csv('../newData/df_ratings.csv')
    ratings = pd.DataFrame(ratings)
    dict_ratings = {}
    i = 0
    user_list = set()
    book_list = set()
    for index, row in ratings.iterrows():
        user = row['User-ID']
        isbn = row['ISBN']
        rate = row['Book-Rating']
        i += 1
        dict_ratings.setdefault(user, {} )
        dict_ratings[user][isbn] = rate
        user_list.add(user)
        book_list.add(isbn)
    return [dict_ratings, i, user_list, book_list]

def makeDictBooks():
    ratings = pd.read_csv('../newData/df_ratings.csv')
    ratings = pd.DataFrame(ratings)
    dict_ratings = {}
    i = 0
    for index, row in ratings.iterrows():
        user = row['User-ID']
        isbn = row['ISBN']
        rate = row['Book-Rating']
        i += 1
        dict_ratings.setdefault(isbn, {} )
        dict_ratings[isbn][user] = rate
    return dict_ratings, i


# In[15]:

def sim_pearson(prefs,p1,p2):
     si = {}
     for item in prefs[p1]:
         if item in prefs[p2]: si[item]=1
     n=len(si)
     if n<=3: return 0
     sum1=sum([prefs[p1][it] for it in si])
     sum2=sum([prefs[p2][it] for it in si])
     sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
     sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
     pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
     num=pSum-(sum1*sum2)/n
     den= ( (sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n) )**0.5
     if den==0: return 0
     return num/den


# In[16]:

pref_users ,cnt , users_list ,books_list  = makeDictUser()


# In[17]:

pref_book, _ = makeDictBooks()


# In[18]:

def getSimilarUsers(pref, users_list, user, cnt=5):
    similarity = []
    for given in users_list:
        if( given != user):
            similarity.append( ( sim_pearson(pref,user,given) , given ) )
            #similarity.append(sim_pearson(pref,user,given) )
    similarity = sorted( similarity, key = lambda x: x[0])
    #similarity.sort()
    return similarity[-cnt:]


# In[19]:

print getSimilarUsers(pref_users, users_list, 175117)


# In[20]:

def getSimilarBooks(pref, book_list, book, cnt = 5):
    similarity = []
    for given in book_list:
        if( given != book):
            similarity.append( (sim_pearson(pref_book,book,given) , given ) )
    similarity = sorted( similarity, key = lambda x: x[0])
    return similarity[-cnt:]


# In[21]:

def getBookAverageRating():
    book_rating = {}
    book_count = {}
    avg_rating = {}
    for i,item in ratings.iterrows():
        if( book_rating.get( item['ISBN']) == None):
            book_rating[item['ISBN']] = 0
            book_count[ item['ISBN'] ] = 0
        book_rating[item['ISBN']] += item['Book-Rating']
        book_count[ item['ISBN'] ] += 1
    for keys in book_rating.iterkeys():
        avg_rating[keys] = book_rating[keys] / book_count[keys]
    return avg_rating, book_count


# In[22]:

print getSimilarBooks(pref_book, books_list, "60520507")


# In[32]:

def getRecommendationByUserCollaborative(user, cnt = 5):
    pref_users ,_ , users_list ,books_list  = makeDictUser()
    similarUser = getSimilarUsers(pref_users, users_list, user, 10)
    totals = {}
    simsums = {}
    count = {}
   # print similarUser,"\n\n"
    
    for others in similarUser:
        sim = others[0]
        if( sim <= 0 ):
            continue
        
        for item in pref_users[others[1]]:
            if item not in pref_users[user]:
                totals.setdefault(item,0)
                totals[item] += pref_users[others[1]][item] * sim
                simsums.setdefault(item,0)
                count.setdefault(item,0)
                simsums[item] += sim
                count[item] += 1
                
    rankings = []
    for item,total in totals.items():
        if( count[item] > 1 ):
            rankings.append(( round(total/simsums[item],2) , item) )
            
    #rankings = [ (total/simsums[item], item) for item,total in totals.items() ]
    
    rankings.sort()
    rankings.reverse()
    return rankings[:cnt]    


# In[33]:

def getRecommendationByBookCollaborative(user, cnt = 5):
    pref_users ,_, users_list ,books_list  = makeDictUser()
    pref_book, _ = makeDictBooks()
    listOfRecommendation = []
    listOfRecommendation = [(1.0, '743464672'), (1.0, '60926317'), (1.0, '157322930X'), (1.0, '373250215'), (1.0, '345427637')]
    for book in pref_users[user]:
       tmp = getSimilarBooks(pref_book, books_list, book )
       for got in tmp:
            listOfRecommendation.append(got)
    avg_rate, _ = getBookAverageRating()
    final = []
    for sim,book in listOfRecommendation:
        final.append( (sim*avg_rate[book] , book))
    final.sort()
    final.reverse()
    return final[:cnt]


# In[34]:

getRecommendationByBookCollaborative(175117)


# In[35]:

getRecommendationByUserCollaborative(175117)


# In[ ]:



