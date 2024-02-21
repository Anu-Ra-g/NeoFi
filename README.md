
## Description

This is a REST API resembling a movie database same as IMDb. The data about users and notes is stored is PostgreSQL database. The API is documented with Swagger. The API uses ***JWT authentication*** for user authentication. The API is hosted at https://neofi-y8ef.onrender.com/ and uses a hosted PostgreSQL database. Both the service and the database are based and deployed on **Render**, the hosting platform. 

The API is hosted using the free service on Render, which means it'll go down due to inactivity until unless brought backup. It's best to start the server and test this API locally using Postman or cURL.

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

P.S :- I lack in experience in testing out the endpoints automatically. Hence, I couldn't create a system for automated testing. I'd like you to consider for me for a internship role if my application do not suffice for a full-time role at your company. Thank You









