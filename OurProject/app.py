from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os  

app = Flask(__name__)

# Загружаем данные
df = pd.read_csv("vacancies_january_2.csv")

# Создаем папку для графиков, если её нет
if not os.path.exists("static"):
    os.makedirs("static")

@app.route("/")
def home():
    return render_template("home.html")  # Заглушка для главной страницы

@app.route("/analytics")
def analytics():
    city = request.args.get("city")  
    filtered_df = df.copy()

    # Получаем список уникальных городов
    cities = sorted(df["city"].dropna().unique())

    if city:
        filtered_df = filtered_df[filtered_df["city"] == city]

    # Если данных нет, передаем в шаблон флаг
    no_data = filtered_df.empty

    if not no_data:
        # Топ-10 профессий
        top_jobs = filtered_df['name'].value_counts().nlargest(10)
        fig1 = px.bar(
            x=top_jobs.index, 
            y=top_jobs.values, 
            title="Топ-10 профессий",
            labels={'x': 'Профессия', 'y': 'Количество'},
            color=top_jobs.index,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1.write_html("static/chart1.html")

        # Распределение зарплат
        if "salary_from" in filtered_df.columns and not filtered_df["salary_from"].isna().all():
            filtered_df["salary_from"] = pd.to_numeric(filtered_df["salary_from"], errors="coerce")
            filtered_df = filtered_df.dropna(subset=["salary_from"])

            if not filtered_df.empty:
                fig2 = px.histogram(
                    filtered_df, 
                    x="salary_from", 
                    title="Распределение зарплат",
                    labels={'salary_from': 'Зарплата'},
                    color_discrete_sequence=["#2ca02c"]
                )
                fig2.write_html("static/chart2.html")

    # Топ-10 городов по вакансиям
    city_counts = df["city"].value_counts().nlargest(10)
    fig3 = px.bar(
        x=city_counts.index, 
        y=city_counts.values, 
        title="Топ-10 городов по количеству вакансий",
        labels={'x': 'Город', 'y': 'Количество вакансий'},
        color=city_counts.index,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig3.write_html("static/chart3.html")

    # Средняя зарплата по городам
    salary_by_city = df.groupby("city")["salary_from"].mean().nlargest(10)
    fig4 = px.bar(
        x=salary_by_city.index, 
        y=salary_by_city.values, 
        title="Средняя зарплата по городам",
        labels={'x': 'Город', 'y': 'Средняя зарплата'},
        color=salary_by_city.index,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig4.write_html("static/chart4.html")

    return render_template("index.html", city=city, cities=cities, no_data=no_data)

@app.route("/universities")
def universities():
    return render_template("universities.html")

if __name__ == "__main__":
    app.run(debug=True)
