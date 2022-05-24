# -*- coding: utf-8 -*-
"""Task.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eE_rYIW5YP4LKSYQchfdBmWmKdn3e9AV

# Sentiment Analysis and Topic modeling for Yelp Reviews using NLP LDA and Gensim Algorithms
**Rationale** This dataset includes all TripAdvisor reviews written in 2015 (through part of 2016) for high review volume Vegas resorts and was collected as part of a large web crawl of over 50 Million online reviews at over 428k worldwide hotels. 

* [Dataset](https://drive.google.com/drive/folders/1nUIOHqvOoF5EkST8u_pMcL7gvKtCy0La?usp=sharing)
    * `vegas2015reviews.csv` contains the reviews 
    * `vegas_venue_info.csv` contains a list of venues in Vegas
    * Note that `gd` is the venue ID in both datasets
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Problem 1: Sentiment Analysis 

## First, let's get to know the dataset.

1. Read in the vegas reviews dataset (call this `df`)
1. Convert any columns that look like dates into Pandas datetime columns.
1. Read in the venue info dataset and merge it with the reviews dataset. (call the resulting dataframe `df`, i.e. write over the old `df`)

Answer the following for the resulting merged dataframe, `df`:
1. How many reviews are there?
1. How many unique hotels are there? Note `gd` is the ID variable for hotels on TripAdvisor.
1. What are the unique types of travel categories?
1. Plot a histogram of the review ratings. How would you describe the overall review ratings on TripAdvisor for Vegas resorts?

## Sentiment 

Use `TextBlob` library to compute the polarity and subjectivity of every review.

1. Compare the histogram of review polarity with review ratings. How are they different? What might you conclude based on this difference about how people rate and how people write?
1. To what degree are polarity and subjectivity correlated with ratings?
1. Use a groupby + corr() statement to calculate the correlation between review ratings and polarity by travel category. In which categories are review polarity most and least correlated with ratings? Any explanation for this relationship?
"""

#Read in the vegas reviews dataset (call this df)

import pandas as pd

review_url = 'https://drive.google.com/file/d/1AIn4VWk7UKHpw6oGgB3KGNVlOY1gsXMs/view?usp=sharing'
review_url='https://drive.google.com/uc?id=' + review_url.split('/')[-2]
df = pd.read_csv(review_url)
df.head()

#Convert any columns that look like dates into Pandas datetime columns.

df['ratingDate'] = pd.to_datetime(df['ratingDate'])
df.head()

df.shape[0]

#Read in the venue info dataset and merge it with the reviews dataset. (call the resulting dataframe df, i.e. write over the old df)

venue_url = 'https://drive.google.com/file/d/18gwz_VmCJpD2d48LoovGNwAY8T_-eTeP/view?usp=sharing'
venue_url = 'https://drive.google.com/uc?id=' + venue_url.split('/')[-2]
df1 = pd.read_csv(venue_url)
#df = pd.concat([df,df1], axis=1, join='inner')
df = df.merge(df1, how='inner', left_on='gd', right_on='gd')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.head()

# How many reviews are there

total_reviews = df.shape[0]
print("Total number of reviews:", total_reviews)

# How many unique hotels are there? Note gd is the ID variable for hotels on TripAdvisor.

unique_hotels = df['gd'].unique()
print("Count of unique hotels:",len(unique_hotels))

# What are the unique types of travel categories
import numpy as np

category = df['travel_category'].unique()
category = np.delete(category, 4)
print("Travel categories:", category)

# Plot a histogram of the review ratings. How would you describe the overall review ratings on TripAdvisor for Vegas resorts?

#overall_ratings=df.groupby('v_name', as_index=False)['reviewrating'].mean()
#vegas_resorts_list=(df.loc[df['v_name'] .str.contains('Vegas') ,'reviewrating']).mean()
overall_ratings = (df['reviewrating'].sum())/(df.shape[0])
#print("Overall review ratings on TripAdvisor for Vegas resorts:",round(vegas_resorts_list,2))
print("Average review ratings on TripAdvisor for Vegas resorts:",round(overall_ratings,2))

hist = df.hist(column='reviewrating', bins=10,grid=False)

"""Number of ratings are pretty high at 4 and 5. So, we can say most of the hotel ratings have attained postive rating."""

import nltk
nltk.download('stopwords')

from textblob import TextBlob
df['polarity'] = df['reviewtext'].map(lambda text: TextBlob(text).sentiment.polarity)
df['subjectivity'] = df['reviewtext'].map(lambda text: TextBlob(text).sentiment.subjectivity)

from textblob import TextBlob

df['polarity'] = df['reviewtext'].map(lambda text: TextBlob(text).sentiment.polarity)
df['subjectivity'] = df['reviewtext'].map(lambda text: TextBlob(text).sentiment.subjectivity)

df.hist(column = 'polarity', bins = 20)
#df.hist(column = 'subjectivity', bins = 20)

"""We see that **polarity score for most of review texts lies in the rangeof [0,0.75]** which means **there are many positive statements.**"""

# Compare the histogram of review polarity with review ratings. 
df.hist(column = 'polarity', by = 'reviewrating',bins=20)

"""From the graph we can see that, **review ratings are mostly aligned with the polarity score for least ratings**. Hotels with review rating 1,2 has polarity in the range [-0.5,0.5] while polarity scores for hotels with review rating 4,5 even has negative/neutral polarity.

We can **infer that people usually feel a need for writting when they are upset** or angry with the service/experience. They feel complaining may give a chance to fix issue. That's why **alignment between least review ratings and polarity is higher.**

On the other hand, **For higher ratings, people don't have a need to write a long intense review that captures the mood of the writer**. They make neutral review about the experience even when they rate the resorts as 4 or 5. That's why **alignment between high review ratings and polarity is neutral in the range of [0,0.7]**
"""

# To what degree are polarity and subjectivity correlated with ratings?
#df.hist(column = 'subjectivity', bins = 20)
review_polarity_corr = df['polarity']. corr(df['reviewrating'])
review_subjectivity_corr = df['subjectivity']. corr(df['reviewrating'])
print("Correlation of Review rating and Polarity:",review_polarity_corr)
print("Correlation of Review rating and subjectivity:",review_subjectivity_corr)

# Use a groupby + corr() statement to calculate the correlation between review ratings and polarity by travel category. 
# In which categories are review polarity most and least correlated with ratings? Any explanation for this relationship?

df.groupby('travel_category')[['reviewrating', 'polarity']].corr()

"""Above result shows that 






**Business and Family category**'s reviews are **highly correlated** 

While **solo and couple category**'s reviews are **less correlated** with polarity and rating.

# Helper Functions
"""

import spacy, time
from gensim.models.ldamulticore import LdaMulticore # this is the multi-core version
from gensim import corpora # import the corpora module
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence
from sklearn.model_selection import train_test_split


def line_doc(filename, encode = 'utf-8'):
    """
    generator function to read in reviews from the file
    and un-escape the original line breaks in the text
    """
    with open(filename, 'r', encoding = encode) as f:
        for txt in f:
            # yield returns next line
            yield txt.replace('\\n', '\n')
            # and get rid of any line breaks

# parsing to be done per sentence
def lemmatize(s, exclude):
    return [w.lemma_.lower() for w in s if (w.lemma_ not in exclude)&(~w.is_punct)]
# next will be a function that will pass a filename to the line_doc function
# and generate the parsed versions of ***EVERY SENTENCE***
# this function streams a file at filename and yields one parsed sentence at a time


def lemmatize_sentence_corpus(filename,nlp, batch_size, n_threads, sw=[], exclusions=[], encode = 'utf-8'):
    nlp.disable_pipes(["ner"]) # disable ner and tagger makes it a little faster
    # batch_size is the number of documents to parse in memory at a time
    # n_threads it the number of parallel (simultaneous processes to run)
    # n_threads is limited by the number of virtual cpu's on the system
    # the default free Colab system has only 2 virtual cores
    # most modern computers have at least 4
    exclude = set(sw + exclusions)
    for parsed_txt in nlp.pipe(line_doc(filename, encode = encode),batch_size=batch_size, n_threads=n_threads):
            for sent in parsed_txt.sents:
                yield ' '.join(lemmatize(sent, exclude))


def write_parsed_sentence_corpus(readfile, writefile, nlp, batch_size, n_threads, sw=[], exclusions =[], encode = 'utf-8'):
    streamingfile = lemmatize_sentence_corpus(readfile,nlp, batch_size, n_threads, sw=sw, exclusions=exclusions, encode = encode)
    with open(writefile, 'w', encoding = encode) as f:
        for sentence in streamingfile:
            if len(sentence)>0: # write sentence if includes non stopwords
                f.write(sentence+'\n')
    print('Success')


def phrase_detection(parsedfile, folderpath, passes = 2, returnmodels = True,threshold=10., encode = 'utf-8'):
    """
    parsedfile is the file location and name of the parsed sentence file
    folderpath is where the models and phrase detected texts need to be stored

    This function does phrase modeling. User specifies the number of passes.
    Each additional pass detects longer phrases. The maximum detectable phrase length for
    each pass, n, is 2^n.
    Returns the list of models by default. Also saves models and intermediary
    phrased sentences for each pass.
    """
    ngram = list()
    for it in range(passes):
        gen = LineSentence(parsedfile)
        gram=Phrases(gen, threshold = threshold)
        ngram.append(gram)
        modelpath = folderpath+'phrase_model_{}.phrasemodel'.format(it+1)
        textpath = folderpath+'sent_gram_{}.txt'.format(it+1)
        gram.save(modelpath)
        # Write sentence n-gram
        with open(textpath, 'w', encoding=encode) as f:
            for sent in gen:
                new_sent = ' '.join(gram[sent])
                f.write(new_sent + '\n')

    if returnmodels == True:
        return ngram


def phrase_prediction(rawfilepath, outpath,nlp, grams, sw =[], exclusions = [], batch_size = 500, n_threads = 2, encode = 'utf-8'):
    """
    rawfilepath is where the raw reviews (where 1 line = 1 review) are saved 
    outpath is where to save the resulting parsed and phrase modeled reviews
    nlp is the spacy parser object
    grams is a list of phrasemodels
    sw is a list of stopwords
    exclusions are additional words to exclude

    """
    with open(outpath, 'w', encoding = encode) as f:
        
        nlp.disable_pipes(["ner"]) # disable ner and tagger makes it a little faster
        exclude = set(sw + exclusions)
        
        for parsed_txt in nlp.pipe(line_doc(rawfilepath, encode = encode),batch_size=batch_size, n_threads=n_threads):
            doc = list()
            for sent in parsed_txt.sents:
                parsed = lemmatize(sent, exclude)
                for gram in grams: # loop through phrase models
                    parsed = gram[parsed] # apply phrase model transformation to sentence
                doc.append(' '.join(parsed).strip()) # append resulting phrase modeled sentence to list "doc"
            # write the transformed review as a single line in the new file
            txt_gram = ' '.join(doc).strip() # join all sentences in doc together as txt_gram
            f.write(txt_gram + '\n') # write the entire phrase modeled and parsed doc as one line in file

"""# 2. Topics in hotel reviews 

## Preprocessing the texts (3)

In this part, you will need to borrow the functions (attached):
1. Create a folder on your google drive to save your NLP files
1. Write a file containing raw reviews.
1. Lemmatize this file into a new file of sentences.
    1. remove stopwords
    1. remove punctuation
    1. Go grab a coffee while this runs. (takes ~10 mins)
1. Apply phrase model twice to identify phrases of up to 4 words in length.
1. Go back to the raw reviews and lemmatize + apply the phrase models at the review level, write the resulting review-level (1 line = 1 review) file to your NLP folder.
    1. Go grab a coffee while this runs. (takes ~10 mins)
1. Create a column in your dataframe called "parsed" that contains the resulting parsed versions of each reviews.
    1. Be sure to save this dataframe so you don't have to start from scratch (can read it in if you come back to the assignment). 
    1. If you come back to this part, make sure that you that you don't delete the outputs from previous session.
1. List the directory of your NLP folder to show that your intermediate steps have been saved.

## LDA model (3)

Apply the LDA model to the parsed reviews 

1. Create a dictionary
1. Filter extreme words in the dictionary
1. Create a corpus of reviews where 1 document = 1 review.
1. Run the LDA for 10-70 topics (inclusive of 70), skipping 10 at a time. (go grab a coffee, this takes ~ 15 minutes)

**How many topics is best in terms of perplexity?**

### Visualize the topics. 

1. Load the best model.
1. Create an LDAVis. (remember you have to `! pip install pyldavis` first)
1. **Pick 3 topics that kind of make sense and describe what they represent.**

### Use LDA to compare pos vs neg reviewers
Imagine you are the marketing director for one of these hotels (pick one of the resorts), **what are the differences in topics mentioned by satisfied and dissatisfied customers?** 
"""

# Create a folder on your google drive to save your NLP files
# Write a file containing raw reviews.
# Load the Drive helper and mount
from google.colab import drive
drive.mount('/content/drive')

import os
os.mkdir("/content/drive/MyDrive/Hotel Reviews NLP1")

# Import PyDrive and associated libraries.
# This only needs to be done once in a notebook.
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authenticate and create the PyDrive client.
# This only needs to be done once in a notebook.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

#Create a Raw reviews file to store a text file.
uploaded = drive.CreateFile({'title': 'Raw_Hotel_Reviews.txt'})
uploaded.SetContentString('')
uploaded.Upload()
print('Uploaded file with ID {}'.format(uploaded.get('id')))

# Create Lemmatised reviews file to store a text file a text file.
uploaded = drive.CreateFile({'title': 'lemmatised_parsed_reviews.txt'})
uploaded.SetContentString('')
uploaded.Upload()
print('Uploaded file with ID {}'.format(uploaded.get('id')))

# Create reviews phrase detection file to store a text file.
uploaded = drive.CreateFile({'title': 'reviews_with_phrase_detection.txt'})
uploaded.SetContentString('')
uploaded.Upload()
print('Uploaded file with ID {}'.format(uploaded.get('id')))

# Create reviews phrase detection file to store a text file.
uploaded = drive.CreateFile({'title': 'phrase_modeled_reviews.txt'})
uploaded.SetContentString('')
uploaded.Upload()
print('Uploaded file with ID {}'.format(uploaded.get('id')))

import numpy as np

lemm_file_path='/content/drive/MyDrive/lemmatised_parsed_reviews.txt'
raw_file_path="/content/drive/MyDrive/Raw_Hotel_Reviews.txt" #raw file path
phrase_detected_file_path='/content/drive/MyDrive/reviews_with_phrase_detection (1).txt'
outpath='/content/drive/MyDrive/phrase_modeled_reviews.txt'
to_write_txt=df['reviewtext']
np.savetxt(raw_file_path, to_write_txt, fmt='%s')

#Lemmatize this file into a new file of sentences.
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
nlp=spacy.load('en_core_web_sm')
write_parsed_sentence_corpus(raw_file_path,lemm_file_path,nlp=nlp,batch_size=1,n_threads=2,sw=stop_words)

#Apply phrase model twice to identify phrases of up to 4 words in length.
phrase_detection(lemm_file_path, phrase_detected_file_path)

#Go back to the raw reviews and lemmatize + apply the phrase models at the review level, write the resulting review-level (1 line = 1 review) file to your NLP folder.
nlp=spacy.load('en_core_web_sm')
reloaded_model1=Phrases.load("/content/drive/MyDrive/reviews_with_phrase_detection.txtphrase_model_1.phrasemodel")
reloaded_model2=Phrases.load("/content/drive/MyDrive/reviews_with_phrase_detection.txtphrase_model_2.phrasemodel")
grams=[reloaded_model1,reloaded_model2]

phrase_prediction(raw_file_path, outpath,nlp, grams=grams,sw =stop_words)

#Create a column in your dataframe called "parsed" that contains the resulting parsed versions of each reviews.
parsed_review=[]
with open(outpath, 'r') as f:
        for sentence in f:
          parsed_review.append(sentence.strip())

df['Parsed']=pd.DataFrame(parsed_review)

df.head(5)

#List file in Hotel Reviews Directory
import os
os.chdir("/content/drive/MyDrive/Hotel Reviews NLP1")
!ls

"""### LDA Model


"""

# Create Dictionary of parsed words
#Filter extreme words in the dictionary

parsed_data=df['Parsed'].tolist()
dict_of_words= corpora.Dictionary(d.split() for d in parsed_data)
print(len(dict_of_words))
dict_of_words.filter_extremes(keep_n=None)
print(len(dict_of_words))

#Create a corpus of reviews where 1 document = 1 review.
split_parsed_review=[d.split() for d in parsed_data]
doc_review_corpus = [dict_of_words.doc2bow(d) for d in split_parsed_review]

#Run the LDA for 10-70 topics (inclusive of 70) skipping 10 at a time
#How many topics is best in terms of perplexity?
perplexity_arr=[]
for k in range(10,71,10):
  LDA_Model= LdaMulticore(doc_review_corpus, id2word=dict_of_words, num_topics=k, per_word_topics=True, chunksize=100, passes=1)
  perplexity_val=LDA_Model.log_perplexity(doc_review_corpus)
  print('\nPerplexity of LDA with ',k, " topics:",perplexity_val) 
  perplexity_arr.append(perplexity_val)

"""Based on running LDA for 10-70 topics with step size of 10, we see that **Perplexity score for 70 topics is the lowest with "-8.254". So, 70 topics can be chosen for building the Best LDA model**"""

#load the best model
Best_lda_model = LdaMulticore(doc_review_corpus, id2word=dict_of_words, num_topics=70, per_word_topics=True, chunksize=100, passes=1)

!pip install pyLDAvis==3.3.0

# Visualize the topics
import pyLDAvis
import pyLDAvis.gensim_models


pyLDAvis.enable_notebook()
LDA_Visualization= pyLDAvis.gensim_models.prepare(Best_lda_model, doc_review_corpus,dict_of_words)
LDA_Visualization
pyLDAvis.save_html(LDA_Visualization, 'LDA_Visualization.html')

"""### **3 Topics from Hotel Reviews Dataset**

Topic 8:

topic 8's some of the frequent terms includes check, charge, pay, bill, extra, fee, wait, long queue, per_night, price, service, internet, $. From this we can infer that **topic 8 is about billing/check-out experience of the users**.

Topic 49:

Some of the frequent terms of topic 49 are mall,taxi, cafe, cabanas, center, south, reasonable_price,position, Pool, cabanas, loungues, cozy,airy. We can understand that **topic 49 is about easily accessible fun and roaming places near hotel.**

Topic 4:

Frequent terms of topic 4 are bathroom, tv, small, lighting, window, open, size, big, spacious, desk, chair. It's explainable that **topic 4 is all about the room and components of room.**

some other topics:
1.   Topic 22 is related to Music and clubbing
2.   Topic 14 is related to hotel location and hospitality

# **Finding Positive and Negative Topics using LDA for Planet Hollywood Resort & Casino**

Considering myself as the Marketing director of 'Planet Hollywood Resort & Casino', I would like to know the positive and negative topics based on reviews of the customer to take appropriate actions in order to improve service and amenities of the resort.

**Initial Try:**

Tried to find positive and negative topics based on all(pos+neg) reviews. Topics generated were more generic. Unable to identify topic that is about root cause of dissatisfaction. So, followed below procedure.

#### **Procedure followed to find topics:**


1.  store resort's reviews as negative and positive based on polarity score in separate dataframes 

2.  Build LDA Model based on categorised dataframes to find 5 main topics from each

3.  Analyse for root cause for satisfaction and dissatisfaction of customers  from topics

4. As the Managing Director, plan on next steps
"""

holly_resort_details=df.loc[df['v_name'] == "Planet Hollywood Resort & Casino"]
holly_resort_details=holly_resort_details[["gd","v_name","ratingDate","reviewrating","reviewtext","Parsed","polarity","subjectivity"]]
holly_resort_details

#Building LDA model 
holly_parsed_data=holly_resort_details['Parsed'].tolist()
holly_dict_of_words= corpora.Dictionary(d.split() for d in holly_parsed_data)
print(len(holly_dict_of_words))
holly_dict_of_words.filter_extremes(keep_n=None)
print(len(holly_dict_of_words))

#Doc2bow--> Convert document (a list of words) into the bag-of-words 
#format = list of (token_id, token_count) 2-tuples. 
#Each word is assumed to be a tokenized and normalized string.

holly_split_parsed_review=[d.split() for d in holly_parsed_data]
holly_doc_review_corpus = [holly_dict_of_words.doc2bow(d) for d in holly_split_parsed_review]

holly_LDA_Model= LdaMulticore(holly_doc_review_corpus, id2word=holly_dict_of_words, num_topics=40, per_word_topics=True, chunksize=100, passes=1)

!pip install pyLDAvis==3.3.0

import pyLDAvis
import pyLDAvis.gensim_models
# Visualize the Negative topics

pyLDAvis.enable_notebook()
holly_LDA_Visualization= pyLDAvis.gensim_models.prepare(holly_LDA_Model, holly_doc_review_corpus,holly_dict_of_words)
holly_LDA_Visualization
pyLDAvis.save_html(holly_LDA_Visualization, 'holly_LDA_Visualization.html')

"""Here are some meaningful topics and the related words from the lot:

**Topic 36: casino**

>frequent words:cool,classy, high-end, ambience

**topic 15:(lamba=0.5) bad reviews about building/maintenance**

>frequent words:dust,rock,understaffed,terrific,carpet,shower-head,loud

**topic 1: Front desk assistance and room service**

> frequent words: front-desk,wait,credit card, hour, house keeping, experiences

**topic 5: amenities of resort and accessible places around resort**
>hotel, music, shopping, lobby, valet-parking

**topic 28: Restaurant service**
> frequent words: food,excellent, buffet, pizza, cashier, drink, bar

### Insights Derived from LDA Model built on Pos+Neg Topics:

Based on some of the topics listed we can say that customers are satisfied with location, quality service of restaurants, casino, spa of the resorts. 

Dissatisfied customers wants to improve room service response time. Other thing they expect/ask is more cleaner rooms and environment.


Topics built by LDA model above didn't capture the main issue that dissatisfied customers had faced. So, digging deeper on next section :)

### Deeper into  Negative and Positive review of Planet HollyWood Resort
So, to dive deeper in the negative and positive topics i am building LDA based on neg and pos reviews alone by separating them based on polarity scores.
"""

#separting negative and pos reviews based on polarity

resort_negative_rev= holly_resort_details[holly_resort_details['polarity'] <= 0.3]
resort_positive_rev = holly_resort_details[holly_resort_details['polarity'] > 0.3 ]

# LDA model to derive 5 topics from Negative reviews
# Reason for choosing num of topics as 5 for LDA modelling: 
# Due to less words in dictionary, extracting 5 topics has good coherence thereby making each topic meaningful and unique 
# thereby helping derive valuable insights

neg_parsed_data=resort_negative_rev['Parsed'].tolist()
neg_dict_of_words= corpora.Dictionary(d.split() for d in neg_parsed_data)
print(len(neg_dict_of_words))
neg_dict_of_words.filter_extremes(keep_n=None)
print(len(neg_dict_of_words))

#Doc2bow--> Convert document (a list of words) into the bag-of-words 
#format = list of (token_id, token_count) 2-tuples. 
#Each word is assumed to be a tokenized and normalized string.

neg_split_parsed_review=[d.split() for d in neg_parsed_data]
neg_doc_review_corpus = [neg_dict_of_words.doc2bow(d) for d in neg_split_parsed_review]

neg_LDA_Model= LdaMulticore(neg_doc_review_corpus, id2word=neg_dict_of_words, num_topics=5, per_word_topics=True, chunksize=100, passes=1)
#neg_LDA_Model.print_topics(num_topics=5, num_words=10)
#neg_LDA_Model.print_topic(topicno=4, topn=10)

# LDA model to derive 5 topics from Positive reviews

pos_parsed_data=resort_positive_rev['Parsed'].tolist()
pos_dict_of_words= corpora.Dictionary(d.split() for d in pos_parsed_data)
print(len(pos_dict_of_words))
pos_dict_of_words.filter_extremes(keep_n=None)
print(len(pos_dict_of_words))

pos_split_parsed_review=[d.split() for d in pos_parsed_data]
pos_doc_review_corpus = [pos_dict_of_words.doc2bow(d) for d in pos_split_parsed_review]

pos_LDA_Model= LdaMulticore(pos_doc_review_corpus, id2word=pos_dict_of_words, num_topics=5, per_word_topics=True, chunksize=100, passes=1)

#!pip install pyLDAvis=3.3.0
# Visualize the Negative topics
import pyLDAvis
import pyLDAvis.gensim_models

pyLDAvis.enable_notebook()
neg_LDA_Visualization= pyLDAvis.gensim_models.prepare(neg_LDA_Model, neg_doc_review_corpus,neg_dict_of_words)
neg_LDA_Visualization
pyLDAvis.save_html(neg_LDA_Visualization, 'neg_LDA_Visualization.html')

"""### **Reviewing Negative Topics**

### Topic/Bubble 5:

**Frequent words:**(with lambda=0.87) 

upgrade, offer, construction, outdated, staff, completely, clean, price, check, look, cigarrette-smoke, manager,rude

It's evident that **this topic is regarding the outlook, maintenance of the hotel and professionalism of staffs.**

**Marketing Director's Point of View:**
Customers look for hotels with friendly, attentive staffs and check-out services. Also, renovated, clean and well maintained bright outlooks appeals customers.


### Topic/Bubble 4:

**Frequent words:**(with lambda=0.4) 

front-desk, 1 hr, nightmare, unacceptable, wait, time, pay, staff, dirty, pool, clean, service, charge,resort_fee

From the frequent words it's evident that this topic is on front desk assistance,room services and checkout experiences. 

**Marketing Director's point of view:**
Rapid room sevices, good hospitality front desk assistance improves customer satisfaction
"""

# Visualize the Positive topics
pyLDAvis.enable_notebook()
pos_LDA_Visualization= pyLDAvis.gensim_models.prepare(pos_LDA_Model, pos_doc_review_corpus,pos_dict_of_words)
pos_LDA_Visualization
pyLDAvis.save_html(pos_LDA_Visualization, 'pos_LDA_Visualization.html')

"""### **Reviewing Positive Topics**

Comig to positive reviews, most of the topics have same frequent words meaning that there are no intense review that users have provided explaining a disappointing/upset situation.

**Topic 1:**

nice, view, location, stay, casino, time, comfortable, clean, recommend,restaurant, eat, music, resort, spa, atmosphere, value, fee

it's obvious that all these are totally happy and satisfied words from the users.

**Marketing director's point of view:**
It's evident that customers are happy with the food,casino, atmosphere,cleanliness, friendly staffs and accessible location of the hotel.

### **Differences in topics mentioned by satisfied and dissatisfied customers**

There are topics where satisfied customers are happy with the resort's cleanliness, accessible location, amenities of the resort like casino, spa, pool, restaurant's food quality and comfortable stay at the resort.

As Per analysis of negative topics, it's observable that customers are not appealed with old outlook and cleanliness of the resort. Also, delay in room service and front desk assistance of staffs disappoints customer's expectations.


####**Suggestions to Management as a Marketing Director:**

As a Marketing Director, my sugestion is to maintain the performace in the areas hotels are performing well already like maintanence of hotels, quality restaurant food , spa, helpful and friendly staffs. 

Adding to that, staffs must be trained to be professional,friendly and can be provided credits/extra bonus for attending customers promptly thereby motivating the staff to attend the customer's issues quickly. Quick response from staffs builds up confidence and satisfaction for customers.

# **Difficulties encountered**

While working on this, I faced very less difficulty . Thanks to Helper functions and clearly laid out steps!

**File creation in Google drive folder from Colab**

This is my first time working on google colab so creating a file in drive's root path worked for me but file creation inside a folder was not working for me. I'm not sure if it's doable! Now, i created everything in my root directory and moved it to desired folder manually.

Would Appretiate your guidance on how to create file in folder using colab Pydrive code! :)

**Finding Fair topic:**

After implementation of LDA, there were many synonymns that were bundled together as a topic that made no sense for a "topic". So, looking for a meaningful topic was time consuming. Enjoyed it though.


**Finding "Right" approach for analysing pos and neg topics:**

Final part of pos and neg topic analysis on *any resort* made me examine attentively on the right approach to do this practise.  

Intially thought, it would be reasonable to generate topics based on all reviews that i had for selected hotel. But, it didn't capture the main problem that dissatisfied customers faced. 

So, i changed the approach by filtering selected hotel's reviews based on polarity score as positive and negative. Then Building LDA model on these small review datasets capured the root cause of dissatisfaction of customers.
"""