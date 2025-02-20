import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Загружаем данные
@st.cache_data
def load_data():
    return pd.read_csv("vacancies_january_2.csv")

df = load_data()

st.title("📊 Аналитика рынка труда")

# Фильтры
city = st.sidebar.selectbox("Выберите город:", ["Все"] + list(df["city"].unique()))
role = st.sidebar.selectbox("Выберите профессию:", ["Все"] + list(df["professional_role"].unique()))

filtered_df = df.copy()
if city != "Все":
    filtered_df = filtered_df[filtered_df["city"] == city]
if role != "Все":
    filtered_df = filtered_df[filtered_df["professional_role"] == role]

# Карта вакансий
st.subheader("🌍 Карта вакансий")
if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:
    fig_map = px.scatter_mapbox(
        filtered_df, 
        lat="latitude", lon="longitude", 
        hover_name="name", 
        hover_data=["salary_from", "salary_currency", "employer_name"], 
        zoom=4
    )
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0, "t":0, "l":0, "b":0}
    )
    st.plotly_chart(fig_map, use_container_width=True)
