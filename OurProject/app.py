import streamlit as st
import pandas as pd
import plotly.express as px

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

# --- Основная часть страницы ---
st.title("📊 Аналитика рынка труда")

# --- Размещение графиков ---
with st.container():
    st.subheader("🌍 Карта вакансий")
    
    if not filtered_df.empty:
        fig_map = px.scatter_mapbox(
            filtered_df, 
            lat="latitude", lon="longitude", 
            hover_name="name", 
            hover_data=["salary_from", "salary_currency", "employer_name"], 
            zoom=4, height=500
        )
        fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map)
    else:
        st.warning("Нет данных с координатами для отображения карты.")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Распределение зарплат")
        fig2 = px.histogram(filtered_df, x="salary_from", nbins=20, title="Распределение вакансий по зарплатам", color_discrete_sequence=['blue'])
        st.plotly_chart(fig2)

    with col2:
        st.subheader("📌 Доля типов занятости")
        employment_counts = filtered_df["employment_type"].value_counts().reset_index()
        employment_counts.columns = ["employment_type", "count"]
        fig3 = px.pie(employment_counts, names="employment_type", values="count", title="Доля типов занятости")
        st.plotly_chart(fig3)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Требуемый опыт работы")
        experience_counts = filtered_df["experience"].value_counts().reset_index()
        experience_counts.columns = ["experience", "count"]
        fig4 = px.pie(experience_counts, names="experience", values="count", title="Распределение по опыту работы")
        st.plotly_chart(fig4)

    with col2:
        st.subheader("🏢 Топ-10 работодателей")
        top_employers = df["employer_name"].value_counts().nlargest(10).reset_index()
        top_employers.columns = ["employer_name", "count"]
        fig5 = px.bar(top_employers, x="employer_name", y="count", title="Топ-10 работодателей", color="employer_name")
        st.plotly_chart(fig5)
