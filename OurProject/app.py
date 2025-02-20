import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

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

# --- 2. Карта вакансий ---
st.subheader("🌍 Карта вакансий")
m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=5)
for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['name']} - {row['salary_from']} {row['salary_currency']}",
    ).add_to(m)
st_folium(m, width=700, height=500)

# --- 3. Распределение зарплат ---
st.subheader("💰 Распределение зарплат")
fig2 = px.histogram(filtered_df, x="salary_from", nbins=20, title="Распределение вакансий по зарплатам", color_discrete_sequence=['blue'])
st.plotly_chart(fig2)

# --- 4. Доля типов занятости ---
st.subheader("📌 Типы занятости")
employment_counts = filtered_df["employment_type"].value_counts().reset_index()
fig3 = px.pie(employment_counts, names="index", values="employment_type", title="Доля типов занятости")
st.plotly_chart(fig3)

# --- 5. Требуемый опыт работы ---
st.subheader("🎯 Требуемый опыт работы")
experience_counts = filtered_df["experience"].value_counts().reset_index()
fig4 = px.pie(experience_counts, names="index", values="experience", title="Распределение по опыту работы")
st.plotly_chart(fig4)

# --- 6. Топ-10 работодателей по количеству вакансий ---
st.subheader("🏢 Топ-10 работодателей по количеству вакансий")
top_employers = df["employer_name"].value_counts().nlargest(10).reset_index()
fig5 = px.bar(top_employers, x="index", y="employer_name", title="Топ-10 работодателей", color="employer_name")
st.plotly_chart(fig5)
