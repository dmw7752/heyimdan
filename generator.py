import os

from flask import Flask, render_template, url_for, abort
from werkzeug import cached_property
import markdown
import yaml


POSTS_DIR = 'posts'

class Feed(object):
    def __init__(self):
        self.posts = {}
        self.populate_feed()

    def populate_feed(self):
        '''Walks the POSTS_DIR and adds all the post objects to the feed.posts dictionary
        '''
        for (root, directory, files) in os.walk(POSTS_DIR):
            for filename in files:
                name, ext = os.path.splitext(filename)
                if ext == '.md':
                    post = Post(name)
                    self.posts[post.url_path] = post

    def get_post(self, path):
        try:
            return self.posts[path.strip('/')]
        except KeyError:
            abort(404)

class Post(object):
    def __init__(self, path):
        self.url_path = path.strip('/')
        self.file_path = os.path.join(POSTS_DIR, path.strip('/') + '.md')
        self.get_metadata()

    def get_metadata(self):
        meta = ''
        self.metadata = {}
        with open(self.file_path, 'r') as file_input:
            for line in file_input:
                if not line.strip():
                    break
                meta += line
        self.metadata.update(yaml.load(meta))

    #This decorator caches the html everytime this is called so you 
    #are not re-rendering the markdown over and over again.
    @cached_property
    def html(self):
        with open(self.file_path, 'r') as file_input:
            content = file_input.read().split('\n\n', 1)[1].strip()
        return markdown.markdown(content)

    @cached_property
    def url(self):
        return url_for('post', path=self.url_path)


app = Flask(__name__)
feed = Feed()


#This decorator registers the def as a jinja2 filter
@app.template_filter('format_date')
def format_date(my_date, format='%B %d, %Y'):
    return my_date.strftime(format)

@app.route('/')
def index():
    return render_template('index.html', posts=sorted(feed.posts.values(),
                                         key=lambda x:x.metadata['date'],
                                         reverse=True))

@app.route('/blog/<path:path>')
def post(path):
    post = feed.get_post(path)
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(port=8000, debug=True)