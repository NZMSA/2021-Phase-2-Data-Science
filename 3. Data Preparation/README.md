## Software Installations and Prerequisites
You'll need to install the Following Python packages (enter the following commands in your powershell/termial):
```
pip install pandas 
pip install scikit-learn
pip install nltk 
```

## Goal

We are going to process raw text data into a format that the machine learning models can understand. 

## Methods

ML models only understand numbers. There are multiple ways to convert text into numbers. See (https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1194/readings/cs224n-2019-notes01-wordvecs1.pdf)

In this tutorial, we'll look at how to implement one method called TF-IDF (Term Frequency Inverse Document Frequency).

## Step 1: Preprocess the text

Text found in the wild has some features that are not very useful for algorithms. 
Only the most advanced algorithms know how to deal with capitalisation, punctuation, stop words etc. 
So for most besic applications, we clean and preprocess the data by removing these and also remove extrememly common words because those also don't add much value. 
Another thing we can do is to group similar words like develop, developing, developed. This type of thing is called Stemming/Lemmatization which you can look up and learn about.

Check your dataset to see if there are any other things that need to be cleaned. Like html tags, numbers etc. which might make sense to remove based on your task.

## Steps 2: Vectorize

Next, we can pass the cleaned text through a vectorizer. In our case, the TFIDF vectorizer. 
If we see the documentation for the [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html#sklearn.feature_extraction.text.TfidfVectorizer) 
we can see that it has quite a few options available to clean the data as well. If your dataset contains a lot of unique words, it's a good idea to limit the number of words in the vectorizer so that our machine learning models can handle the input size (here we limit the number of features to 2000 words).

Check out [this video](https://www.youtube.com/watch?v=hXNbFNCgPfY) for a more detailed explaination of TF-IDF.


```python
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer

clean_data = pd.read_csv('...')

vectorizer = TfidfVectorizer(lowercase=True,token_pattern=r'(?u)\b[A-Za-z]+\b',stop_words='english',max_features=2000,strip_accents='unicode')
X = vectorizer.fit_transform(clean_data['text_column'].values)
print(vectorizer.get_feature_names())
```

## Review the output

Check the output your model produces.

```python
print(clean_data['text_column'][0])
numbers = pd.DataFrame(vectorizer.transform(clean_data['text_column'][[0]]).toarray())
numbers.T.plot()
```

Congrats, now you have converted the text to numbers that can be put into one of the many machine learning algorithms!
