# 🎓 Degree Evaluation - Project Setup

## 📌 Prerequisites
- Pip installed
- Python3 installed 
- Mysql installed 
- Django installed `pip3 install django`
- Mysql-Client installed `pip3 install mysqlclient`
- Dotenv installed `pip3 install python-dotenv` 

## 🗄️ Database Setup
1. **Create a Mysql Database**
   - create an .env file including these details:
```python
    DATABASE_NAME=your database name
    DATABASE_USER=your user name
    DATABASE_PASSWORD=your password
    DATABASE_HOST=your database host
    DATABASE_PORT=your database port
    
    SECRET_KEY=your random secret key
```
2. **The program will automatically read your .env file, and then connect to your database**

## 🔧 Virtual Environment
1. **Create a Virtual Environment**
   - Run `python3 -m venv env` to create a virtual environment.
2. **Activate the Virtual Environment**
   - On Linux/macOS, run `source env/bin/activate`.
   - On Windows, run `env\Scripts\activate`.


## ⚙️ Django Migrations
1. **Make Migrations**
   - Run `python3 manage.py makemigrations`.
2. **Run Migrations**
   - Execute `python3 manage.py migrate` to apply the migrations.

## 📊 Load Data
1. **Load Initial Data**
   - Execute `python3 manage.py loaddata university/fixtures/*.json`.

## 💻 Run the Server
1. **Start the Django Development Server**
   - Run `python3 manage.py runserver`.
   - Access the server through your preferred browser at `http://127.0.0.1:8000/`.
