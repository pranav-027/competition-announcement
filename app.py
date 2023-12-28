# flask_app/app.py

from flask import Flask, render_template, request
from my_app import get_competition_message  # Import the function from my_python_app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    competition_url = request.form['(competition_url']
    compWhatsAppMessage = get_competition_message(competition_url)  # Use the imported function from my_python_app

    return render_template('result.html', message=compWhatsAppMessage)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
