# Sunnybrae-Superette-OnlineStore
Creating an e commerce websitie for Sunnybrae Superette. 

<br> Set up of Virtual Environment and Django </br>

<br> Opening cmd at the location of the project.
<br> Install virtaul environment, type the following in cmd: "py -m venv venv"
<br> Then type the following to activate the virtual environment: "venv\Scripts\activate" 
<br> Once activated in cmd: "pip -m install django
<br> After Django is installed, navigate to the project folder and type in cmd "django-admin startproject projectname" (projectname can be whatever, for me its SunnybraeWeb)
<br> Navigate to the directory of the project: "cd SunnybraeWeb" 
<br> run the following in CMD: "python manage.py startapp store" (store can be named whatever you want)
<br> open settings.py which should be in the projectname folder and then in the list called Installed_APPS = [ ] include 'store.apps.StoreConfig', ("its named store.apps for me but will be based on whatever you called it instead of store in the step above.)
<br> check if setup correctly via running the following in cmd (ensure that you are in the same directory as manage.py) "python manage.py runserver" then open up the port if done properly it should take you to a success landing page. 