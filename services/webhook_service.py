from flask import Blueprint, request
import git
import hmac
import hashlib
import os

webhook_blueprint = Blueprint('webhook', __name__)

# Load the GitHub webhook secret from the environment
GITHUB_SECRET = os.getenv('GitHub_SECRET')

# Method to check for expected 
def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)

# Handler for Webhook update request
@webhook_blueprint.route('/update_server', methods=['POST'])
def webhook():
    x_hub_signature = request.headers.get("X-Hub-Signature")
    if not is_valid_signature(x_hub_signature, request.data, GITHUB_SECRET):
        return 'Invalid Signature', 400

    if request.method == 'POST':
        repo = git.Repo('mysite')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    
    else:
        return 'Wrong event type', 400