from db import blog_db
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', projects=blog_db)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog/<name>')
def blog(name):
    blog_data = blog_db[name]
    title = blog_data['title']
    subtitle = blog_data['subtitle']
    template = '/blogs/{}'.format(blog_data['template'])
    print(template)
    return render_template(template, is_blog=True, title=title, subtitle=subtitle)

if __name__ == '__main__':
    app.run(debug=True)
