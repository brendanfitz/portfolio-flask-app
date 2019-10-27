from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "TODO: INDEX PAGE"

@app.route('/about')
def about():
    return "TODO: ABOUT PAGE"

@app.route('/benson')
def benson():
    return "TODO: BENSON"

@app.route('/luther')
def luther():
    return "TODO: LUTHER"

@app.route('/mcnulty')
def mcnulty():
    return "TODO: MCNULTY"

@app.route('/fletcher')
def fletcher():
    return "TODO: FLETCHER"

@app.route('/kojak')
def kojak():
    return "TODO: KOJAK"

if __name__ == '__main__':
    app.run(debug=True)
