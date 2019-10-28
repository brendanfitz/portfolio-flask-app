from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/benson')
def benson():
    return render_template('01-benson.html')

@app.route('/luther')
def luther():
    return render_template('02-luther.html')

@app.route('/mcnulty')
def mcnulty():
    return render_template('03-mcnulty.html')

@app.route('/fletcher')
def fletcher():
    return render_template('04-fletcher.html')

@app.route('/kojak')
def kojak():
    return render_template('05-kojak.html')

if __name__ == '__main__':
    app.run(debug=True)
