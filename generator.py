import os

from flask import Flask, render_template, url_for
from werkzeug import cached_property
import markdown
import yaml

app = Flask(__name__)

POSTS_DIR = 'posts'

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

#This decorator registers the def as a jinja2 filter
@app.template_filter('format_date')
def format_date(my_date, format='%B %d, %Y'):
	return my_date.strftime(format)

@app.route('/')
def index():
	posts = [Post('hello/')]
	return render_template('index.html', posts=posts)

@app.route('/blog/<path:path>')
def post(path):
	post = Post(path)
	return render_template('post.html', post=post)


if __name__ == '__main__':
	app.run(port=8000, debug=True)