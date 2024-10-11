import os
import logging
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import NotFound  # Import NotFound
import random

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        categories_dict = {category.id: category.type for category in categories}

        if len(categories_dict) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()
        categories_dict = {category.id: category.type for category in categories}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_dict,
            'current_category': None
        })



    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            print(f"Attempting to delete question with ID: {question_id}")
            
            # Use Session.get() to retrieve the question by its ID
            question = db.session.get(Question, question_id)
            print(f"Retrieved question: {question}")
            
            if question is None:
                print(f"Question with ID {question_id} not found. Raising NotFound exception.")
                raise NotFound()  # Use the NotFound exception directly

            # If the question exists, delete it
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except NotFound as e:
            raise e  # Re-raise the NotFound exception to ensure a proper 404 response
        except Exception as e:
            print(f"Error: {str(e)}")  # Log the error for debugging
            abort(422)  # Handle all other errors with a 422



    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if not (new_question and new_answer and new_category and new_difficulty):
            abort(422)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })

        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        # Step 2: Get the request body as JSON
        body = request.get_json()

        # Step 3: Validate the request
        if not body or 'searchTerm' not in body:
            abort(422, description="Missing required field: 'searchTerm'.")

        # Step 4: Get the search term from the request body
        search_term = body.get('searchTerm')

        # Step 5: Perform the search in the database (using ILIKE for case-insensitive search)
        search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        # Step 6: If no results are found, return an empty list with a message
        if len(search_results) == 0:
            return jsonify({
                'success': True,
                'questions': [],
                'total_questions': 0,
                'current_category': None,
                'message': 'No questions found matching the search term.'
            })

        # Step 7: Format the results and return them
        return jsonify({
            'success': True,
            'questions': [question.format() for question in search_results],
            'total_questions': len(search_results),
            'current_category': None
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = db.session.get(Category, category_id)  # Use Session.get()

        if category is None:
            abort(404)

        questions = Question.query.filter(Question.category == category_id).all()

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if not quiz_category:
            abort(400, description="Category is required.")

        # If quiz_category['id'] is not 0, fetch the specific category questions
        if quiz_category['id'] != 0:
            # Fetch the category from the database
            category = db.session.get(Category, quiz_category['id'])
            if category is None:
                abort(404, description=f"Category with ID {quiz_category['id']} not found.")

            # Fetch the questions for the specific category that aren't in previous_questions
            questions = Question.query.filter(
                Question.category == quiz_category['id'],
                Question.id.notin_(previous_questions)
            ).all()
        else:
            # If quiz_category['id'] == 0, fetch questions from all categories
            questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

        # Handle case where no questions remain
        if len(questions) == 0:
            return jsonify({
                'success': True,
                'question': None
            })

        # Randomly select the next question
        next_question = random.choice(questions).format()

        return jsonify({
            'success': True,
            'question': next_question
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    return app
