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
    city = st.sidebar.selectbox("Выберите город:", ["Все"] + list(df["city"].dropna().unique()))
    role = st.sidebar.selectbox("Выберите профессию:", ["Все"] + list(df["professional_role"].dropna().unique()))
    employment_type = st.sidebar.selectbox("Выберите тип занятости:", ["Все"] + list(df["employment_type"].dropna().unique()))
    experience = st.sidebar.selectbox("Выберите опыт работы:", ["Все"] + list(df["experience"].dropna().unique()))

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
    filtered_df["salary_avg"] = filtered_df[["salary_from", "salary_to"]].mean(axis=1)
    salary_data = filtered_df.groupby(["city", "professional_role"])["salary_avg"].mean().reset_index()

    if not salary_data.empty:
        salary_data = salary_data.sort_values(by="salary_avg", ascending=False)
        fig_salary = px.bar(
            salary_data, 
            x="city", 
            y="salary_avg", 
            color="professional_role", 
            title="Средняя зарплата по городам",
            labels={"salary_avg": "Средняя зарплата", "city": "Город", "professional_role": "Профессия"},
            hover_name="professional_role",
            hover_data={"salary_avg": ":.0f"},
            height=600
        )
        fig_salary.update_layout(xaxis={"categoryorder": "total descending"})
        st.plotly_chart(fig_salary, use_container_width=True)
    else:
        st.warning("Нет данных для построения графика средней зарплаты.")

elif st.session_state.page == "Universities":
    st.components.v1.html(load_html("static/universities.html"), height=600, scrolling=True)
