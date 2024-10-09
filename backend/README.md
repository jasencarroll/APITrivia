# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

# Documentation of API endpoints:

### `GET '/categories'`

- **Description**: Fetches all available categories.
- **Request Arguments**: None
- **Returns**: An object with a `categories` key that contains an object of `id: category_string` pairs.

#### Example Response:
```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

### `GET '/questions?page=<page_number>'`

- **Description**: Fetches a paginated list of questions. Each page contains 10 questions. Also returns categories and the total number of questions.
- **Request Arguments**: 
  - `page` (optional) - integer representing the page number. Defaults to 1.
- **Returns**: An object with `questions`, `total_questions`, `categories`, and `current_category` keys.

#### Example Response:
```json
{
  "success": true,
  "questions": [
    {
      "id": 5,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 2
    },
    {
      "id": 9,
      "question": "Who painted the Mona Lisa?",
      "answer": "Leonardo da Vinci",
      "category": "2",
      "difficulty": 3
    }
  ],
  "total_questions": 20,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null
}
```

---

### `DELETE '/questions/<int:question_id>'`

- **Description**: Deletes a question by its `id`.
- **Request Arguments**: None (URL parameter `question_id` is required).
- **Returns**: An object indicating whether the deletion was successful.

#### Example Response:
```json
{
  "success": true,
  "deleted": 5
}
```

---

### `POST '/questions'`

- **Description**: Adds a new question to the database.
- **Request Body**:
  - `question`: string, the question text.
  - `answer`: string, the answer text.
  - `category`: string, the category ID.
  - `difficulty`: integer, the difficulty level.
- **Returns**: An object indicating whether the creation was successful and the `id` of the created question.

#### Example Request Body:
```json
{
  "question": "What is the largest planet in our solar system?",
  "answer": "Jupiter",
  "category": "1",
  "difficulty": 3
}
```

#### Example Response:
```json
{
  "success": true,
  "created": 25
}
```

---

### `POST '/questions/search'`

- **Description**: Searches for questions based on a search term.
- **Request Body**:
  - `searchTerm`: string, the search keyword.
- **Returns**: A list of questions that match the search term.

#### Example Request Body:
```json
{
  "searchTerm": "capital"
}
```

#### Example Response:
```json
{
  "success": true,
  "questions": [
    {
      "id": 5,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 2
    }
  ],
  "total_questions": 1,
  "current_category": null
}
```

---

### `GET '/categories/<int:category_id>/questions'`

- **Description**: Fetches questions for a specific category.
- **Request Arguments**: None (URL parameter `category_id` is required).
- **Returns**: A list of questions for the given category.

#### Example Response:
```json
{
  "success": true,
  "questions": [
    {
      "id": 5,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 2
    },
    {
      "id": 6,
      "question": "Which is the largest country in Europe?",
      "answer": "Russia",
      "category": "3",
      "difficulty": 3
    }
  ],
  "total_questions": 2,
  "current_category": "Geography"
}
```

---

### `POST '/quizzes'`

- **Description**: Fetches a random question to play the quiz based on a category and previous questions.
- **Request Body**:
  - `previous_questions`: list of question IDs that have already been asked.
  - `quiz_category`: object with `id` field representing the category ID.
- **Returns**: A random question from the specified category that hasn't been asked before.

#### Example Request Body:
```json
{
  "previous_questions": [5, 9],
  "quiz_category": {
    "id": "3"
  }
}
```

#### Example Response:
```json
{
  "success": true,
  "question": {
    "id": 6,
    "question": "Which is the largest country in Europe?",
    "answer": "Russia",
    "category": "3",
    "difficulty": 3
  }
}
```

---

### Error Responses

#### `404 Not Found` Response
Returned when a resource is not found (e.g., when requesting a non-existent question or category).

#### Example Response:
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

#### `422 Unprocessable Entity` Response
Returned when the server is unable to process the contained instructions (e.g., invalid data or a failed database operation).

#### Example Response:
```json
{
  "success": false,
  "error": 422,
  "message": "Unprocessable entity"
}
```

---

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Key Features

1. **CORS Setup**: The app uses `CORS` to allow cross-origin resource sharing, meaning it can be accessed from different domains, including front-end applications.
   
   - CORS is configured to allow requests from any origin (`*`).
   
2. **Pagination Helper**: The `paginate_questions` function is responsible for paginating the questions. It retrieves a page of questions based on the `QUESTIONS_PER_PAGE` constant.

3. **CRUD Operations**:
   - **Categories (`/categories`)**: This endpoint returns all the available categories as a dictionary.
   - **Questions (`/questions`)**:
     - Fetch all questions with pagination.
     - Create a new question by posting to the `/questions` route.
     - Delete a question using the `/questions/<int:question_id>` route.
     - Search for questions based on a search term using the `/questions/search` route.
     - Fetch questions by category with `/categories/<int:category_id>/questions`.

4. **Quiz Handling (`/quizzes`)**:
   - This endpoint allows users to play the quiz. It returns a random question that hasn't been asked before based on the category and previously answered questions.

5. **Error Handling**:
   - Custom error handlers for common HTTP errors like `404` (Resource not found) and `422` (Unprocessable entity).

### Improvements and Suggestions:

1. **Error Handling for Edge Cases**:
   You can enhance the error handling by catching specific exceptions, especially in the `POST` and `DELETE` routes, and providing more detailed responses to the client. For example, in `create_question`, instead of using a blanket `except`, you can handle specific exceptions like `SQLAlchemyError`.

2. **Security Considerations**:
   While your app allows `*` origins in CORS, this is generally not recommended in production environments because it opens up the API to any domain. You may want to restrict the allowed origins to specific domains in a production setup:
   ```python
   CORS(app, resources={r"/api/*": {"origins": "http://your-frontend.com"}})
   ```

3. **Logging**:
   Adding logging for each operation (especially in error handlers) will make it easier to debug issues in production. You can use Python’s built-in logging module:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

4. **Bulk Delete (Optional)**:
   If your app requires bulk deletion of questions, you can modify the delete route to handle a list of question IDs instead of just one.

5. **Code Organization**:
   As your app grows, consider breaking down your routes into separate blueprint modules (e.g., categories, questions) to maintain cleaner code organization.
