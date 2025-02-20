from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/universities')
def universities():
    return render_template('universities.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
