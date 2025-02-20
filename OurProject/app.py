import streamlit as st
import pandas as pd
import plotly.express as px

# Загружаем данные
@st.cache_data
def load_data():
    return pd.read_csv("vacancies_january_2.csv")

df = load_data()

# --- Стилизация страницы ---
st.markdown("""
    <style>
        .main {background-color: #f8f9fa; padding: 20px; border-radius: 10px;}
        .sidebar .block-container {background-color: #ffffff; padding: 20px; border-radius: 10px;}
        .stButton>button {background-color: #007bff; color: white; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# --- Фильтры ---
st.sidebar.header("Фильтры")
city = st.sidebar.multiselect("Выберите город:", df["city"].unique(), default=[])
role = st.sidebar.multiselect("Выберите профессию:", df["professional_role"].unique(), default=[])
employment_type = st.sidebar.multiselect("Выберите тип занятости:", df["employment_type"].unique(), default=[])
experience = st.sidebar.multiselect("Выберите требуемый опыт:", df["experience"].unique(), default=[])

# Кнопка сброса фильтров
if st.sidebar.button("Сбросить фильтры"):
    city, role, employment_type, experience = [], [], [], []

filtered_df = df.copy()
if city:
    filtered_df = filtered_df[filtered_df["city"].isin(city)]
if role:
    filtered_df = filtered_df[filtered_df["professional_role"].isin(role)]
if employment_type:
    filtered_df = filtered_df[filtered_df["employment_type"].isin(employment_type)]
if experience:
    filtered_df = filtered_df[filtered_df["experience"].isin(experience)]

filtered_df = filtered_df.dropna(subset=["latitude", "longitude"])

with st.container():
    st.subheader("🌍 Карта вакансий")
    if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:
        fig_map = px.scatter_mapbox(
            filtered_df, lat="latitude", lon="longitude", hover_name="name", 
            hover_data=["salary_from", "salary_currency", "employer_name"], zoom=4
        )
        fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0, "t":0, "l":0, "b":0})
        st.plotly_chart(fig_map, use_container_width=True)
        st.write(f"В выбранном регионе представлено {len(filtered_df)} вакансий.")
    else:
        st.warning("Нет данных с координатами для отображения карты.")

with st.container():
    st.subheader("💰 Распределение зарплат")
    fig2 = px.histogram(filtered_df, x="salary_from", nbins=20, title="Распределение вакансий по зарплатам", color_discrete_sequence=['blue'])
    fig2.update_layout(margin={"r":10, "t":30, "l":10, "b":30})
    st.plotly_chart(fig2, use_container_width=True)
    if not filtered_df.empty:
        st.write(f"Средняя зарплата в выбранной категории составляет {filtered_df['salary_from'].mean():,.0f} тенге.")

with st.container():
    st.subheader("📌 Типы занятости")
    employment_counts = filtered_df["employment_type"].value_counts().reset_index()
    employment_counts.columns = ["employment_type", "count"]
    fig3 = px.pie(employment_counts, names="employment_type", values="count", title="Доля типов занятости")
    st.plotly_chart(fig3, use_container_width=True)
    if not employment_counts.empty:
        top_employment = employment_counts.iloc[0]
        st.write(f"Наибольшая доля вакансий приходится на {top_employment['employment_type']} ({top_employment['count']} вакансий).")

with st.container():
    st.subheader("🎯 Требуемый опыт работы")
    experience_counts = filtered_df["experience"].value_counts().reset_index()
    experience_counts.columns = ["experience", "count"]
    fig4 = px.pie(experience_counts, names="experience", values="count", title="Распределение по опыту работы")
    st.plotly_chart(fig4, use_container_width=True)
    if not experience_counts.empty:
        top_experience = experience_counts.iloc[0]
        st.write(f"Большинство работодателей ищут специалистов с опытом {top_experience['experience']} ({top_experience['count']} вакансий).")

with st.container():
    st.subheader("🏢 Топ-20 работодателей по количеству вакансий")
    top_employers = df["employer_name"].value_counts().nlargest(20).reset_index()
    top_employers.columns = ["employer_name", "count"]
    fig5 = px.bar(top_employers, x="employer_name", y="count", title="Топ-20 работодателей", color="employer_name")
    st.plotly_chart(fig5, use_container_width=True)
    if not top_employers.empty:
        st.write(f"Крупнейший работодатель: {top_employers.iloc[0]['employer_name']} ({top_employers.iloc[0]['count']} вакансий).")

with st.container():
    st.subheader("📊 Востребованность профессии")
    demand_counts = filtered_df["professional_role"].value_counts().nlargest(20).reset_index()
    demand_counts.columns = ["professional_role", "count"]
    fig_demand = px.bar(demand_counts, x="professional_role", y="count", title="Топ-20 востребованных профессий", color="count", color_continuous_scale="Blues")
    st.plotly_chart(fig_demand, use_container_width=True)
    if not demand_counts.empty:
        st.write(f"Самая востребованная профессия: {demand_counts.iloc[0]['professional_role']} ({demand_counts.iloc[0]['count']} вакансий).")
