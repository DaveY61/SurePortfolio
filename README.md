## Table of Contents
- [1. Project Goals](#1-project-goals)
- [2. Key Features](#2-key-features)
- [3. Technology Used](#3-technology-used)
- [4. Application Guide](#4-application-guide) *(to use it)*
  - [4.1 Getting Started](#41-getting-started)
  - [4.2 User Guide](#42-user-guide)
- [5. Pre-Development Steps](#5-pre-development-steps) *(to leverage ideas)*
  - [5.1 Resources](#51-resources)
  - [5.2 Select Host Server](#52-select-host-server)
  - [5.3 Select Framework](#53-select-framework)
  - [5.4 Implement "Hello World" App on the Host Server](#54-implement-hello-world-app-on-the-host-server)
  - [5.5 Integrate with GitHub](#55-integrate-with-github)
  - [5.6 Webhook Service](#56-webhook-service)
  - [5.7 Other Services](#57-other-services)

  
## 1. Project Goals
This ***primary goal*** of this project is to develop a web-based **Dividend Stock Portfolio** which allows building a portfolio of dividend stocks, performs analysis of the positions, displays a roll-up of the portfolio data, and includes a table with position details.

The ***secondary goal*** is to learn the development steps and technology needed to deploy a functional Python WEB Application.

> [!NOTE]
> Use the deployed WEB site *(see [Getting Started](#41-getting-started))*<br>
> Clone this as a starting point for your own application.<br>
> Review the [Pre-Development Steps](#5-pre-development-steps) to leverage parts for your own work.

> [!WARNING]  
> This is a ***work in progress*** so if you like where this is heading then be sure to check back later.<br>
> While under active development, the code may change frequently and the web application may be "broken" temporarily as features are developed.

## 2. Key Features

## 3. Technology Used

## 4. Application Guide

### 4.1 Getting Started
Site is Located here: https://sureportfolio.pythonanywhere.com/
  
### 4.2 User Guide

## 5. Pre-Development Steps
Before starting application development, I wanted to first get a server, framework, and some infrastructure in place.  So these "pre-development steps" were done to prepare for application development.  I documented these steps for me to use again in the future and for anyone else wanting to develop and deploy a Python WEB application.  There are lots (really too many) ways to do this correctly!  I picked one path that works well in the steps below.  

### 5.1 Resources
The following links provide helpful instructions and guideance to build you web-based Python application.
1. Best hosting platforms for Python: https://www.python-engineer.com/posts/hosting-platforms-for-python/
2. Build and deploy a Python application: https://blog.back4app.com/how-to-build-and-deploy-a-python-application/
3. Build a Python Web Applications: https://realpython.com/python-web-applications/
4. Web Applications & Frameworks: https://docs.python-guide.org/scenarios/web/
5. Python Frameworks: https://www.monocubed.com/blog/top-python-frameworks/
6. Flask vs Django: https://www.educative.io/blog/python-frameworks-flask-vs-django
7. A Beginner's Guide to building Flask website on PythonAnywhere: https://blog.pythonanywhere.com/121/

### 5.2 Select Host Server
**SELECTED:** [PythonAnywhere](https://www.pythonanywhere.com)

For the host server, my requirements were:

      1) Python support
      2) GitHub integration
      3) Easy to get started
      4) Free tier with No Credit Card needed

       A domain name would have been a plus, but not worth paying for at this early stage of work.
       It looked like a domain name required a paid service.

If you search for "python web application hosting", the [PythonAnywhere](https://www.pythonanywhere.com) comes up as one of the first choices.  But there are many options to choose from.  Many offer a "Free Tier" but still require a credit card to get started.  I selected PythonAnywhere since it already comes with Python installed and met my selection requirements above.  PythonAnyware does offer an upgrade to a paid version, also, the application is stored in GitHub so can easily be moved to different host later.

It does have limitations, but seemed well suited for my initial project.
> "**PythonAnywhere offers free Python hosting that is particularly suited to beginners and educators.** For those needing more robust features, PythonAnywhere also has paid hosting plans. The pre-installed Python environment further simplifies setup, allowing developers to focus more on coding and less on configuration.<br><br>
However, its storage allowances are low, especially for the prices of the paid plans. Plus, the amount of bandwidth you’re allowed is intentionally unclear. It not only depends on your plan, but you’re also at the mercy of PythonAnywhere’s resources. Overall, PythonAnywhere is best for short, educational projects."<br>
>*https://www.websiteplanet.com/blog/best-python-hosting-services/*

But this 'Easy Setup' was the really big benefit for getting started with PythonAnywhere.
>TOP PRO<br>
**Easy setup**<br>
It's literally a matter of minutes to get a Python-backed website up and running.<br>
>*https://www.slant.co/topics/5453/~hosting-providers-for-a-python-web-application#1*

### 5.3 Select Framework
**SELECTED:** [Flask](https://flask.palletsprojects.com/)

If you search for "best python web application framework", several can be found but two popular ones are [Django](https://www.djangoproject.com/) and [Flask](https://flask.palletsprojects.com/).  I selected Flask since it seemed better suited for my small application and had less of a learning curve to get started.

**Django** is a **complete and complex framework** that comes fully equipped with nearly all the applications a website would need, hence the “batteries-included” nickname.
**Flask** is classified as a **lightweight microframework**. The name is fitting because Flask features only provide the essential functions for setting up your website.

>"In a Flask vs Django fight, Flask would be well out of its weight class. The Flask framework is **ideal for small projects**, whereas Django is ideal for a project with plenty of web apps. The most staggering difference between the two frameworks is the lines of code in each. Flask uses roughly 29,000 lines, whereas Django has just about 290,000 lines of code.
>
>
>With 10 times less code to sift through, Flask can be a much **more suitable framework for those new to web development**. Also, the benefit of manually adding functionality and applications makes Flask an excellent practice tool for beginners. "<br>
>*https://www.educative.io/blog/python-frameworks-flask-vs-django#differences*

### 5.4 Implement "Hello World" App on the Host Server
**METHOD:** Automated by PythonAnywhere

This next step is easy and done for you by PythonAnywhere.  After completing the introduction tour, click the ***I want to create a web application*** option and it will walk you through the steps to create the simple WEB app.

>**Creating A 'Hello World' Web App (Part 1 of 10)**<br>
Up here you will see instructions walking you through the process of creating a Python web application. You can go forward and back through the steps using the arrow buttons below, and you can finish at any time by clicking the cross in the top right. If after closing this helper, you want to go through it again --- or try another one -- go to the Help page, by following the link above and to the right.
>
>*PythonAnywhere walks you through a 10-step process*<br>
>https://blog.pythonanywhere.com/121/

The tutorial creates the "Hello World" site using Flask
>**Creating A 'Hello World' Web App (Part 4 of 10)**<br>
>New Web App Wizard
>
>The next thing we need to do to create a web app is to choose a Web framework -- that is, the specific Python system that will run your web app. There are a bunch of different ones (a good way to start an argument between Python developers is to ask which is the "best" one), **but for this tutorial we'll use Flask.**

You end up with this simple "Hello from Flash!" python application file on the site.

      # A very simple Flask Hello World app for you to get started with...
      from flask import Flask
      
      app = Flask(__name__)
      
      @app.route('/')
      def hello_world():
          return 'Hello from Flask!'

### 5.5 Integrate with GitHub
**METHOD:** WebHook from GitHub / Application endpoint on PythonAnywhere 

Now with a Host, a Framework, and the start of an Application, full development is almost ready to begin.  To streamline deployment, the PythonAnywhere site should be integerated with GitHub.

    Goal is (1) application work on local PC, (2) push GitHub, and (3) automatic refresh server.

    local → GitHub → PythonAnywhere

#### 1. Store PythonAnywhere site in a repo<br>
   Open the [PythonAnywhere help](https://blog.pythonanywhere.com/121/) and scroll to the "Keeping our code under control" section

   Their document walks you through the details to establish a git repo for your 'mysite' application.<br>
   Basically these steps:
   
    a. Open PythonAnywhere: click '$Bash' *(under 'New Console')*
    b. Change Folder: 'cd mysite'
    c. Use 'git config'
            git config --global user.name "Your Name"
            git config --global user.email "you@example.com"
    d. Make an empty repo
            git init
    e. Create '.gitignore' file
            cat > .gitignore
            *.pyc
            __pycache__
            ctrl-D
    d. Push the initial files into the repo
           git add .gitignore flask_app.py
    e. Commit the files
           git commit -m"First Version"
   
#### 2. Create a GitHub **Public** repo<br>
   [Open GitHub](https://github.com/) and use "Create a new repository" to hold your application.<br>
   For the automatic site update to work on a free PythonAnywhere account it will need to be **a public repo in GitHub**.
  
#### 3. Associate PythonAnywhere site with the GitHub Repo
   Return to the Bash shell in the 'mysite' folder and use these commands

    git remote add origin https://github.com/yourusername/yourreponame.git
    git branch -M main
    git push -u origin main

#### 4. Clone for Local Development
   Open the GitHub desktop application<br>
   Select "File->Clone Repositiory"<br>
   Select your new GitHub repo from step #2

   Make a Local change and push to Pythonanywhere
   
      Edit the "flash_app.py" file to change the message
      Push local changes to git and sync with the GitHub server

      Update Pythonanywhere from GitHub
        - Use "git pull" in the Bash shell to pull the updated file
        - On the "Web" tab, use the green "Reload" button to apply the updated file

> [!NOTE]
> The sample Pythonanywhere application 'flask_app.py' assumes you'll be editing directly on their system.  To edit and run locally on your PC, then the following lines need to be added you your flask application.

Add the following lines to your 'flask_app.py

     if __name__ == '__main__':
         app.run(debug=True)

#### 5. Automate site update with Webhook
  To automate the site update from GitHub, two things are needed.  Detailed steps are documented in the references below.

  **First:** Add a GitHub Webhook so an action is taken when the repo is updated.

      a. Open the repo on GitHub
      b. Open the Settings->Webhook page
      c. Add the Payload URL: https://your_domain/update_server  
            for the free site, "your_domain" might be "https://username.pythonanywhere.com/update_server"
            for a paid site, use you selected domain name
      d. For Content Type, select
            'application/json
      e. Click the "Add webhook" button

  **Second:** Add an endpoint route in the application to update the Pythonanywhere site from GitHub.

  In your "flask_app.py" file, add a Flask endpoint route to handle the Webhook message.  In the example below the repo is located in the "mysite" folder on Pythonanywhere.

    import git
    
    @app.route('/update_server', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            repo = git.Repo('mysite')
            origin = repo.remotes.origin
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400 
            
  **Last:** Trigger Auto-Reload on Pythonanywhere.
      
  The "git pull" (above) is actually a "git fetch → git merge" combination, so this will use the post-merge hook.
      
      a. In your git repo over at PythonAnywhere go to .git/hooks/
      b. Make a new file called post-merge.
      c, Put the following code the file:
           #!/bin/sh
           touch /var/www/username_pythonanywhere_com_wsgi.py
           (Use the path to your wsgi file which when touched, reloads your webapp.)
      d. Make this executable, open a bash console there and run
           chmod +x post-merge

#### 6. Secure the Webhook
This last bit is fully lifted from the [first resource](https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664) below showing how to use a "secret" from the GitHub Webhook to make sure only your update is refreshing the server.  This method uses a secret passed by GitHub and checks against the .env file secret that you saved in a file on the server.

Use the GitHub guide for securing the Webhook https://developer.github.com/webhooks/securing/.
Add it to PythonAnywhere as an environment variable (matching the Secret field in the GitHub) This might be helpful https://help.pythonanywhere.com/pages/environment-variables-for-web-apps

The following was added to the "flask_app,py" to read the .env file and validate the Webhook signature

***Read the secret:***

    from check_signature import is_valid_signature
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    w_secret = os.getenv('GitHub_SECRET')

***Update to route handler to check the signature:***

    @app.route('/update_server', methods=['POST'])
    def webhook():
        x_hub_signature = request.headers.get("X-Hub-Signature")
        if not is_valid_signature(x_hub_signature, request.data, w_secret):
            return 'Invalid Signature', 400
        
***Added file "check_signature.py"***

      import hmac
      import hashlib
      
      def is_valid_signature(x_hub_signature, data, private_key):
          # x_hub_signature and data are from the webhook payload
          # private key is your webhook secret
          hash_algorithm, github_signature = x_hub_signature.split('=', 1)
          algorithm = hashlib.__dict__.get(hash_algorithm)
          encoded_key = bytes(private_key, 'latin-1')
          mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
          return hmac.compare_digest(mac.hexdigest(), github_signature)

> Git References<br>
> https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664<br>
> https://stackoverflow.com/a/54268132/9044659<br>
> https://developer.github.com/webhooks/

### 5.6 Webhook Service
Currently the Webhook handler was added in the "flask_app.py" application file.  While this was a simple start, it is poor model to grow when adding other services and application code.  It is better to move all services (and other packages) to different .py files in other folders.  The "flask_app.py" can just import these other packages.

The flask_app.py was changed to provide:

  1. ***create_app()*** function which loads the .env content and then imports each service package with a blueprint.

          def create_app():
            # Load environment variables from .env file
            load_dotenv()
            
            # Define the Flask app
            app = Flask(__name__)
            
            # Dynamically discover and register blueprints
            register_blueprints(app, 'services')  
        
            return app
     
  2. ***register_blueprints()*** function which finds and imports the files in the services folder
     
          def register_blueprints(app, package_name):
              package = importlib.import_module(package_name)
              for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
                  if is_pkg:
                      continue
                  module = importlib.import_module(f"{package_name}.{module_name}")
                  if hasattr(module, 'blueprint'):
                      app.register_blueprint(getattr(module, 'blueprint'))

  The ***servce/webhook_service.py*** file was added to contain the webhook update handler

### 5.7 Other Services

#### 1. Application Log

#### 2. Send SMTP Email

#### 3. User Authentication

