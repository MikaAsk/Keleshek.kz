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
    return render_template("home.html")  # Теперь главная страница — это заглушка

@app.route("/analytics")
def analytics():
    city = request.args.get("city")  
    filtered_df = df.copy()

    # Получаем список уникальных городов
    cities = sorted(df["city"].dropna().unique())

    if city:
        filtered_df = filtered_df[filtered_df["city"] == city]

    # Графики
    if not filtered_df.empty:
        top_jobs = filtered_df['name'].value_counts().nlargest(10)
        fig1 = px.bar(x=top_jobs.index, y=top_jobs.values, title="Топ-10 профессий", labels={'x': 'Профессия', 'y': 'Количество'})
        fig1.write_html("static/chart1.html")  

    if "salary_from" in filtered_df.columns and not filtered_df["salary_from"].isna().all():
        filtered_df["salary_from"] = pd.to_numeric(filtered_df["salary_from"], errors="coerce")
        filtered_df = filtered_df.dropna(subset=["salary_from"])  

        if not filtered_df.empty:
            fig2 = px.histogram(filtered_df, x="salary_from", title="Распределение зарплат", labels={'salary_from': 'Зарплата'})
            fig2.write_html("static/chart2.html")

    city_counts = df["city"].value_counts().nlargest(10)
    fig3 = px.bar(x=city_counts.index, y=city_counts.values, title="Топ-10 городов по количеству вакансий", labels={'x': 'Город', 'y': 'Количество вакансий'})
    fig3.write_html("static/chart3.html")

    salary_by_city = df.groupby("city")["salary_from"].mean().nlargest(10)
    fig4 = px.bar(x=salary_by_city.index, y=salary_by_city.values, title="Средняя зарплата по городам", labels={'x': 'Город', 'y': 'Средняя зарплата'})
    fig4.write_html("static/chart4.html")

    return render_template("index.html", city=city, cities=cities)

@app.route("/universities")
def universities():
    return render_template("universities.html")

if __name__ == "__main__":
    app.run(debug=True)
