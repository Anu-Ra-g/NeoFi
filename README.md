
## Description

This is a REST API resembling a movie database same as IMDb. The data about users and notes is stored is PostgreSQL database. The API is documented with Swagger. The API uses ***JWT authentication*** for user authentication. The API is hosted at and uses a hosted PostgreSQL database. Both the service and the database are based and deployed on **Render**, the hosting platform. 

**Packages used for this project**
- Flask
- Flask-RESTx
- Flask-SQLAlchemy
- Flask-JWT-Extended
- PyJWT
- psycopg2
- python-dotenv

## API endpoints

- `POST /signup`  
- `POST /login`  
- `POST /notes/create` 🔒
- `GET /notes/{id}` 🔒 
- `POST /notes/share` 🔒 
- `PUT /notes/{id}` 🔒 
- `GET /notes/version-history/{id}` 🔒

## To run the code

1. Clone the repo <br>
    `git clone https://github.com/Anu-Ra-g/beyondcc.git` <br>
2. Change the app directory <br>
    `cd beyondcc` 
3. Activate the virtual environment <br>
    `venv\Scripts\activate (Windows)` <br>
4. Install the dependencies<br>
    `pip install -r requirements.txt`
4. Run the command <br>
    `python runserver.py`











