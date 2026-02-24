# CS361-Team31-User-Authentication-Microservice
User Authentication microservice for CS361 Team 31. Provides user registration, login, and token validation via REST API using JSON.

## How to use:
1. First install the required packages
- Flask
- PyJWT

```pip install flask pyjwt```

2. Run the app by going in the same folder as app.py and run

```python app.py```

You should see something like this:

```Running on http://127.0.0.1:5000```

3. To test, open another terminal and test with curl:

- To register a user, two parameters must be sent:
  - username: str (must be a unique username)
  - password: str
    - requires at least 8 characters
    - requires at least one uppercase letter
    - requires at least one lowercase
    - requires at least one symbol
- Information received will include:
  - message: str
  - status: str

Register Example:
```
curl -X POST http://127.0.0.1:5000/register \
-H "Content-Type: application/json" \
-d "{\"username\":\"testuser\",\"password\":\"StrongPassword123@\"}"
```

- To login a registered user, two parameters must be sent:
  - username: str
  - password: str
- On success, information received will include:
  - status: str
  - token: str
- On fail, information received will include:
  - status: str
  - message: str
  
Login Example: 
```
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d "{\"username\":\"testuser\",\"password\":\"StrongPassword123@\"}"
```

UML Diagram:

![Auth Microservice UML Diagram](assets/UML_diagram.png "Auth Microservice UML Diagram")