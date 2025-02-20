import streamlit as st
import pandas as pd
import plotly.express as px

# Функция загрузки данных
@st.cache_data
def load_data():
    return pd.read_csv("vacancies_january_2.csv")

df = load_data()

# --- Навигация ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

def navigate(page):
    st.session_state.page = page

st.sidebar.title("Навигация")
st.sidebar.button("🏠 Home", on_click=lambda: navigate("Home"))
st.sidebar.button("📊 Analytics", on_click=lambda: navigate("Analytics"))
st.sidebar.button("🎓 Universities", on_click=lambda: navigate("Universities"))

# --- Функция загрузки HTML-контента ---
def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# --- Логика страниц ---
if st.session_state.page == "Home":
    st.components.v1.html(load_html("static/home.html"), height=600, scrolling=True)

elif st.session_state.page == "Analytics":
    st.title("📊 Аналитика рынка труда")

    # --- Фильтры ---
    st.sidebar.header("Фильтры")
    city = st.sidebar.selectbox("Выберите город:", ["Все"] + list(df["city"].unique()))
    role = st.sidebar.selectbox("Выберите профессию:", ["Все"] + list(df["professional_role"].unique()))
    employment_type = st.sidebar.selectbox("Выберите тип занятости:", ["Все"] + list(df["employment_type"].unique()))
    experience = st.sidebar.selectbox("Выберите опыт работы:", ["Все"] + list(df["experience"].unique()))

    if st.sidebar.button("Сбросить фильтры"):
        city, role, employment_type, experience = "Все", "Все", "Все", "Все"

    filtered_df = df.copy()
    if city != "Все":
        filtered_df = filtered_df[filtered_df["city"] == city]
    if role != "Все":
        filtered_df = filtered_df[filtered_df["professional_role"] == role]
    if employment_type != "Все":
        filtered_df = filtered_df[filtered_df["employment_type"] == employment_type]
    if experience != "Все":
        filtered_df = filtered_df[filtered_df["experience"] == experience]

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
        st.plotly_chart(fig_map, use_container_width=True)
        st.write(f"В выбранном регионе представлено {len(filtered_df)} вакансий.")
    else:
        st.warning("Нет данных с координатами для отображения карты.")

    # --- Средняя зарплата по городам и профессиям ---
    st.subheader("📈 Средняя зарплата по городам и профессиям")
    salary_data = filtered_df.groupby(["city", "professional_role"])["salary_from"].mean().reset_index()
    if not salary_data.empty:
        fig_salary = px.bar(
            salary_data, 
            x="city", 
            y="salary_from", 
            color="professional_role", 
            title="Средняя зарплата по городам"
        )
        st.plotly_chart(fig_salary, use_container_width=True)
    else:
        st.warning("Нет данных для построения графика средней зарплаты.")

    # --- Распределение зарплат ---
    st.subheader("📊 Распределение зарплат")
    if "salary_from" in filtered_df.columns and not filtered_df["salary_from"].isna().all():
        fig_salary_dist = px.histogram(
            filtered_df, 
            x="salary_from", 
            title="Распределение уровня зарплат",
            nbins=20
        )
        st.plotly_chart(fig_salary_dist, use_container_width=True)
    else:
        st.warning("Нет данных для построения распределения зарплат.")

    # --- Доля типов занятости и опыта ---
    st.subheader("📌 Доля типов занятости и опыта")
    employment_counts = filtered_df["employment_type"].value_counts().reset_index()
    employment_counts.columns = ["employment_type", "count"]
    
    if not employment_counts.empty:
        fig_employment = px.pie(
            employment_counts, 
            names="employment_type", 
            values="count", 
            title="Распределение типов занятости"
        )
        st.plotly_chart(fig_employment, use_container_width=True)
    else:
        st.warning("Нет данных о типах занятости.")

    # --- Востребованные профессии ---
    st.subheader("🔥 Востребованные профессии")
    role_counts = filtered_df["professional_role"].value_counts().reset_index()
    role_counts.columns = ["professional_role", "count"]
    
    if not role_counts.empty:
        fig_roles = px.bar(
            role_counts.head(10), 
            x="professional_role", 
            y="count", 
            title="Топ-10 самых востребованных профессий"
        )
        st.plotly_chart(fig_roles, use_container_width=True)
    else:
        st.warning("Нет данных о востребованных профессиях.")

elif st.session_state.page == "Universities":
    st.components.v1.html(load_html("static/universities.html"), height=600, scrolling=True)
