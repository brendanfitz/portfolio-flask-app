from db import blog_db
from flask import Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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
    return render_template(template, is_blog=True, title=title, subtitle=subtitle)

@app.route('/visuals/<name>')
def visuals(name):
    blog_data = blog_db[name]
    template = '/visuals/{}'.format(blog_data['template_visuals'])
    return render_template(template)

if __name__ == '__main__':
    app.run(debug=True)
