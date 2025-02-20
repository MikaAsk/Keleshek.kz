import streamlit as st
import pandas as pd
import plotly.express as px

# Загружаем данные
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# Фильтры
city = st.selectbox("Выберите город:", df["city"].unique())

# Фильтруем данные
filtered_df = df[df["city"] == city]

# Визуализация
fig = px.histogram(filtered_df, x="salary_from", nbins=20, title="Распределение зарплат")
st.plotly_chart(fig)

st.write("Данные по вакансиям:")
st.dataframe(filtered_df)
