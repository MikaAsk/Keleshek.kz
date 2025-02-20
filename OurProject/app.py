import os
from flask import Flask, render_template

app = Flask(_name_)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/universities')
def universities():
    return render_template('universities.html')

if name == "main":
    port = int(os.environ.get("PORT", 5000))  # Render задаёт PORT, если нет — используем 5000
    app.run(host="0.0.0.0", port=port)
