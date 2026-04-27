import pandas as pd
import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


edu_df = pd.read_csv("https://ourworldindata.org/grapher/share-of-the-population-with-a-completed-post-secondary-education.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

edu_metadata = requests.get("https://ourworldindata.org/grapher/share-of-the-population-with-a-completed-post-secondary-education.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

income_df= pd.read_csv("https://ourworldindata.org/grapher/economic-inequality-gini-index.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

income_metadata = requests.get("https://ourworldindata.org/grapher/economic-inequality-gini-index.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

gov_df = pd.read_csv("https://ourworldindata.org/grapher/average-learning-outcomes-by-total-education-expenditure-per-capita.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

gov_metadata = requests.get("https://ourworldindata.org/grapher/average-learning-outcomes-by-total-education-expenditure-per-capita.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

inc_edu_df = pd.read_csv('adult.csv')

st.header('Header')
st.subheader('a')

edu_df = edu_df[
    edu_df["Population age 25+ with completed post-secondary education"] != 0]

# Country selector
countries = edu_df["Entity"].unique()
selected_countries = st.multiselect(
    "Select Countries",
    countries)

filtered_df = edu_df[edu_df["Entity"].isin(selected_countries)]
filtered_df = filtered_df.sort_values(["Entity", "Year"])

fig, ax = plt.subplots()

for name, group in filtered_df.groupby("Entity"):
    ax.plot(
        group["Year"],
        group["Population age 25+ with completed post-secondary education"],
        label=name
    )

ax.set_xlabel("Year")
ax.set_ylabel("Population 25+ with Post-Secondary Education")
ax.set_title("Post-Secondary Education Over Time")
ax.legend()

st.pyplot(fig)





# Rename long column
income_df = income_df.rename(columns={
    "gini__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells": "gini"})


# Country selector
selected_countries = st.multiselect(
    "Select Countries",
    income_df["entity"].unique(),
    default=["United States"]
)

# Filter
filtered_income = income_df[
    income_df["entity"].isin(selected_countries)
]

# Create interactive chart
fig = px.line(
    filtered_income,
    x="year",
    y="gini",
    color="entity",
    title="Income Inequality (Gini Index) Over Time",
    labels={
        "year": "Year",
        "gini": "Gini Index",
        "entity": "Country"})

min_year = int(income_df["year"].min())
max_year = int(income_df["year"].max())

year_range = st.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

filtered_income = filtered_income[
    (filtered_income["year"] >= year_range[0]) &
    (filtered_income["year"] <= year_range[1])
]

# Show in Streamlit
st.plotly_chart(fig, use_container_width=True)