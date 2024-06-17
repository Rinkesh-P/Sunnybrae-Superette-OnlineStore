# Sunnybrae-Superette-OnlineStore

## Project Overview:

The Sunnybrae Superette OnlineStore project is a personal project aimed at improving my skills in software development. While primarily a learning exercise, the project also serves as an opportunity to create a fully functional e-commerce website.
<br>
Although this project is personal, it's worth noting that a client was overseeing its development. The client, Sunnybrae Superette, graciously provided real data to populate the website's database. Permission was granted by the client to use this data for educational purposes.

### Features 
- Product Browsing: Users can browse a wide range of products offered by Sunnybrae Superette across different categories.
- Search Functionality: The website features a search function that allows users to search for specific products by name or keyword.
- User Authentication: Users can register, log in, and log out of their accounts to access personalized features such as saving items to their cart or viewing order history.
- Secure Checkout: The checkout process is secure and user-friendly, ensuring a seamless shopping experience for customers.

### Future Plans 

While the current focus is on implementing core features, future plans for this project include:

- enhancing user interface and experience via better styling and visuals
    - Including more inforamtion in the order confirmation 
    - Product Images. 
    - A better homepage for the users to land on

- implementing additional features:
    - The ability to review products. 
    - apply discounts. 
    - order tracking. 
    - ability to see stock levels.

## Folder Structure:
```bash
Sunnybrae-Superette-OnlineStore/
|-- SunnybraeWeb/
|   |-- static/
|   |   |-- css/
|   |   |   |-- main.css
|   |   |-- images/
|   |   |-- js/
|   |   |   |-- main.js
|   |-- store/
|   |   |-- migrations/
|   |   |-- templates/
|   |   |   |-- store/
|   |   |   |   |-- cart.html
|   |   |   |   |-- checkout.html
|   |   |   |   |-- faq.html
|   |   |   |   |-- login.html
|   |   |   |   |-- main.html
|   |   |   |   |-- order_confirmation.html
|   |   |   |   |-- product.html
|   |   |   |   |-- register.html
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- forms.py
|   |   |-- models.py
|   |   |-- test.py
|   |   |-- urls.py
|   |   |-- views.py
|   |-- SunnybraeWeb/
|   |   |-- __init__.py
|   |   |-- asgi.py
|   |   |-- settings.py
|   |   |-- urls.py
|   |   |-- wsgi.py
|   |-- data.xml
|   |-- db.sqlite3
|   |-- manage.py
|   |-- xml_to_sql.py
|-- venv/
|-- planning.docx
|-- read.me
```


## Set-Up

<br> 1 - Opening command prompt (cmd) at the location of the project.

<br> 2 - Install virtaul environment by typing the following command: 
    
    py -m venv venv

<br> 3 - Activate virtual environment: 
    
    venv\Scripts\activate 

<br> 4 - Install Django: 

    pip install django 

<br> 5 - If you are wanting to run this specific project then you will need to run the following in cmd in the SunnybraeWeb folder

    python manage.py runserver

<br> 5 - Once Django is installed navigate to project folder and create Django project: 

    django-admin startproject projectname  (replace project name with desired project name in this case SunnybraeWeb)

<br> 6 - Navigate to the directory of the project

<br> 7 - Create new Django App within project: 
    
    python manage.py startapp appname (where appname can be replaced with whatever you want to call it in this case it is called store)

<br> 8 - open settings.py located in the 'projectname' folder and add new app to "INSTALLED_APPS' list: INSTALLED_APPS[
    ....
    'appname.apps.AppConfig'
]

<br> 9 - Verify setup was correct by running development server: 

    python manage.py runserver

<br>

### Database Setup
<br> 10 - Once models.py has been set up with your relevant tables run the following command in the command promt: 

    python manage.py migrate

<br> 11 - Optional Step: 

    Fill the database with initial data, for this project I obtained the data from my Client and ran the following file to transfer data from XML to SQL: python xml_to_sql.py 

<br> 11 - create superuser to test user authentication and functionality: 

    python manage.py createsuperuser 