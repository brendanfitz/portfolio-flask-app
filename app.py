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
    return render_template('benson.html')

@app.route('/luther')
def luther():
    return render_template('luther.html')

@app.route('/mcnulty')
def mcnulty():
    return render_template('mcnulty.html')

@app.route('/fletcher')
def fletcher():
    return render_template('fletcher.html')

@app.route('/kojak')
def kojak():
    return render_template('kojak.html')

if __name__ == '__main__':
    app.run(debug=True)
