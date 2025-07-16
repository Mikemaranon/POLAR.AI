# FLASK TEMPLATE

This repository is meant to be a template of how i work with my Flask applications, using my own database and user managers. 
The structure proposed here ensures that any complex app can be created through specific modules that can be implemented in the `web_server/server.py` file the same way `data_m` and `user_m` modules are

In order to run the app, execute this:
```bash
cd web_server
python3 main.py
```

sample API call:
> This endpoint does not require authentication or a request body.
```bash
curl -X POST http://localhost:5000/api/check \
     -H "Content-Type: application/json"
```

Documentation on how the structure and code works is right bellow

## Server

We have 3 different files:
- `main.py`: Starts the Flask Instance, is where the program starts to execute
- `server.py`: Manages the Flask application, adding every module created to it
- `app_routes.py`: Manages the routes in the web, here we define the logic used for the user to navigate between pages

On the other hand, the server complexity starts here: the implementation of different modules to structure the logic of the server in different processes through classes and methods to control all the data workflow. I have included 3 basic modules that i consider essential to every app:
### data_m
A database that stores data in `.json` files through different directories in `data_m/data`. database.py manages all the logic and is the class that should be called whenever we want to access a certain data register from any other module or the main Flask program
### user_m
A module designed to register, login and logout users from the app by using `PyJWT` to generate tokens. The manager has the following methods that can be called using the instance of `user_manager`:
- **`user_manager` methods**: The manager has the following methods that can be called using the instance of the class
    - `check_user()`: can be called to check if the token received from the request is available, returns the user instance where all the information is stored
    - `login()`: checks if the user exists through `authenticate()` method and initializes a new instance for the user if it exists, if the user was already logged in, a new instance will be generated and will overwrite the old one
    - `logout()`: deletes the user instance from the caché
    - `get_user()`: receives an input token and returns the user instance correspondint to that token
    - `authenticate()`: calls the Database to check if the input user exists, returns `true` if the user exists and the password from the `login()` method is the same as the one in the Database. Returns `false` if either of both do not apply
    
- **`user` methods**: The user has 3 basic methods to manage all its information
    - `set_session_data()`: creates a value for a key in the `self.session_data` map.
    - `get_session_data()`: returns the value for the input key in the `self.session_data` map.
    - `clear_session()`: clears the session data leaving it empty

### api_m
Every Flask application has and api system to communicate with the client. This app will manage all the api calls from this module, leaving all the logic to the `api_manager`. It has the following methods
- `_register_APIs()`: register each api endpoint by writing in this method the following line: 
```python
self.app.add_url_rule("/api/[endpoint]", "[endpoint_name]", self.API_[method], methods=["GET", "POST"])
```
- `API_[method]`: to create the logic of an API endpoint, creathe the method writing here the logic

## Client

To make user managing easier, I created a JavaScript file called `token-handler.js` in `web_app/static/JS` with the following methods

### token handling
methods to handle the token locally
- `store_token(token)`: stores the input token in the local storage
- `getToken()`: returns the locally stored token
- `delete_token()`: deletes the locally stored token

### authentication
> IMPORTANT: ASYNC FUNCTION BELLOW
- `login(username, password) `: manages the login of the application connecting to the enpoint
- `send_API_request(method, endpoint, body = null)`: a generic method to call an API endpoint with the token managing logic implemented.

This makes it easier to manage the API calling from the client, it shall be used as the example bellow:

### LOGIN
```JavaScript
    try {
        const response = await login(username, password)

        const data = await response.json();
        console.log(data);

        if (response.ok && data.token) {
            store_token(data.token);
            loadPage("/");
        } else {
            errorMessage.textContent = data.error || "An error occurred.";
            errorMessage.style.display = "block";
        }
    } catch (error) {
        console.error("Error during login:", error);
        errorMessage.textContent = "Incorrect user, please try again.";
        errorMessage.style.display = "block";
    }
```

### API
```JavaScript

    // sending a message to a chatbot managed by Flask, expecting an answer
    try {
        const context = getChatContext()

        body = { 
            temperature: context.temperature,
            system_msg: context.system_msg,
            message: message 
        }

        const response = await send_API_request("POST", "/api/send-message", body)

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data[0];

    } catch (error) {
        console.error('Error:', error);
        return 'Something went wrong.';
    }
```