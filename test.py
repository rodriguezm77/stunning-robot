import pandas as pd
import streamlit as st
import requests


edu_df = pd.read_csv("https://ourworldindata.org/grapher/share-of-the-population-with-a-completed-post-secondary-education.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
edu_metadata = requests.get("https://ourworldindata.org/grapher/share-of-the-population-with-a-completed-post-secondary-education.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

# Fetch the data.
income_df= pd.read_csv("https://ourworldindata.org/grapher/economic-inequality-gini-index.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
income_metadata = requests.get("https://ourworldindata.org/grapher/economic-inequality-gini-index.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

# Fetch the data.
gov_df = pd.read_csv("https://ourworldindata.org/grapher/average-learning-outcomes-by-total-education-expenditure-per-capita.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
gov_metadata = requests.get("https://ourworldindata.org/grapher/average-learning-outcomes-by-total-education-expenditure-per-capita.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

inc_edu_df = pd.read_csv('adult.csv')
inc_edu_df