
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,request
import git

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'TEST 123 Latest Message from SurePortfolio!'

@app.route('/update_server', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('mysite')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    
    elif request.method == 'GET':
        repo = git.Repo('mysite')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    
    else:
        return 'Wrong event type', 400