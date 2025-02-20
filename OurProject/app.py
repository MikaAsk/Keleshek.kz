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

# --- Карта вакансий ---
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
    st.plotly_chart(fig_map, use_container_width=True)  # 🔹 Адаптивная ширина
else:
    st.warning("Нет данных с координатами для отображения карты.")

# --- Распределение зарплат ---
st.subheader("💰 Распределение зарплат")
fig2 = px.histogram(
    filtered_df, 
    x="salary_from", 
    nbins=20, 
    title="Распределение вакансий по зарплатам",
    color_discrete_sequence=['blue']
)
fig2.update_layout(margin={"r":10, "t":30, "l":10, "b":30})  # 🔹 Улучшенные отступы
st.plotly_chart(fig2, use_container_width=True)

# --- Доля типов занятости ---
st.subheader("📌 Типы занятости")
employment_counts = filtered_df["employment_type"].value_counts().reset_index()
employment_counts.columns = ["employment_type", "count"]
fig3 = px.pie(
    employment_counts, 
    names="employment_type", 
    values="count", 
    title="Доля типов занятости"
)
fig3.update_layout(margin={"r":10, "t":30, "l":10, "b":30})  # 🔹 Улучшенные отступы
st.plotly_chart(fig3, use_container_width=True)

# --- Требуемый опыт работы ---
st.subheader("🎯 Требуемый опыт работы")
experience_counts = filtered_df["experience"].value_counts().reset_index()
experience_counts.columns = ["experience", "count"]
fig4 = px.pie(
    experience_counts, 
    names="experience", 
    values="count", 
    title="Распределение по опыту работы"
)
fig4.update_layout(margin={"r":10, "t":30, "l":10, "b":30})  # 🔹 Улучшенные отступы
st.plotly_chart(fig4, use_container_width=True)

# --- Топ-20 работодателей ---
st.subheader("🏢 Топ-20 работодателей по количеству вакансий")
top_employers = df["employer_name"].value_counts().nlargest(20).reset_index()
top_employers.columns = ["employer_name", "count"]
fig5 = px.bar(
    top_employers, 
    x="employer_name", 
    y="count", 
    title="Топ-20 работодателей по количеству вакансий", 
    color="employer_name"
)
fig5.update_layout(
    xaxis_tickangle=-45,  # 🔹 Улучшенный наклон подписей
    margin={"r":10, "t":30, "l":10, "b":30}
)
st.plotly_chart(fig5, use_container_width=True)

# --- Востребованность профессии ---
st.subheader("📊 Востребованность профессии")

# Выбираем топ-20 профессий
demand_counts = filtered_df["professional_role"].value_counts().nlargest(20).reset_index()
demand_counts.columns = ["professional_role", "count"]

# Строим график
fig_demand = px.bar(
    demand_counts, 
    x="professional_role", 
    y="count", 
    title="Топ-20 востребованных профессий",
    color="count",
    color_continuous_scale="Blues"
)

# Улучшаем отображение подписей
fig_demand.update_layout(
    xaxis_title="Профессия",
    yaxis_title="Количество вакансий",
    xaxis_tickangle=-45,  # 🔹 Улучшенный наклон подписей
    margin={"r":10, "t":30, "l":10, "b":30}
)

st.plotly_chart(fig_demand, use_container_width=True) 
