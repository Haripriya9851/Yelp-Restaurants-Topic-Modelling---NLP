# Yelp-Restaurants-Topic-Modelling---NLP

Using NLP based LDA-Gensim Topic modelling Algorithm to categorize Yelp restaurant reviews for prescriptive analysis for the hotel management.
**code:** [LDA Topic Modelling Code](https://github.com/Haripriya9851/Yelp-Restaurants-Topic-Modelling---NLP/blob/main/Sentiment%20Analysis%20and%20Topic%20Modeling%20using%20NLP.ipynb)


# Comparison of Review Polarity with Review Ratings 

**Review ratings are mostly aligned with the polarity score for least ratings.** Hotels with review rating 1,2 has polarity in the range [-0.5,0.5] while polarity scores for hotels with review rating 4,5 even has negative/neutral polarity.

**We can infer that people usually feel a need for writting when they are upset or angry with the service/experience.** They feel complaining may give a chance to fix issue. That's why alignment between least review ratings and polarity is higher.

On the other hand, **For higher ratings, people don't have a need to write a long intense review that captures the mood of the writer.** They make neutral review about the experience even when they rate the resorts as 4 or 5. That's why alignment between high review ratings and polarity is neutral in the range of [0,0.7]

# LDA Topic Model Result Analysis:
## 3 Topics from Hotel Reviews Dataset
**Topic 8:** topic 8's some of the frequent terms includes check, charge, pay, bill, extra, fee, wait, long queue, per_night, price, service, internet, $. From this we can infer that topic 8 is about billing/check-out experience of the users.

**Topic 49:** Some of the frequent terms of topic 49 are mall,taxi, cafe, cabanas, center, south, reasonable_price,position, Pool, cabanas, loungues, cozy,airy. We can understand that topic 49 is about easily accessible fun and roaming places near hotel.

**Topic 4:** Frequent terms of topic 4 are bathroom, tv, small, lighting, window, open, size, big, spacious, desk, chair. It's explainable that topic 4 is all about the room and components of room.

**some other topics:**
- Topic 22 is related to Music and clubbing
- Topic 14 is related to hotel location and hospitality

# Finding Positive and Negative Topics using LDA for Planet Hollywood Resort & Casino


Coming to positive reviews, most of the topics have same frequent words meaning that there are no intense review that users have provided explaining a disappointing/upset situation.

## Topic/Bubble 1: Reviewing Positive Topics

Frequent words: nice, view, location, stay, casino, time, comfortable, clean, recommend,restaurant, eat, music, resort, spa, atmosphere, value, fee

it's obvious that all these are totally happy and satisfied words from the users.

**Marketing director's point of view:** It's evident that customers are happy with the food,casino, atmosphere,cleanliness, friendly staffs and accessible location of the hotel.

## Topic/Bubble 5: Reviewing Negative Topics
Frequent words(with lambda=0.87) :upgrade, offer, construction, outdated, staff, completely, clean, price, check, look, cigarrette-smoke, manager,rude

It's evident that this topic is regarding the outlook, maintenance of the hotel and professionalism of staffs.

**Marketing Director's Point of View:** Customers look for hotels with friendly, attentive staffs and check-out services. Also, renovated, clean and well maintained bright outlooks appeals customers.

## Topic/Bubble 4: Reviewing Negative Topics
Frequent words:(with lambda=0.4)

front-desk, 1 hr, nightmare, unacceptable, wait, time, pay, staff, dirty, pool, clean, service, charge,resort_fee

From the frequent words it's evident that this topic is on front desk assistance,room services and checkout experiences.

**Marketing Director's point of view:** Rapid room sevices, good hospitality front desk assistance improves customer satisfaction
### Differences in topics mentioned by satisfied and dissatisfied customers

There are topics where satisfied customers are happy with the resort's cleanliness, accessible location, amenities of the resort like casino, spa, pool, restaurant's food quality and comfortable stay at the resort.

As Per analysis of negative topics, it's observable that customers are not appealed with old outlook and cleanliness of the resort. Also, delay in room service and front desk assistance of staffs disappoints customer's expectations.

## Suggestions to Management as a Marketing Director:

As a Marketing Director, my sugestion is to maintain the performace in the areas hotels are performing well already like maintanence of hotels, quality restaurant food , spa, helpful and friendly staffs.

Adding to that, staffs must be trained to be professional,friendly and can be provided credits/extra bonus for attending customers promptly thereby motivating the staff to attend the customer's issues quickly. Quick response from staffs builds up confidence and satisfaction for customers.

# Difficulties encountered

While working on this, I faced very less difficulty . 

1. **File creation in Google drive folder from Colab** : This is my first time working on google colab so creating a file in drive's root path worked for me but file creation inside a folder was not working for me. I'm not sure if it's doable! Now, i created everything in my root directory and moved it to desired folder manually. Would Appretiate your guidance on how to create file in folder using colab Pydrive code! :)

2. **Finding Fair topic:** After implementation of LDA, there were many synonymns that were bundled together as a topic that made no sense for a "topic". So, looking for a meaningful topic was time consuming. Enjoyed it though.

3. **Finding "Right" approach for analysing pos and neg topics:** Final part of pos and neg topic analysis on any resort made me examine attentively on the right approach to do this practise. Intially thought, it would be reasonable to generate topics based on all reviews that i had for selected hotel. But, it didn't capture the main problem that dissatisfied customers faced.

So, i changed the approach by filtering selected hotel's reviews based on polarity score as positive and negative. Then Building LDA model on these small review datasets capured the root cause of dissatisfaction of customers.
