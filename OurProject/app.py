import streamlit as st
import pandas as pd
import plotly.express as px

# Настройка страницы
st.set_page_config(page_title="Аналитика рынка труда", layout="centered")

# Загружаем данные
@st.cache_data
def load_data():
    return pd.read_csv("vacancies_january_2.csv")

df = load_data()

# --- Фильтры ---
st.sidebar.header("🔍 Фильтры")
city = st.sidebar.selectbox("🏙️ Выберите город:", ["Все"] + list(df["city"].dropna().unique()))
role = st.sidebar.selectbox("💼 Выберите профессию:", ["Все"] + list(df["professional_role"].dropna().unique()))

filtered_df = df.copy()
if city != "Все":
    filtered_df = filtered_df[filtered_df["city"] == city]
if role != "Все":
    filtered_df = filtered_df[filtered_df["professional_role"] == role]

# Удаляем строки с пустыми координатами
filtered_df = filtered_df.dropna(subset=["latitude", "longitude"])

# --- Основная часть страницы ---
st.title("📊 Аналитика рынка труда")

# --- Карта вакансий ---
st.markdown("## 🌍 Карта вакансий")

if not filtered_df.empty:
    fig_map = px.scatter_mapbox(
        filtered_df, 
        lat="latitude", lon="longitude", 
        hover_name="name", 
        hover_data=["salary_from", "salary_currency", "employer_name"], 
        zoom=4, height=500
    )
    fig_map.update_layout(
        mapbox_style="open-street-map", 
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)", 
        font=dict(size=14)
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("⚠️ Нет данных с координатами для отображения карты.")

# --- Распределение зарплат ---
st.markdown("## 💰 Распределение зарплат")

fig_salary = px.histogram(
    filtered_df, 
    x="salary_from", 
    nbins=20, 
    title="Распределение вакансий по зарплатам", 
    color_discrete_sequence=['#1f77b4']
)
fig_salary.update_layout(
    bargap=0.2, 
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(size=14)
)
st.plotly_chart(fig_salary, use_container_width=True)

# --- Доля типов занятости ---
st.markdown("## 📌 Типы занятости")

employment_counts = filtered_df["employment_type"].value_counts().reset_index()
employment_counts.columns = ["employment_type", "count"]

fig_employment = px.pie(
    employment_counts, 
    names="employment_type", 
    values="count", 
    title="Доля типов занятости",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_employment.update_traces(textinfo="percent+label")
st.plotly_chart(fig_employment, use_container_width=True)

# --- Требуемый опыт работы ---
st.markdown("## 🎯 Требуемый опыт работы")

experience_counts = filtered_df["experience"].value_counts().reset_index()
experience_counts.columns = ["experience", "count"]

fig_experience = px.pie(
    experience_counts, 
    names="experience", 
    values="count", 
    title="Распределение по опыту работы",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig_experience.update_traces(textinfo="percent+label")
st.plotly_chart(fig_experience, use_container_width=True)

# --- Топ-10 работодателей ---
st.markdown("## 🏢 Топ-10 работодателей")

top_employers = df["employer_name"].value_counts().nlargest(10).reset_index()
top_employers.columns = ["employer_name", "count"]

fig_employers = px.bar(
    top_employers, 
    x="employer_name", 
    y="count", 
    title="Топ-10 работодателей по количеству вакансий", 
    color="employer_name",
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig_employers.update_layout(
    xaxis_title="Работодатель", 
    yaxis_title="Количество вакансий",
    xaxis_tickangle=-45,
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(size=14)
)
st.plotly_chart(fig_employers, use_container_width=True)
