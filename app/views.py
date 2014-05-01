from app import app

DATA_BASE_FOLDER = '/Users/yasser/sci-repo/pitchdataset'

@app.route('/')
@app.route('/index')
def index():
	return "Hello, world!"
