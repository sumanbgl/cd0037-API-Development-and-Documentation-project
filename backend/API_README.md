This document provides the summary of all the end points in Trivia application in terms of url, request and responses.

URL : `GET '/categories'`

Description: 
- Retrieves a map of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: No
- Returns: An object with a single key, categories, that contains an object of category_id: category_string key:value pairs.
- 
Sample Request:
- `GET '/categories'`
- 
Sample Response:
```json
{
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

URL: `GET '/questions?page=${integer}'`

Description:
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - of type integer. NOTE: if no value for page is passed, it will be defaulted to 1.
- Returns: An object with 10 paginated questions, total number of questions, object containing all categories, and current category string
- Returns: 404 http status code, if no more questions are found

Sample Request:
`GET '/questions?page=2'`

Sample Response:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "Which is the heaviest organ in human body?",
      "answer": "The Liver",
      "difficulty": 5,
      "category": 1
    }
  ],
  "totalQuestions": 50,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography"    
  },
  "currentCategory": "Science"
}
```

---

URL: `GET '/categories/${category_id}/questions'`

Description:
- Retrieves questions for a cateogry specified by category id in request argument
- Request Arguments: `category_id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string
- Returns: 404, if a non-existent category id is passed

Sample Request: `GET '/categories/5/questions`

Sample Response:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "Which is the heaviest organ in human body?",
      "answer": "The Liver",
      "difficulty": 5,
      "category": 1
    }
  ],
  "totalQuestions": 1,
  "currentCategory": "Science"
}
```

---

URL: `DELETE '/questions/${question_id}'`

Description:
- Deletes a specified question using the question id
- Request Arguments: `question_id` - of type integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Sends 200 status code for success.
- Returns: 404 status code, if non-existent question_id is passed.

Sample Request: `DELETE '/questions/20'`

---

URL: `POST '/quizzes'`

Description:
- This is used to fetch the next question to be displayed to the player in the game.
- Request: Sends a post request to get the next question.
- Returns: a single new question object with http status code 200.
- Returns: http status code 400 if quiz_category is missing in the request payload.

Sample Request Body:
```json
{
    "previous_questions": [1, 4, 21, 15],
    "quiz_category": {
      "id" : 1,
      "type": "Science" 
    }
 }
```

Sample Response:
```json
{
  "question": {
    "id": 20,
    "question": "Which is the heaviest organ in human body?",
    "answer": "The Liver",
    "difficulty": 5,
    "category": 1
  }
}
```

---

URL: `POST '/questions'`

Description:
- Sends a post request to create a new question
- Returns: Sends a JSON with created_question_id containing the id of the newly created question with http status code 200.
- Returns: http status code 422 if any of question, answer, difficulty, category is missing in request payload.

Sample Request Body:
```json
{
  "question": "In which year did Kapil Dev retire from Indian test cricket?",
  "answer": "1998",
  "difficulty": 1,
  "category": 5
}
```
Sample Response:
```json
{
  "created_question_id": 50
}
```
---

URL: `POST '/questions'`

Description:
- Sends a post request in order to search for questions by search term

Sample Request:
```json
{
  "searchTerm": "title"
}
```

- Returns: any array of questions, a number of totalQuestions satisfying search term with status code 200.

Sample Response:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "difficulty": 2,
      "category": 4
    }
  ],
  "totalQuestions": 50,
  "currentCategory": "History"
}
```
- Returns: http status code 400, if searchTerm is missing in the request payload.