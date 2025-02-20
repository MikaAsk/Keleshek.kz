import streamlit as st
import pandas as pd
import plotly.express as px

# --- Функция загрузки данных ---
@st.cache_data
def load_data():
    return pd.read_csv("vacancies_january_2.csv")

df = load_data()

# --- Инициализация состояния ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "city" not in st.session_state:
    st.session_state.city = "Все"
if "role" not in st.session_state:
    st.session_state.role = "Все"
if "employment_type" not in st.session_state:
    st.session_state.employment_type = "Все"
if "experience" not in st.session_state:
    st.session_state.experience = "Все"

# --- Функции навигации и сброса фильтров ---
def navigate(page):
    st.session_state.page = page

def reset_filters():
    st.session_state.city = "Все"
    st.session_state.role = "Все"
    st.session_state.employment_type = "Все"
    st.session_state.experience = "Все"

# --- Боковая панель навигации ---
st.sidebar.title("Навигация")
st.sidebar.button("🏠 Home", on_click=navigate, args=("Home",))
st.sidebar.button("📊 Analytics", on_click=navigate, args=("Analytics",))
st.sidebar.button("🎓 Universities", on_click=navigate, args=("Universities",))

# --- Главная страница ---
if st.session_state.page == "Home":
    st.title("🏠 Добро пожаловать!")
    st.write("Здесь будет главная информация о сайте и его возможностях.")

# --- Страница Аналитики ---
elif st.session_state.page == "Analytics":
    st.title("📊 Аналитика рынка труда")

    # --- Фильтры ---
    st.sidebar.header("Фильтры")
    st.session_state.city = st.sidebar.selectbox("Выберите город:", ["Все"] + list(df["city"].unique()), index=["Все"] + list(df["city"].unique()).index(st.session_state.city) if st.session_state.city in df["city"].unique() else 0)
    st.session_state.role = st.sidebar.selectbox("Выберите профессию:", ["Все"] + list(df["professional_role"].unique()), index=["Все"] + list(df["professional_role"].unique()).index(st.session_state.role) if st.session_state.role in df["professional_role"].unique() else 0)
    st.session_state.employment_type = st.sidebar.selectbox("Выберите тип занятости:", ["Все"] + list(df["employment_type"].unique()), index=["Все"] + list(df["employment_type"].unique()).index(st.session_state.employment_type) if st.session_state.employment_type in df["employment_type"].unique() else 0)
    st.session_state.experience = st.sidebar.selectbox("Выберите опыт работы:", ["Все"] + list(df["experience"].unique()), index=["Все"] + list(df["experience"].unique()).index(st.session_state.experience) if st.session_state.experience in df["experience"].unique() else 0)

    st.sidebar.button("🔄 Сбросить фильтры", on_click=reset_filters)

    # --- Фильтрация данных ---
    filtered_df = df.copy()
    if st.session_state.city != "Все":
        filtered_df = filtered_df[filtered_df["city"] == st.session_state.city]
    if st.session_state.role != "Все":
        filtered_df = filtered_df[filtered_df["professional_role"] == st.session_state.role]
    if st.session_state.employment_type != "Все":
        filtered_df = filtered_df[filtered_df["employment_type"] == st.session_state.employment_type]
    if st.session_state.experience != "Все":
        filtered_df = filtered_df[filtered_df["experience"] == st.session_state.experience]

    # --- Карта вакансий ---
    st.subheader("🌍 Карта вакансий")
    if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns and not filtered_df.empty:
        fig_map = px.scatter_mapbox(
            filtered_df, 
            lat="latitude", lon="longitude", 
            hover_name="name", 
            hover_data=["salary_from", "salary_currency", "employer_name"], 
            zoom=4
        )
        fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0, "t":0, "l":0, "b":0})
        st.plotly_chart(fig_map, use_container_width=True)
        st.write(f"В выбранном регионе представлено {len(filtered_df)} вакансий.")
    else:
        st.warning("Нет данных с координатами для отображения карты.")

# --- Страница Университетов ---
elif st.session_state.page == "Universities":
    st.title("🎓 Университеты")
    st.write("Раздел о университетах и образовании.")
