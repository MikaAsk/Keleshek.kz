import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Загружаем данные
@st.cache_data
def load_data():
    return pd.read_csv("vacancies_january_2.csv")

df = load_data()

# --- Фильтры ---
st.sidebar.header("Фильтры")
city = st.sidebar.selectbox("Выберите город:", ["Все"] + list(df["city"].unique()))
role = st.sidebar.selectbox("Выберите профессию:", ["Все"] + list(df["professional_role"].unique()))

filtered_df = df.copy()
if city != "Все":
    filtered_df = filtered_df[filtered_df["city"] == city]
if role != "Все":
    filtered_df = filtered_df[filtered_df["professional_role"] == role]

# Удаляем строки с пустыми координатами
filtered_df = filtered_df.dropna(subset=["latitude", "longitude"])

# --- Зарплатная аналитика ---
st.subheader("💰 Зарплатная аналитика")
fig_salary = px.box(filtered_df, x="professional_role", y="salary_from", points="all", title="Диапазон зарплат по профессиям")
st.plotly_chart(fig_salary)

# --- Востребованность профессии ---
st.subheader("📈 Востребованность профессии")
fig_demand = px.bar(filtered_df["professional_role"].value_counts().reset_index(), x="index", y="professional_role", title="Количество вакансий по профессиям")
st.plotly_chart(fig_demand)

# --- Требования работодателей ---
st.subheader("📌 Требования работодателей")
fig_experience = px.pie(filtered_df["experience"].value_counts().reset_index(), names="index", values="experience", title="Требуемый опыт работы")
st.plotly_chart(fig_experience)

# --- География вакансий ---
st.subheader("🌍 География вакансий")
fig_map = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", hover_name="name", zoom=4, height=500)
fig_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_map)

# --- Карьерные перспективы ---
st.subheader("🚀 Карьерные перспективы")
fig_career = px.bar(filtered_df.groupby("professional_role")["salary_from"].mean().reset_index(), x="professional_role", y="salary_from", title="Средняя зарплата по профессиям")
st.plotly_chart(fig_career)
