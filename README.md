# Quest Maker API

## Authentication Service Endpoints Documentation

This document provides documentation for the authentication endpoints implemented in the Authentication Service for the Quest Maker API.

### Authentication Endpoints

#### `POST /`

Create new authentication instance.

- **Request:**
  - Body:
    - `email`: Email address of the user.
    - `password`: Password for the user.
    - `firstName` (optional): First name of the user.
    - `lastName` (optional): Last name of the user.
    - `roleIds` (optional): List of role IDs assigned to the user.
    - `organizationId` (optional): List of organization IDs the user belongs to.
    - `userType` (default: 'regular'): Type of user.

- **Response:**
  - Returns the ID of the newly created authentication instance.

- **Error Handling:**
  - Throws an HTTPException if there is an error creating the user in the User service.

#### `GET /`

Read authentication information.

- **Request:**
  - Headers:
    - `Authorization`: Bearer token.

- **Response:**
  - Returns authentication information for the authorized user.

- **Error Handling:**
  - Throws an HTTPException with status code 403 if the token lacks the necessary scope.

#### `PUT /`

Update authentication information.

- **Request:**
  - Headers:
    - `Authorization`: Bearer token.
  - Body:
    - `email`: New email address for the user.
    - `firstName` (optional): New first name for the user.
    - `lastName` (optional): New last name for the user.
    - `roleIds` (optional): New list of role IDs for the user.
    - `organizationId` (optional): New list of organization IDs for the user.

- **Response:**
  - Returns string `'Successfully updated'`.

- **Error Handling:**
  - Throws an HTTPException with status code 403 if the token lacks the necessary scope.

#### `DELETE /deactivate/`

Deactivate user account.

- **Request:**
  - Headers:
    - `Authorization`: Bearer token.

- **Response:**
  - Returns string `'Successfully deleted'` if the user account is deactivated.

- **Error Handling:**
  - Throws an HTTPException with status code 403 if the token lacks the necessary scope.

#### `PUT /change-password/`

Change user password.

- **Request:**
  - Headers:
    - `Authorization`: Bearer token.
  - Body:
    - `password`: New password for the user.

- **Response:**
  - Returns string `'Successfully changed password'` if the password is successfully changed.

- **Error Handling:**
  - Throws an HTTPException with status code 403 if the token lacks the necessary scope.

### Token Endpoints

#### `POST /`

Generate a new access token.

- **Request:**
  - Body:
    - `email`: Email address of the user.
    - `password`: Password for the user.

- **Response:**
  - Returns a new access token.

- **Error Handling:**
  - Throws an HTTPException if there is an error verifying the credentials.

### Pydantic Models

The following Pydantic models are used for request and response data:

- `AuthCreate`
- `AuthUpdate`
- `AuthResponse`
- `AuthInDB`
- `AuthOutDB`
- `Credentials`
- `Token`
- `AuthChangePassword`

---

# Cloning and Running the Web Server

Follow the instructions below to clone a GitHub repository, install the required dependencies using `pip install`, and run the web server using `uvicorn`.

## Prerequisites

Make sure you have the following installed on your system:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) (preferably Python >= 3.11)
- [pip](https://pip.pypa.io/) (Python package installer)

## Steps

1. **Clone the GitHub Repository:**

   Open a terminal or command prompt and run the following command to clone the GitHub repository:

   ```bash
   git clone https://github.com/akinolaemmanuel49/QuestMakerAPIAuthenticationService.git
   ```

2. **Navigate to the Project Directory:**

   Change your working directory to the cloned repository:

   ```bash
   cd QuestMakerAPIAuthenticationService
   ```

3. **Install Requirements:**

   Run the following command to install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   This command reads the dependencies listed in the `requirements.txt` file and installs them.

4. **Run the Web Server:**

   Once the requirements are installed, run the following command to start the web server using `uvicorn`:

   ```bash
   uvicorn main:app --port 8001 --reload
   ```

   - `main:app` specifies the location of the FastAPI app instance.
   - `--port 8001` sets the port number to 8001 (you can choose a different port if needed).
   - `--reload` enables automatic reloading of the server when code changes are detected (useful for development).

5. **Access the Web Server:**

   Open your web browser and go to [http://localhost:8001](http://localhost:8001) (or the port you specified) to access the running web server.

   The application should be up and running, and you can interact with the specified API endpoints.

6. **Use FastAPI builtin swagger docs:**

    Open your web browser and go to [http://localhost:8001/docs](http://localhost:8001/docs) (or the port you specified) to access the running documentation web app.

---

# Handling the .env File

To handle the provided `.env` file, follow these basic instructions:

1. **Create a MongoDB Cluster:**

   - Create a MongoDB cluster using the free tier on the [MongoDB Atlas](https://www.mongodb.com/atlas/database) platform.
   - Obtain the cluster connection string.

2. **Fill in Missing Values:**

   - Open the `.env` file in a text editor.
   - Fill in the missing values for the following variables:
     - `MONGODB_CLUSTER`: Replace it with the MongoDB cluster connection string.
     - `MONGODB_USERNAME`: Set your MongoDB username.
     - `MONGODB_PASSWORD`: Set your MongoDB password.
     - `JWT_SECRET_KEY`: Choose a secret value for JWT token signing.
     - Ensure other variables like `JWT_EXPIRATION_TIME_IN_MINUTES`, `JWT_REFRESH_EXPIRATION_TIME_IN_HOURS`, `JWT_ALGORITHM`, and `ENCRYPTION_SCHEMES` have appropriate values. You can use the provided values or customize them based on your requirements.
     - `USER_SERVICE_URL`: Set the URL of the user service. The default is set to `http://127.0.0.1:8002`, but update it if your user service is hosted elsewhere.

3. **Save and Rename:**

   - Save the changes to the `.env` file.
   - Rename the file from `.env` to just `.env`. Ensure there is no additional extension (e.g., `.txt`).

4. **Keep Secure:**

   - Ensure that the `.env` file is kept secure and not shared publicly. It contains sensitive information like passwords and secret keys.