from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Загружаем данные
df = pd.read_csv("job_market_data.csv")  # Файл с данными о вакансиях

@app.route("/", methods=["GET", "POST"])
def index():
    # Получаем значения из формы (если они переданы)
    selected_region = request.form.get("region")
    selected_industry = request.form.get("industry")
    selected_profession = request.form.get("profession")

    # Фильтруем данные по выбранным параметрам
    filtered_df = df.copy()
    if selected_region:
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]
    if selected_industry:
        filtered_df = filtered_df[filtered_df["Industry"] == selected_industry]
    if selected_profession:
        filtered_df = filtered_df[filtered_df["Profession"] == selected_profession]

    # График 1: Средняя зарплата по профессиям
    salary_chart = px.bar(filtered_df.groupby("Profession")["Salary"].mean().reset_index(),
                          x="Profession", y="Salary",
                          title="Средняя зарплата по профессиям",
                          labels={"Salary": "Зарплата (USD)", "Profession": "Профессия"},
                          color="Salary")

    # График 2: Соотношение вакансий и резюме
    demand_supply_chart = px.line(filtered_df.groupby("Profession")["Job Openings", "Resumes"].sum().reset_index(),
                                  x="Profession", y=["Job Openings", "Resumes"],
                                  title="Спрос (вакансии) vs предложение (резюме)",
                                  labels={"value": "Количество", "Profession": "Профессия"},
                                  markers=True)

    # График 3: Популярные навыки среди работодателей
    skills_chart = px.bar(filtered_df["Skills"].str.split(", ").explode().value_counts().reset_index().head(10),
                          x="index", y="Skills",
                          title="Топ-10 востребованных навыков",
                          labels={"index": "Навык", "Skills": "Количество упоминаний"},
                          color="Skills")

    # Преобразуем графики в HTML
    salary_chart_html = salary_chart.to_html(full_html=False)
    demand_supply_chart_html = demand_supply_chart.to_html(full_html=False)
    skills_chart_html = skills_chart.to_html(full_html=False)

    # Передаем данные в шаблон
    return render_template("index.html",
                           salary_chart=salary_chart_html,
                           demand_supply_chart=demand_supply_chart_html,
                           skills_chart=skills_chart_html,
                           regions=df["Region"].unique(),
                           industries=df["Industry"].unique(),
                           professions=df["Profession"].unique())

if __name__ == "__main__":
    app.run(debug=True)
