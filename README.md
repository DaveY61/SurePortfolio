## Table of Contents

- [1. Project Goals](#1-project-goals)
- [2. Key Features](#2-key-features)
- [3. Technology Used](#3-technology-used)
- [4. Application Guide](#4-application-guide) *(to use it)*
  - [4.1 Getting Started](#41-getting-started)
  - [4.2 User Guide](#42-user-guide)
- [5. Development Steps](#5-development-steps) *(to leverage ideas)*
  - [5.1 Development Resources](#51-development-resources)
  - [5.2 Select Host Server](#52-select-host-server)
  - [5.3 Select Framework](#53-select-framework)
  
## 1. Project Goals
This ***primary goal*** of this project is to develop a web-based **Dividend Stock Portfolio** which allows building a portfolio of dividend stocks, performs analysis of the positions, displays a roll-up of the portfolio data, and includes a table with position details.

The ***secondary goal*** is to learn the development steps and technology needed to deploy a functional Python WEB Application.

> [!NOTE]
> You may use the deployed WEB site *(see [4.1 Getting Started](#41-getting-started))*<br>
> You may clone this as a starting point for your own application.<br>
> You may review the [Development Steps](#5-development-steps) to leverage parts for your own application.

> [!WARNING]  
> This is a ***work in progress*** so if you like where this is heading then be sure to check back later.<br>
> While under active development, the code may change frequently and the web application may be "broken" temporarily as features are developed.

## 2. Key Features

## 3. Technology Used
This project uses GitHub WebHooks to push updates and deploy the content on https://www.pythonanywhere.com/

## 4. Application Guide

### 4.1 Getting Started
Site is Located here: https://sureportfolio.pythonanywhere.com/
  
### 4.2 User Guide

## 5. Development Steps

### 5.1 Development Resources
The following links provide helpful instructions and guideance to build you web-based Python application.
1. Build a Python Web Applications: https://realpython.com/python-web-applications/
2. Web Applications & Frameworks: https://docs.python-guide.org/scenarios/web/
3. Python Frameworks: https://www.monocubed.com/blog/top-python-frameworks/
4. Flask vs Django: https://www.educative.io/blog/python-frameworks-flask-vs-django

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

>"In a Flask vs Django fight, Flask would be well out of its weight class. The Flask framework is **ideal for small projects**, whereas Django is ideal for a project with plenty of web apps. The most staggering difference between the two frameworks is the lines of code in each. Flask uses roughly 29,000 lines, whereas Django has just about 290,000 lines of code.<br><br>
With 10 times less code to sift through, Flask can be a much **more suitable framework for those new to web development**. Also, the benefit of manually adding functionality and applications makes Flask an excellent practice tool for beginners. "<br>
>*https://www.educative.io/blog/python-frameworks-flask-vs-django#differences*


3. Implement a basic "Hello World" page on the host server
4. Store the site in GitHub w/automatic push to the host server
5. Add User Login front end
6. Select a GUI Visualization library
7. Develop the Portfolio format with the GUI library
8. Add "live data" gathering to update the Portfolio data
9. Add support for an "email summary" sent to the Portfolio Owner's email address

