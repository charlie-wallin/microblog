from app import app 

# decorators
# A decorator modifies the functions that follows it
@app.route('/')
@app.route('/index')
def index():
    return "Hello world!"

