from db import blog_db
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    title = 'About'
    subtitle = ''
    return render_template('about.html', title=title, subtitle=subtitle)

@app.route('/blog/<name>')
def blog(name):
    blog_data = blog_db[name]
    title = blog_data['title']
    subtitle = blog_data['subtitle']
    template = '/blogs/{}'.format(blog_data['template'])
    print(template)
    return render_template(template, title=title, subtitle=subtitle)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
