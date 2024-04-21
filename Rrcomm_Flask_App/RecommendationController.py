from flask import Flask, render_template, request
import requests
import json
from _draw_pic_from_recipes import generate_pic_from_text


app = Flask(__name__, template_folder='./templates')
CLOUD_FUNCTION_URL = " <recommend_via_userID> url "

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Greeting controller
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Extract userId from the form data
        user_id = request.form.get('userId')

        # Make a GET request to the Cloud Function
        requestBody = {"userId": user_id}
        response = requests.post(CLOUD_FUNCTION_URL, json=requestBody)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            json_string = response.content.decode('utf-8')
            # Convert JSON string to dictionary
            data = json.loads(json_string)
            recipes_list = data.get("recipes", [])

            for recipe in recipes_list:
                description = recipe.get("description")
                recipe["picture"] = generate_pic_from_text(description)

            # Return the response data
            return render_template('recommend.html', data=recipes_list)
        else:
            # If the request was unsuccessful, return an error message
            return render_template('error.html', message="Error: Unable to fetch data from Cloud Function")
    except Exception as e:
        # If an exception occurs, return an error message
        return render_template('error.html', message="Error: " + str(e))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)