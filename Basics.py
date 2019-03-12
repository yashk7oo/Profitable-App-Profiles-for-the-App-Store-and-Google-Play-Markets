#!/usr/bin/env python
# coding: utf-8

# # Profitable app profiles for App Store and    Google Play Markets
# 
# In this project, we assume that our company developes ios and android apps that are free to download and install.
# The major factor affecting the revenue of our apps is in-app ads.
# 
# Our goal for this project is to analyze data to help our developers understand what kinds of apps are likely to attract more users.

# In[1]:


from csv import reader

opened_file=open('AppleStore.csv')
readfile=reader(opened_file)
ios=list(readfile)
ios_header=ios[0]
ios=ios[1:]


opened_file=open('googleplaystore.csv')
readfile=reader(opened_file)
android=list(readfile)
android_header=ios[0]
android=android[1:]



# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))
        


# In[3]:


del(android[10472])


# In[4]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)
        print('\n')


# The above cell demonstrateds that the google playstore dataset has duplicate rows.
# Now let us count the total number of duplicate rows in google play store dataset.

# In[5]:


duplicate=[]
unique=[]
for row in android:
    name=row[0]
    if(name in unique):
        duplicate.append(name)
    else:
        unique.append(name)
print("Count of duplicate apps:",len(duplicate))
print('\n')
print("Count of unique apps:",len(unique))

In order to analyze data,we first have to remove redundant records or duplicate apps entries in our case.

We iterate over each entry and of all the duplicate records,we preserve only the one with the highest rating.This is done to make sure that the best result for each app is obtained in terms of rating.We can have some other criteria as well.
# In[6]:


duplicate1=[]
unique1=[]
for row in ios:
    name=row[1]
    if(name in unique1):
        
        duplicate1.append(name)
    else:
        
        unique1.append(name)
print("Count of duplicate apps:",len(duplicate1))
print('\n')
print("Count of unique apps:",len(unique1))


# In[7]:


reviews_max={}
rating_max={}
for row in android:
    name=row[0]
    n_reviews=float(row[3])
    if(name in reviews_max and n_reviews>reviews_max[name]):
        reviews_max[name]=n_reviews
    elif(name not in reviews_max):
        reviews_max[name]=n_reviews
print(len(reviews_max))

for row1 in ios:
    name1=row1[1]
    n_rating=float(row1[5])
    if(name1 in rating_max and n_rating>rating_max[name1]):
        rating_max[name1]=n_rating
    elif(name1 not in rating_max):
        rating_max[name1]=n_rating


# In[8]:


android_clean = []
already_added = []
ios_clean=[]
already_added1=[]

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
        
for app1 in ios:
    name1 = app1[1]
    n_rating = float(app1[5])
    
    if (rating_max[name1] == n_rating) and (name1 not in already_added1):
        ios_clean.append(app1)
        already_added1.append(name1)


# In the above cell,we consider the fact that if more than one records have same maximum value of rating for same app,we can still have duplicate data.
# 
# In order to avoid that we isolate name and review,then iterate through our android data set and only if name is not in already_added list and rating of that record is equal to max rating fo app with same name,we append the record to android_clean list.
# 
# We do the same thing with ios app dataset but filter it based on rating count as reviews are not present in the dataset.
# 
# This way we get a new dataset only having unique records.

# In[9]:


def lang(string):
    c=0
    for i in range(0,len(string)):
        if(ord(string[i])>127):
            c +=1
    if(c<=3):
        return True
    return False


# In[10]:


android_english=[]
ios_english=[]
for row in android_clean:
    if(lang(row[0])):
        android_english.append(row)
        
for row1 in ios_clean:
    if(lang(row1[1])):
        ios_english.append(row1)
print(len(android_english),len(ios_english))


# In[11]:


free_apps_android=[]
free_apps_ios=[]
for row in android_english:
    price=row[7]
    if(price=='0'):
        free_apps_android.append(row)
for app in ios_english:
    price = app[4]
    if price == '0.0':
        free_apps_ios.append(app)
        
print(len(free_apps_android))
print(len(free_apps_ios))


# The stratergy adopted by the company for a new app idea is:
# 
# 1)Minimal android version of app is added to playstore.
# 2)If app has good response,we develop it further.
# 3)If app is profitable after 6 months,we develop it for ios platform as well.
# 
# We need those app profile which are successful on both the markets as they might be really productive.
# 
# Let's analyze some common genres for each market seperately
#     

# In[12]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1

    total=len(dataset)
    percent_table={}
    for row1 in table:
        percent_table[row1]=(table[row1]/total)*100
    

    return(percent_table)

def display_table(dataset, index):
    table = freq_table(dataset, index)
    
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        


# In[13]:


display_table(free_apps_ios,-5)


# In[14]:


display_table(free_apps_android,1) #category


# In[16]:


display_table(free_apps_android,-4) #genres


# From android app dataset,we will only consider category for further analysis and neglect genres as we want to focus on the bigger picture.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.
# 
# We need to know genres which are most popular.For android dataset,we can get this info from installs columan and calculate average number of installs.but for app store dataset,we need to consider user ratings as no installs column is present.
# 
# Now we calculate average number of user ratings per app genre for app store dataset.

# In[17]:


genres_ios=freq_table(free_apps_ios,-5)
for genre in genres_ios:
    total=0
    len_genre=0
    for i in free_apps_ios:
        genre_app=i[-5]
        if(genre_app==genre):
            nratings=float(i[5])
            total +=nratings
            len_genre +=1
    avg_rating=total/len_genre
    print(genre,':',avg_rating)
    


# We seee that App Store has maximum user reviews for navigation Genre.But on further inspection,we find that this count is dominated by 1 or 2 apps only and cannot be considered as actual reviews of general public.
# This is demonstrated below:

# In[22]:


for app in free_apps_ios:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# 
# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages, but we'll leave this level of detail for later.
# 
# Reference apps have 74,942 user ratings on average, but it's actually the Bible and Dictionary.com which skew up the average rating:

# In[24]:


for app in free_apps_ios:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# 
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.
# 
# the above idea applies for books genre as well.

# In[ ]:


Now let us considerGoogle play store dataset.


# In[19]:


display_table(free_apps_android, 5) # the Installs columns


# Now calculate average number of app installs per genre for android app dataset.The above range is not accurate but we can be okay with that because we are focus to find which app genres attract more users.
# 
# 
# 

# In[21]:


categories_android = freq_table(free_apps_android, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in free_apps_android:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# On average, communication apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:
# 

# In[26]:


for app in free_apps_android:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# Let's take a look at some of the apps from this genre and their number of installs:

# In[28]:


for app in free_apps_android:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# Let's look at extremely popular apps over here:

# In[30]:



for app in free_apps_android:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# These very popular apps are only few in number, so this market still shows potential.Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[34]:


for app in free_apps_android:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.
# 
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.
# 
# However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

# # Conclusions
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
