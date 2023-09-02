from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

IP = "192.168.1.104"
PORT = "8000"

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Load user data from JSON file
with open('users.json', 'r') as file:
    users_data = json.load(file)

with open('data/questions.json', 'r') as questions_file:
    questions = json.load(questions_file)

with open('data/scores.json', 'r') as scores_file:
    scores = json.load(scores_file)

# Helper function to check user credentials
def check_credentials(username, password):
    for user in users_data['users']:
        if user['username'] == username and user['password'] == password:
            return True
    return False




@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if request.method == 'POST':
        code = request.form.get('code')
        question_id = int(request.form.get('question_id'))

        # Get test cases for the selected question
        test_cases = questions[question_id]['test_cases']

        # Run the code against test cases
        results = True # temp

        # Update user scores based on the results
        if all(results):
            username = 'user'  # Replace with the actual username of the user
            scores[username][question_id] = True  # Update the score

        # Save updated scores to the scores.json file
        with open('data/scores.json', 'w') as scores_file:
            json.dump(scores, scores_file, indent=4)

        return jsonify(results)

    return render_template('index.html', questions=questions)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

app.run(host= IP, port = PORT, debug= False)