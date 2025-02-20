import streamlit as st
import pandas as pd
import plotly.express as px

# 🔹 Настройка страницы
st.set_page_config(page_title="Аналитика вакансий", layout="wide")

# 🎨 Стилизация
st.markdown("""
    <style>
        body {background-color: #f5f7fa;}
        .main-title {text-align: center; font-size: 28px; font-weight: bold; color: #333;}
        .sub-title {font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #555;}
        .stPlotlyChart {background: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

# 📥 Загружаем данные
@st.cache_data
def load_data():
    return pd.read_csv("vacancies_january_2.csv")

df = load_data()

# 🎛️ Фильтры (слева)
with st.sidebar:
    st.header("🔍 Фильтры")
    city = st.selectbox("🏙 Город:", ["Все"] + list(df["city"].dropna().unique()))
    role = st.selectbox("💼 Профессия:", ["Все"] + list(df["professional_role"].dropna().unique()))

filtered_df = df.copy()
if city != "Все":
    filtered_df = filtered_df[filtered_df["city"] == city]
if role != "Все":
    filtered_df = filtered_df[filtered_df["professional_role"] == role]

filtered_df = filtered_df.dropna(subset=["latitude", "longitude"])

# 🏆 Основной заголовок
st.markdown("<h1 class='main-title'>Аналитика рынка труда</h1>", unsafe_allow_html=True)

# 📌 Карта вакансий
st.markdown("<h2 class='sub-title'>🌍 Карта вакансий</h2>", unsafe_allow_html=True)
if not filtered_df.empty:
    fig_map = px.scatter_mapbox(
        filtered_df, lat="latitude", lon="longitude", hover_name="name",
        hover_data=["salary_from", "salary_currency", "employer_name"], zoom=4, height=500
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("⚠️ Нет данных для отображения карты.")

# 💰 Улучшенная гистограмма зарплат с градиентом
st.markdown("<h2 class='sub-title'>💰 Распределение зарплат</h2>", unsafe_allow_html=True)

# Фильтруем данные, убираем пропущенные значения
salary_filtered = filtered_df.dropna(subset=["salary_from"])

# Создаем bins для распределения зарплат
fig_salary = px.histogram(
    salary_filtered, 
    x="salary_from", 
    nbins=30, 
    title="Распределение вакансий по зарплатам",
    color="salary_from",  
    color_continuous_scale="bluered",  # Градиент от синего к красному
)

# Настраиваем стили
fig_salary.update_layout(
    xaxis_title="Зарплата",
    yaxis_title="Количество вакансий",
    coloraxis_colorbar=dict(
        title="Уровень зарплаты",  
        tickvals=[salary_filtered["salary_from"].min(), salary_filtered["salary_from"].max()],
        ticktext=["Низкие зарплаты", "Высокие зарплаты"],
    ),
    margin=dict(l=40, r=40, t=40, b=40),  
)

st.plotly_chart(fig_salary, use_container_width=True)


# 📌 Типы занятости и опыт работы (рядом)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h2 class='sub-title'>📌 Типы занятости</h2>", unsafe_allow_html=True)
    employment_counts = filtered_df["employment_type"].value_counts().reset_index()
    employment_counts.columns = ["employment_type", "count"]
    fig_employment = px.pie(employment_counts, names="employment_type", values="count", color_discrete_sequence=px.colors.qualitative.Set2)
    fig_employment.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_employment, use_container_width=True)

with col2:
    st.markdown("<h2 class='sub-title'>🎯 Опыт работы</h2>", unsafe_allow_html=True)
    experience_counts = filtered_df["experience"].value_counts().reset_index()
    experience_counts.columns = ["experience", "count"]
    fig_experience = px.pie(experience_counts, names="experience", values="count", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_experience.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_experience, use_container_width=True)

# 🏢 Топ-10 работодателей
st.markdown("<h2 class='sub-title'>🏢 Топ-10 работодателей</h2>", unsafe_allow_html=True)
top_employers = df["employer_name"].value_counts().nlargest(10).reset_index()
top_employers.columns = ["employer_name", "count"]
fig_employers = px.bar(top_employers, x="employer_name", y="count", color="employer_name", color_discrete_sequence=px.colors.qualitative.Set3)
fig_employers.update_layout(xaxis_title="Работодатель", yaxis_title="Количество вакансий", xaxis_tickangle=-45)
st.plotly_chart(fig_employers, use_container_width=True)
