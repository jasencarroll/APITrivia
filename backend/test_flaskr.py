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

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test GET /categories
    def test_get_categories(self):
        """Test fetching all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        print(res)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)

    #def test_404_get_categories(self):
    #    """Test fetching non-existent categories"""
    #    res = self.client().get('/categories/9999')
    #    data = json.loads(res.data)

#        self.assertEqual(res.status_code, 404)
#        self.assertEqual(data['success'], False)
#        self.assertEqual(data['message'], 'Resource not found')

    # ... (Your other test methods for questions, quizzes, etc.) ... 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()