import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        return response

    def _get_categories():
        rows = Category.query.all()
        fmt_categories = [category.format() for category in rows]
        categories_map = {}
        for category in fmt_categories:
            categories_map[category['id']] = category['type']
        return categories_map

    def _get_cur_category_string(cat_id):
        cur_cat = Category.query.filter(Category.id == cat_id).first()
        return cur_cat.type

    """    
    Endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories", methods=['GET'])
    @cross_origin()
    def get_all_categories():
        # rows = Category.query.all()
        # fmt_categories = [category.format() for category in rows]
        # categories_map = {}
        # for category in fmt_categories:
        #     categories_map[category['id']] = category['type']
        categories_json = {"categories": _get_categories()}
        return jsonify(categories_json), 200

    """    
    An endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    @cross_origin()
    def get_questions():
        # pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all().order_by(Question.id)
        formatted_ques = [question.format() for question in questions][start:end]

        # find category string of first question in the list
        cur_cat = _get_cur_category_string(formatted_ques[0]['category'])

        return jsonify({"questions": formatted_ques, "totalQuestions": len(formatted_ques),
                        "categories": _get_categories(),
                        "currentCategory": cur_cat}), 200

    """    
    An endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<id>", methods=['DELETE'])
    @cross_origin()
    def delete_specific_question(id: int):
        ques_to_delete = Question.query.filter(Question.id == id).one_or_none()

        if ques_to_delete is None:
            abort(404)

        ques_to_delete.delete()
        return jsonify({'success': True}), 200

    """    
    An endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    @cross_origin()
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)

        if not is_valid_question(new_question):
            abort(422)

        try:
            new_question.insert()
            return jsonify({'success': True, 'created_question_id': new_question.id}), 200
        except:
            abort(422)

    def is_valid_question(new_quest: Question):
        if new_quest.question is None or new_quest.answer is None or new_quest.category is None or new_quest.difficulty is None:
            return False
        return True

    """
    @TODO:
    A POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/searchQuestions', methods=['POST'])
    @cross_origin()
    def search_question_by_search_term():
        body = request.get_json()

        if body is None:
            abort(400)

        search_term = body.get('searchTerm', None)

        if search_term is None:
            abort(400)

        questions = Question.query.filter(Question.question.ilike('%'+search_term+'%')).order_by(Question.id).all()
        formatted_questions = [question.format() for question in questions]
        cur_cat_string = ""
        if len(formatted_questions) > 0:
            cur_cat_string = _get_cur_category_string(formatted_questions[0]['category'])

        return jsonify({'questions': formatted_questions, 'totalQuestions': len(questions),
                        'currentCategory': cur_cat_string}), 200

    """
    @TODO:
    A GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<cat_id>/questions", methods=['GET'])
    def get_questions_by_cat_id(cat_id):
        questions = Question.query.filter(Question.category == cat_id).order_by(Question.id).all()

        if len(questions) == 0:
            abort(404)

        formatted_questions = [question.format() for question in questions]
        cur_cat_string = ""
        if len(questions) > 0:
            cur_cat_string = _get_cur_category_string(formatted_questions[0]['category'])

        return jsonify({"questions": formatted_questions, "totalQuestions": len(questions),
                        "currentCategory": cur_cat_string}), 200

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """    
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({"success": False,
                        "message": 'Bad Request',
                        "error": 400
                        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,
                        "message": 'Resource Not Found',
                        "error": 404
                        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({"success": False,
                        "message": 'Unprocessable entity',
                        "error": 422
                        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"success": False,
                        "message": 'Internal Server Error',
                        "error": 500
                        }), 500

    return app
