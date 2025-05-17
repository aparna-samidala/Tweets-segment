import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st.title('Tweet Sentiment Analysis')

st.markdown("This application is all about the tweet sentiment analysis of airlines.We can analyze the reviews of passengers using the streamlit app")

st.sidebar.title('Sentiment analysis of airlines')
st.sidebar.markdown(":airplane: We can analyze the passengers review from this application :airplane:")

file_path = os.path.join(os.path.dirname(__file__), 'Tweets.csv')
data = pd.read_csv(file_path)

if st.checkbox("Show Data"):
     st.write(data.head(100))
     
st.sidebar.subheader("Tweets Analyser")     
tweets=st.sidebar.radio('Sentiment Type',('Positive :heart_eyes:','Negative :disappointed:','Neutral :neutral_face:'))

filtered_data = data.query('airline_sentiment == @tweets')[['text']]
if not filtered_data.empty:
    st.write(filtered_data.sample(1).iat[0, 0])
else:
    st.write("No tweets found for the selected sentiment.")

select=st.sidebar.selectbox('Visualisation Of Tweets', ['Histogram', 'Pie Chart'],key=1)

sentiment=data['airline_sentiment'].value_counts()
sentiment=pd.DataFrame({'Sentiment':sentiment.index, 'Tweets': sentiment.values})
st.markdown("### Sentiment count")
if select == "Histogram":
    fig = px.bar(sentiment, x='Sentiment', y='Tweets', color = 'Tweets', height= 500)
    st.plotly_chart(fig)
else:
    fig = px.pie (sentiment, values= 'Tweets', names= 'Sentiment')
    st.plotly_chart(fig)
    
    
st.sidebar.markdown('Time & Location of tweets')
hr = st.sidebar.slider("Hour of the day", 0, 23)
data['Date'] = pd.to_datetime(data['tweet_created'])
hr_data = data[data['Date'].dt.hour == hr]

import pandas as pd

# Remove rows with missing coordinates
hr_data = hr_data[hr_data['tweet_coord'].notnull()]

# Split 'tweet_coord' into two columns
hr_data[['latitude', 'longitude']] = hr_data['tweet_coord'].apply(
    lambda x: pd.Series(eval(x))
)

if not st.sidebar.checkbox("Hide", True, key='hide_checkbox'):
    st.markdown("### Location of the tweets based on the hour of the day")
    st.markdown("%i tweets during %i:00 and %i:00" % (len(hr_data), hr, (hr+1)%24))
    st.map(hr_data)

st.sidebar.markdown("Airline tweets by sentiment")
choice = st.sidebar.multiselect("Airlines", ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key ='0')
if len(choice)>0:
    air_data=data[data.airline.isin(choice)]
    fig1 = px.histogram(air_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig1)