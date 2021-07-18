

<div align="center" style="display:flex">
    <img width="200px" src="https://user-images.githubusercontent.com/41566813/126031976-64662e14-d20b-4aa7-9499-210c6834bb48.png"/>
    <h1>Data Extraction Example</h1>

</div>

Congrats on finishing MSA phase 1 data science 😃. In this section we are going to create a web crawler to extract the reviews from IMDB with python, beautifulsoup, and requests. <br>


## Overview

- [Software Installations and Prerequisites](#software-installations-and-prerequisites)
- [Goal](#goal)
- [Steps](#steps)
    - [Step 0 - Analyse URL](#step-0-analyse-url)
    - [Step 1 - Make a request](#step-1-make-a-request)
    - [Step 2 - Get Individual Movie](#step-2-get-individual-movie)
    - [Step 3 - Extract Review Links](#step-3-extract-review-links)
    - [Step 4 - Get Individual Review](#step-4-get-individual-review-for-each-movie)
    - [Step 5 - Get the review text and title then store the text into .csv file](#step-5-get-the-review-text-and-title-then-store-the-text-into-csv-file)
- [Note](#note)
<hr>

## Software Installations and Prerequisites
1. Python
2. Make sure pip is installed in your computer. Check [Workshop 1]("https://github.com/NZMSA/2021-introduction-to-data-science/tree/main/Data%20Preparation/slides") for how to install pip
3. Enter the following command in your powershell/termial:
```
pip install beautifulsoup4 
pip install requests
pip install pandas 
```
Note for MacOS if above doesn't work try ```pip3 install```<br>

## Goal
So what is our goal in this case? It is about movie reviews. <br>
We are going to extract the reviews from [IMDB](https://www.imdb.com/) **top 100** movies. 

# Steps
Below is one way to get movie reviews, there are many other ways but the main idea would be similar. 
## Step 0. Analyse URL
When we do web crawling, it is important to understand the URL and the website you are crawling from. <br>
In this case we are looking at the top 100 movies from IMDB, and we will use the IMDB advanced search function ```https://www.imdb.com/search/title/``` to get our criterias. <br>
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126056285-449b9bbf-abca-4756-bd42-8720a48743b2.png"/><br>
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126056330-26f4c3ec-d86d-4552-9e18-4485730a7c51.png"/><br>
As shown above the IMDB advanced search function has a lot of options. In our example we just need our result to be **feature film, IMDB top 100, disply 100 per page and sorted by user rating descending**.
Once we click search, the URL should be ```https://www.imdb.com/search/title/?title_type=feature&groups=top_100&sort=user_rating,desc&count=100```
<br>
We can use this URL to make requests and get responses. But the response will be a HTML page. So we need ```beautifulsoup``` to extract the page of each movie. 
<br>

## Step 1. Make a request
Now we sorted the URL, we gonna write some codes!<br>
First we need to import the packages we pip installed. <br>
```python
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import itertools
```
Now we are going to make use of requests and beautifulsoup to make a request to our target URL. It would simply be the following:
```python
url = '''https://www.imdb.com/search/title/?title_type=feature&groups=top_100&sort=user_rating,desc&count=100'''
response = requests.get(url)
movies_soup = BeautifulSoup(response.text, 'html.parser')
```
Now if you ```print(movies_soup)``` you will see a bunch of HTML stuff. It means we got the page successfully. Yay🥳!

## Step 2. Get individual movie
We have the response now, let's try to get the link of each movie. If we right click on the ```https://www.imdb.com/search/title/?title_type=feature&groups=top_100&sort=user_rating,desc&count=100``` page then click inspect or press F12 we should see the following:
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126061390-c58119a5-ef7f-4e9d-8637-f1a871451e7e.png"/><br>
Don't get overwhlemed by this, we just need to observe the pattern of the title links. <br>
Click the top right corner of the inspect box:<br>
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126061472-3bc50d0b-159e-4c4b-bcb4-19966b75cf11.png"/><br>
Then move ur cursor to any of the movie title. You would see something like this:
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126061499-d48b254f-e9aa-4e9e-b954-9e1fcb5048e9.png"/><br>
With this we are able to see what the movie title is link to <br>
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126061613-154dd952-f010-4aab-8816-f9378fe6972f.png"/><br>
<br>
Now we got one link, if we look at other movie links we would find a pattern. That is all the links are ```<a>``` tag with no ```class``` and they start with ```/title``` and end with ```?ref_=adv_li_tt``` <br>
Note that in our codes we need to implement as they end with ```/```, because the ```?ref_=adv_li_tt``` is the Referral and we will not get it with our crawler. <br>
If you are interested in why they put it there, here is a [LINK](https://stackoverflow.com/questions/21457548/why-put-ref-in-url)<br>

So the code would be:
```python
# Get all the <a> tag without a class
movie_tags = movies_soup.find_all('a', attrs={'class': None})
# Filter the a-tags to get just the titles
movie_tags = [tag.attrs['href'] for tag in movie_tags 
              if tag.attrs['href'].startswith('/title') & tag.attrs['href'].endswith('/')]
# Remove duplicate links
movie_tags = list(dict.fromkeys(movie_tags))

print("In total we have " + str(len(movie_tags)) + " movie titles") # Comment out afterwards
print("Displaying 10 titles") # Comment out afterwards
print(movie_tags[:10]) # Comment out afterwards
```

The output should be:
```
There are a total of 100 movie titles
Displaying 10 titles
['/title/tt0111161/', '/title/tt0068646/', '/title/tt0468569/', '/title/tt0071562/', '/title/tt0050083/', '/title/tt0167260/', '/title/tt0110912/', '/title/tt0108052/', '/title/tt1375666/', '/title/tt0137523/']
```

## Step 3. Extract review links
Now for each movie we want to extra their review links.<br>
Again like what we did in step 2 we inspect the page to find the the user revies. It looks like the following:<br>
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126062993-c64291a7-5b0f-4dc7-9bc6-891d90891461.png"/><br>
To get those links in our code, it looks like the following:
```python
base_url = "https://www.imdb.com"
# Get movie links with reviews
movie_links = [base_url + tag + 'reviews' for tag in movie_tags]
print("In total we have " + str(len(movie_links)) + " movie user reviews") # Comment out afterwards
print("Displaying 10 user reviews links") # Comment out afterwards
print(movie_links[:10]) # Comment out afterwards
```
And the output should look like this:
```
There are a total of 100 movie user reviews
Displaying 10 user reviews links['https://www.imdb.com/title/tt0111161/reviews', 'https://www.imdb.com/title/tt0068646/reviews', 'https://www.imdb.com/title/tt0468569/reviews', 'https://www.imdb.com/title/tt0071562/reviews', 'https://www.imdb.com/title/tt0050083/reviews', 'https://www.imdb.com/title/tt0167260/reviews', 'https://www.imdb.com/title/tt0110912/reviews', 'https://www.imdb.com/title/tt0108052/reviews', 'https://www.imdb.com/title/tt1375666/reviews', 'https://www.imdb.com/title/tt0137523/reviews']
```

## Step 4. Get individual review for each movie
Now any of the output link in step 3 should look similar to the screenshot below:<br>
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126063927-292ab7ce-e89b-4654-9917-791e545f4afa.png"/><br>
And again we want to get a single review link, we need to find the pattern. <br>
Notice all the review links have a ```class=title"```, we can then get those links with the following codes:<br>

### This takes a while because we need to access to every movie with beautifulsoup<br>
```python
# Create a helper function to get review links
def getReview(soup):
    # Get all the review tags
    user_review_list = soup.find_all('a', attrs={'class':'title'})
    # Get the first review tag
    review_tag = user_review_list[0]
    # Return the none review link
    review_link = "https://www.imdb.com" + review_tag['href']
    return review_link

# Get a list of soup objects. This takes a while
movie_review_soups = [BeautifulSoup(requests.get(link).text, 'html.parser') for link in movie_links]
# Get all 100 movie review links
movie_review_list = [getReview(movie_review_soup) for movie_review_soup in movie_review_soups]

print("There are a total of " + str(len(movie_review_list)) + " individual movie reviews") # Comment out afterwards
print("Displaying 10 reviews") # Comment out afterwards
print(movie_review_list[:10]) # Comment out afterwards
```
In this code, the helper function getReview(soup) takes a soup object (each movie page), and it will get all the reviews in that page, and then select the first review. (It could be any, we just use the first as an example).<br>
Outside the helper function, the code first get all the soups with the movie links we had before. This step takes a long time as beautifulsoup need to access to those movie pages, each takes around one second. Then for each of those movies, we extract the review link with helper function. <br>
After around 100 seconds, we would get something similar to this:
```
There are a total of 100 individual movie reviews
Displaying 10 reviews
['https://www.imdb.com/review/rw0349418/', 'https://www.imdb.com/review/rw3038370/', 'https://www.imdb.com/review/rw6457886/', 'https://www.imdb.com/review/rw5049900/', 'https://www.imdb.com/review/rw4728061/', 'https://www.imdb.com/review/rw3379367/', 'https://www.imdb.com/review/rw6261036/', 'https://www.imdb.com/review/rw0328197/', 'https://www.imdb.com/review/rw4692192/', 'https://www.imdb.com/review/rw5006989/']
```

## Step 5. Get the review text and title then store the text into .csv file
Now we get all the reviews we want, we just need a way to get the text and title!<br>
And again, we observe the page and find out the text always have a ```class="text show-more__control"```, and title is always in a ```<h1 class="header">```. Shown as following:<br>
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126064964-64de6f49-0134-4aa8-9691-55a522a0f9b1.png"/>
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126065070-ad124857-82a5-4e36-bd3c-1b2ffa262f6a.png"/>

The code for this would be:
```python
# Create lists for dataframe and csv later
review_texts = []
movie_titles = []

# Loop through the movie reviews
for url in movie_review_list:
    # Get the review page
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    # Find div tags with class text show-more__control, then get its text
    review_tag = soup.find('div', attrs={'class': 'text show-more__control'}).getText()
    # Add the review text in the review list
    review_texts += [review_tag]
    # Find the h1 tag and get the second element i.e. the title
    title_tag = list(soup.find('h1').children)[1].getText()
    # Add the title in the title list
    movie_titles += [title_tag]
```
We construct two list for later use, then we run a for loop of the movie review url to get review text and movie title. We then add those two values into the list we created initially.<br>
The output would be similar to this:

```
['The Shawshank Redemption', ...]
Why do I want to write the 234th comment on The Shawshank Redemption? I am....
```
<br>
Finally we will convert the list into a dataframe so that we can put it into a .csv file.<br>
We will use pandas! It looks like the following:

```python
# Construct a dataframe
df = pd.DataFrame({'movie': movie_titles, 'user_review_permalink': movie_review_list,'user_review': review_texts})
# Put into .csv file
df.to_csv('userReviews.csv', index=False)
```
Now there should be a .csv file called userReviews.csv under the root folder, and it should look similar to this:
<img width="500px" src="https://user-images.githubusercontent.com/41566813/126066389-4349195b-a42d-45c4-9754-8d2b203639c6.png"/>

ANND that is the end, we now get all the data into a nice format and you can start your next chapter : )
## Note
This is just an example of how to use web crawling to get data. There are different ways to achieve the same result<br>
For MSA assesment, the steps would be slightly different so please undestand the process first and then try to implement the solution. <br>
When crawling please be careful so that you are not spamming the website. <br>

You might find the [beautifulsoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) come in handly when doing ur assesment!

ALl the best and feel free to ask any questions 😃!
