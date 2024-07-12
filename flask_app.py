from flask import Flask,request
import git
from check_signature import is_valid_signature

import os
from dotenv import load_dotenv

load_dotenv()
w_secret = os.getenv('GitHub_SECRET')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Updated Message from SurePortfolio!'

@app.route('/update_server', methods=['POST'])
def webhook():
    x_hub_signature = request.headers.get("X-Hub-Signature")
    if not is_valid_signature(x_hub_signature, request.data, w_secret):
        return 'Invalid Signature', 400

    if request.method == 'POST':
        repo = git.Repo('mysite')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    
    else:
        return 'Wrong event type', 400
    
if __name__ == '__main__':
    app.run(debug=True)