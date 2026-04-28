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


st.header('Factors of Education')
st.subheader('Interactive Charts')

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

st.header('Analysis')
st.subheader('There is an obvious positive relationship between time and the percentage of people with post-secondary education. It is important to highlight select countries. Russia has the highest percentage out of all countries accoridng to the data. China has a lower percentage compared to the United States')






# Rename long column
income_df = income_df.rename(columns={
    "gini__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells": "gini"
})

# Make numeric + remove 0s
income_df["gini"] = pd.to_numeric(income_df["gini"], errors="coerce")
income_df = income_df[(income_df["gini"] != 0) & (income_df["gini"].notna())]

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
        "entity": "Country"
    }
)

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

st.header('Analysis')
st.header('After assessing multiple countries, each country has their own trend. This can be based on the political decisions of their leaders. ')








st.title("Test Scores vs Government Education Spending")

# Clean data
plot_df = gov_df.dropna(subset=[
    "government_expenditure_on_education__constant_pppdollar__millions",
    "harmonized_test_scores__sex_all_students"
])

# Optional: Region filter
regions = st.multiselect(
    "Select Region(s)",
    options=plot_df["owid_region"].unique(),
    default=plot_df["owid_region"].unique()
)

plot_df = plot_df[plot_df["owid_region"].isin(regions)]

# Optional: Year slider
year_range = st.slider(
    "Select Year Range",
    int(plot_df["year"].min()),
    int(plot_df["year"].max()),
    (int(plot_df["year"].min()), int(plot_df["year"].max()))
)

plot_df = plot_df[
    (plot_df["year"] >= year_range[0]) &
    (plot_df["year"] <= year_range[1])
]




plot_df = plot_df.sort_values("year")
plot_df = plot_df.groupby("entity").tail(1)


# Create interactive scatter plot
fig = px.scatter(
    plot_df,
    x="government_expenditure_on_education__constant_pppdollar__millions",
    y="harmonized_test_scores__sex_all_students",
    color="owid_region",
    hover_name="entity",
    title="Test Scores vs Government Spending",
    labels={
        "government_expenditure_on_education__constant_pppdollar__millions": "Gov Spending (PPP, millions)",
        "harmonized_test_scores__sex_all_students": "Harmonized Test Scores"
    }
)

plot_df = (
    plot_df
    .groupby("entity", as_index=False)
    .agg({
        "government_expenditure_on_education__constant_pppdollar__millions": "mean",
        "harmonized_test_scores__sex_all_students": "mean",
        "owid_region": "first"
    })
)


st.plotly_chart(fig, use_container_width=True)

df = pd.read_csv('tableA1(tableA1) (1).csv')



