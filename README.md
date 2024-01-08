# SecureUser API 

This simple REST API is built using Flask-Restful and MongoDB. It allows you to store users' details and user templates' details. The API uses access tokens to ensure that each user can only access their own resources. The supported functions include GET, PUT, POST, and DELETE.

## Installation

Follow these steps to set up the API in a virtual environment:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/SecureUser_API .git
    ```

2. Navigate to the project directory:

    ```bash
    cd SecureUser_API 
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Update the configuration file `config.py` with your MongoDB connection details and other configuration parameters.

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. The API will be available at [http://localhost:5000](http://localhost:5000).

## Endpoints

- **GET /users**: Get the list of all users.
- **GET /users/{user_id}**: Get details of a specific user.
- **POST /users**: Create a new user.
- **PUT /users/{user_id}**: Update details of a specific user.
- **DELETE /users/{user_id}**: Delete a specific user.

- **GET /templates**: Get the list of all templates.
- **GET /templates/{template_id}**: Get details of a specific template.
- **POST /templates**: Create a new template.
- **PUT /templates/{template_id}**: Update details of a specific template.
- **DELETE /templates/{template_id}**: Delete a specific template.

## Token Authentication

The API uses token-based authentication to ensure secure access to user resources. Include the access token in the request headers:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN

## Contributing
    If you'd like to contribute to the project, please follow these guidelines:

## Fork the repository.
    Create a new branch: git checkout -b feature-name
    Make your changes and commit them: git commit -m 'Add some feature'
    Push to the branch: git push origin feature-name
    Submit a pull request.

## License
  This project is licensed under the MIT License.

  Replace placeholders like `your-username` with your actual GitHub username, and customize the sections as needed for your project.






