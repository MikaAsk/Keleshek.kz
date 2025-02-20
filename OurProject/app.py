from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Загружаем данные
df = pd.read_csv("job_market_data.csv")

@app.route("/", methods=["GET"])
def index():
    """Главная страница с фильтрами"""
    return render_template(
        "index.html",
        regions=df["Region"].dropna().unique(),
        industries=df["Industry"].dropna().unique(),
        professions=df["Profession"].dropna().unique()
    )

@app.route("/chart", methods=["POST"])
def chart():
    """Обновляет графики в зависимости от фильтров"""
    data = request.json
    selected_region = data.get("region")
    selected_industry = data.get("industry")
    selected_profession = data.get("profession")

    filtered_df = df.copy()
    if selected_region:
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]
    if selected_industry:
        filtered_df = filtered_df[filtered_df["Industry"] == selected_industry]
    if selected_profession:
        filtered_df = filtered_df[filtered_df["Profession"] == selected_profession]

    # 1️⃣ Средняя зарплата по профессиям
    salary_chart = px.bar(
        filtered_df.groupby("Profession")["Salary"].mean().reset_index(),
        x="Profession",
        y="Salary",
        title="Средняя зарплата по профессиям",
        labels={"Salary": "Зарплата (USD)", "Profession": "Профессия"},
        color="Salary"
    ).to_html(full_html=False)

    # 2️⃣ Соотношение вакансий и резюме
    demand_supply_chart = px.line(
        filtered_df.groupby("Profession")[["Job Openings", "Resumes"]].sum().reset_index(),
        x="Profession",
        y=["Job Openings", "Resumes"],
        title="Спрос (вакансии) vs предложение (резюме)",
        labels={"value": "Количество", "Profession": "Профессия"},
        markers=True
    ).to_html(full_html=False)

    # 3️⃣ Популярные навыки среди работодателей
    if "Skills" in filtered_df.columns and not filtered_df["Skills"].isna().all():
        skills_chart = px.bar(
            filtered_df["Skills"].dropna().str.split(", ").explode().value_counts().reset_index().head(10),
            x="index",
            y="Skills",
            title="Топ-10 востребованных навыков",
            labels={"index": "Навык", "Skills": "Количество упоминаний"},
            color="Skills"
        ).to_html(full_html=False)
    else:
        skills_chart = "<p>Нет данных о навыках</p>"

    # 4️⃣ Количество вакансий по отраслям
    industry_chart = px.pie(
        filtered_df["Industry"].value_counts().reset_index(),
        names="index",
        values="Industry",
        title="Количество вакансий по отраслям",
        labels={"index": "Отрасль", "Industry": "Количество вакансий"}
    ).to_html(full_html=False)

    return jsonify({
        "salary_chart": salary_chart,
        "demand_supply_chart": demand_supply_chart,
        "skills_chart": skills_chart,
        "industry_chart": industry_chart
    })

if __name__ == "__main__":
    app.run(debug=True)
