import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.config.from_object("test_config")
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.db_conn_params = self.app.config['DB_CONN_PARAMS']
        self.database_path = "postgres://{}/{}".format(self.db_conn_params, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def create_new_question(self):
        new_question = {"question": "utq1", "answer": "uta1", "category": "1", "difficulty": 1}
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)
        return data['created_question_id']

    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_categories_405(self):
        res = self.client().post('/categories', json={})
        self.assertEqual(res.status_code, 405)

    def test_get_questions_success(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['currentCategory'])

    def test_get_questions_404(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_specific_question_success(self):
        ques_id = self.create_new_question()
        res = self.client().delete('/questions/' + str(ques_id))

        self.assertEqual(res.status_code, 200)

    def test_delete_specific_question_404(self):
        res = self.client().delete('/questions/-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Resource Not Found")
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)

    def test_create_question_success(self):
        new_question = {"question": "utq1", "answer": "uta1", "category": "1", "difficulty": 1}
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_question_422(self):
        new_question = {"answer": "uta1", "category": "1", "difficulty": 1}
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable entity")

    def test_search_questions_success(self):
        res = self.client().post("/searchQuestions", json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['totalQuestions'], 2)

    def test_search_questions_400(self):
        res = self.client().post("/searchQuestions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Request")

    def test_get_questions_by_cat_success(self):
        res = self.client().get("/categories/5/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['totalQuestions'], 3)

    def test_get_questions_by_cat_404(self):
        res = self.client().get("/categories/-1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found")

    def test_play_quizzes_success(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [20],
            "quiz_category": {"id": 1, "type": "Science"}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question']['id'], 21)

    def test_play_quizzes_400(self):
        res = self.client().post("/quizzes", json={"previous_questions": [20]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
