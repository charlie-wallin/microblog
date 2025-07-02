from app import app 

# decorators
# A decorator modifies the functions that follows it
@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Rennie'}
    # The return statement must be followed by something 
    # on the same line.
    return'''
    <html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + ''' </h1>
    </body>
    </html>
    '''
