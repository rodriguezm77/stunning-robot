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



st.header('Factors of Education')
st.subheader('Interactive Charts')

edu_df = edu_df[
    edu_df["Population age 25+ with completed post-secondary education"] != 0]


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




income_df = income_df.rename(columns={
    "gini__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells": "gini"})

income_df["gini"] = pd.to_numeric(income_df["gini"], errors="coerce")
income_df = income_df[(income_df["gini"] != 0) & (income_df["gini"].notna())]


selected_countries = st.multiselect(
    "Select Countries",
    income_df["entity"].unique())


filtered_income = income_df[
    income_df["entity"].isin(selected_countries)]


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
    (filtered_income["year"] <= year_range[1])]

st.plotly_chart(fig, use_container_width=True)

st.header('Analysis')
st.header('After assessing multiple countries, each country has their own trend. This can be based on the political decisions of their leaders. ')








st.title("Test Scores vs Government Education Spending")

plot_df = gov_df.dropna(subset=[
    "government_expenditure_on_education__constant_pppdollar__millions",
    "harmonized_test_scores__sex_all_students"
])


regions = st.multiselect(
    "Select Region(s)",
    options=plot_df["owid_region"].unique(),
    default=plot_df["owid_region"].unique()
)

plot_df = plot_df[plot_df["owid_region"].isin(regions)]


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



fig = px.scatter(
    plot_df,
    x="government_expenditure_on_education__constant_pppdollar__millions",
    y="harmonized_test_scores__sex_all_students",
    color="owid_region",
    hover_name="entity",
    title="Test Scores vs Government Spending",
    labels={
        "government_expenditure_on_education__constant_pppdollar__millions": "Gov Spending (millions)",
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
    }))


st.plotly_chart(fig, use_container_width=True)



st.header('Analysis')
st.subheader('In conclusion, while total government spending on education is a critical factor in shaping educational systems, it does not automatically translate into improved average learning outcomes. This analysis underscores the necessity of not only increasing funding but also ensuring that resources are allocated effectively to enhance teaching quality and address the diverse needs of students. As we move forward, it is essential to adopt a holistic approach that prioritizes strategic investments in education, fostering an environment where every student can succeed. Ultimately, the goal should be to create a system where financial resources are matched by innovative practices that truly enhance learning experiences and outcomes for all learners')



combine_gov_inc_df = gov_df.merge(
    income_df,
    on=['entity', 'code', 'year'],
    how='inner')





st.set_page_config(layout="wide")

st.title("Education Spending, Inequality, and Test Scores Dashboard")


gov_df = gov_df.copy()
income_df = income_df.copy()

# Remove duplicates
gov_df = gov_df.drop_duplicates(subset=["entity", "year"])
income_df = income_df.drop_duplicates(subset=["entity", "year"])

# Merge datasets
combined_df = pd.merge(
    gov_df,
    income_df[["entity", "code", "year", "gini"]],
    on=["entity", "code", "year"],
    how="inner"
)

# Drop missing key values
combined_df = combined_df.dropna(subset=[
    "harmonized_test_scores__sex_all_students",
    "government_expenditure_on_education__constant_pppdollar__millions",
    "gini"
])

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=sorted(combined_df["owid_region"].dropna().unique()),
    default=sorted(combined_df["owid_region"].dropna().unique())
)

filtered_df = combined_df[combined_df["owid_region"].isin(regions)]

year = st.sidebar.slider(
    "Select Year",
    min_value=int(filtered_df["year"].min()),
    max_value=int(filtered_df["year"].max()),
    value=int(filtered_df["year"].max())
)

year_df = filtered_df[filtered_df["year"] == year]

# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------
col1, col2 = st.columns(2)

# ---------------------------------------------------
# 1️⃣ SPENDING VS TEST SCORES
# ---------------------------------------------------
with col1:
    st.subheader(f"Spending vs Test Scores ({year})")

    fig1 = px.scatter(
        year_df,
        x="government_expenditure_on_education__constant_pppdollar__millions",
        y="harmonized_test_scores__sex_all_students",
        color="owid_region",
        hover_name="entity",
        trendline="ols",
        labels={
            "government_expenditure_on_education__constant_pppdollar__millions":
                "Gov Spending (PPP $ Millions)",
            "harmonized_test_scores__sex_all_students":
                "Test Scores"
        }
    )

    st.plotly_chart(fig1, use_container_width=True)

    corr1 = year_df[
        ["government_expenditure_on_education__constant_pppdollar__millions",
         "harmonized_test_scores__sex_all_students"]
    ].corr().iloc[0, 1]

    st.metric("Correlation", round(corr1, 3))

# ---------------------------------------------------
# 2️⃣ GINI VS TEST SCORES
# ---------------------------------------------------
with col2:
    st.subheader(f"Gini vs Test Scores ({year})")

    fig2 = px.scatter(
        year_df,
        x="gini",
        y="harmonized_test_scores__sex_all_students",
        color="owid_region",
        hover_name="entity",
        trendline="ols",
        labels={
            "gini": "Gini Index",
            "harmonized_test_scores__sex_all_students": "Test Scores"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)

    corr2 = year_df[
        ["gini",
         "harmonized_test_scores__sex_all_students"]
    ].corr().iloc[0, 1]

    st.metric("Correlation", round(corr2, 3))

# ---------------------------------------------------
# 3️⃣ COUNTRY TREND OVER TIME
# ---------------------------------------------------
st.subheader("Country Trends Over Time")

country = st.selectbox(
    "Select a Country",
    sorted(filtered_df["entity"].unique())
)

country_df = filtered_df[filtered_df["entity"] == country]

fig3 = px.line(
    country_df,
    x="year",
    y=[
        "harmonized_test_scores__sex_all_students",
        "government_expenditure_on_education__constant_pppdollar__millions",
        "gini"
    ],
    labels={"value": "Value", "variable": "Metric"}
)

st.plotly_chart(fig3, use_container_width=True)