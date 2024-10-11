import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app  # Assuming this imports your Flask app
from models import setup_db, Question, Category  # Import db from models.py


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:admin@localhost:5432/trivia_test"
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
        self.new_question = {
            "question": "What is the largest ocean on Earth?",
            "answer": "Pacific Ocean",
            "category": 1,
            "difficulty": 2
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

        # Test GET /questions
    def test_get_paginated_questions(self):
        """Test getting paginated questions"""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_beyond_valid_page(self):
        """Test 404 error when requesting beyond valid page"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Test GET /categories
    def test_get_categories(self):
        """Test fetching all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)

    def test_404_get_categories(self):
        """Test fetching non-existent categories"""
        res = self.client().get('/categories/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Test DELETE /questions/<id>
    def test_delete_question(self):
        """Test deleting a question"""
        with self.app.app_context():  # Wrap database operations in app context
            question = Question(question="Test Question", answer="Test Answer", category="1", difficulty=1)
            question.insert()

            question_id = question.id
            res = self.client().delete(f'/questions/{question_id}')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], question_id)

    def test_404_delete_non_existent_question(self):
        res = self.client().delete('/questions/9999')  # Non-existent question ID
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
        
        # Test POST /questions
    def test_create_question(self):
        """Test creating a new question"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])
        self.assertEqual(data['success'], True)

    def test_422_create_question(self):
        """Test 422 error when creating question with missing data"""
        incomplete_question = {
            "question": "",
            "answer": "Pacific Ocean",
            "category": 1,
            "difficulty": 2
        }
        res = self.client().post('/questions', json=incomplete_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')
        
        # Success Test: Get questions for a valid category
    def test_get_questions_by_category_success(self):
        """Test getting questions for a valid category"""
        res = self.client().get('/categories/1/questions')  # Assuming category with ID 1 exists
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], 'Science')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    # Failure Test: Get questions for an invalid category
    def test_get_questions_by_category_failure(self):
        """Test 404 error when getting questions for a non-existent category"""
        res = self.client().get('/categories/9999/questions')  # Assuming category with ID 9999 does not exist
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Test POST /questions/search
    def test_search_questions(self):
        """Test searching questions"""
        res = self.client().post('/questions/search', json={'searchTerm': 'ocean'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)

    def test_200_search_no_results(self):
        """Test that searching for a term with no matching results returns an empty list with a 200 status"""
        res = self.client().post('/questions/search', json={'searchTerm': 'xyznotfound'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)  # Expecting 200 for valid search with no results
        self.assertEqual(data['success'], True)  # Check that success is True
        self.assertEqual(len(data['questions']), 0)  # Ensure no results are returned
        # No need to check for 'message' since this is not an error

    # Test POST /quizzes
    def test_play_quiz(self):
        """Test playing quiz with specific category"""
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 3}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['success'], True)

    def test_404_play_quiz_with_invalid_category(self):
        """Test 404 error when playing quiz with invalid category"""
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 999}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()