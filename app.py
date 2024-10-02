import sqlite3
from flask import Flask, session, request, render_template, redirect, url_for, g, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/reset')
def reset():
    # Clear session to reset all progress (manual reset route)
    session.clear()
    return redirect(url_for('home'))

@app.route('/home')
def home():
    
    # Initialize levels in the desired order
    level_descriptions = {
        '1': 'Complete the connection task to proceed to the next task.',
        '2': 'Find binary, Decode binary to decimal, Decode alphabet from decimal, Arrange alphabet to a name and enter',
        '3': 'Use the directions in mirrored way to draw, then use the draw reference to find hidden image on the page',
        '4': 'Solve the final task to win the game.'
    }

    completed_levels = session.get('completed_levels', [])
    return render_template('home2.html', completed_levels=completed_levels, level_descriptions=level_descriptions)

@app.route('/complete_level/<level>')
def complete_level(level):
    if 'completed_levels' not in session:
        session['completed_levels'] = []

    if level not in session['completed_levels']:
        session['completed_levels'].append(level)

    session.modified = True  # Mark the session as modified
    return redirect(url_for('home'))

@app.route('/connection_task', methods=['GET', 'POST'])
def connection_task():
    error = {}
    correct_inputs = {}

    # Define the correct answers for each input field
    answers = {
        'input1': 'datascience',
        'input2': 'improve',
        'input3': 'searchengine',
        'input4': 'algorithm',
        'input5': 'result',
        'input6': 'datascience improve searchengine algorithm result'  # Replace with the correct sentence
    }

    if request.method == 'POST':
        # Check if each input is correct or incorrect
        for i in range(1, 6):
            input_val = request.form.get(f'input{i}')
            if input_val.lower() == answers[f'input{i}'].lower():
                correct_inputs[f'input{i}'] = True  # Mark as correct
            else:
                error[f'input{i}'] = f'Incorrect input for word {i}'
        
        # Check if the final sentence (input6) is correct
        input6_val = request.form.get('input6')
        if input6_val and input6_val.lower() == answers['input6'].lower():
            return redirect(url_for('complete_level', level='1'))  # Move to next level
        elif input6_val:
            error['input6'] = "Try again"

    return render_template('connection.html', error=error, correct_inputs=correct_inputs)


@app.route('/decode_task', methods=['GET', 'POST'])
def decode_task():
    if request.method == 'POST':
        final_input = request.form.get('finalInput')
        if final_input and final_input.lower() == 'steve':
            return redirect(url_for('complete_level', level='2'))  # Mark Level 2 complete
        else:
            return render_template('decode_task1.html', error="Incorrect final answer. Please try again!")
    return render_template('decode_task1.html')

@app.route('/image_task', methods=['GET', 'POST'])
def image_task():
    if request.method == 'POST':
        user_input = request.form.get('user_input')  # Get the user input from the form
        if user_input and user_input.lower() == 'rotcaercra':
            return redirect(url_for('complete_level', level='3'))  # Mark Level 3 complete
        else:
            return render_template('image_task.html', error="Incorrect answer. Try again.")  # Render with an error message
    return render_template('image_task.html')



@app.route('/final_task', methods=['GET', 'POST'])
def final_task():
    if request.method == 'POST':
        locker_input = request.form.get('lockerInput')
        user_answer = request.form.get('userAnswer')
        
        
        # Check the locker code
        if locker_input:
            if locker_input == "3512":
                flash("Shift all letter 1 forward : 'HQNMLZM' , & enter into box")
            else:
                flash("Incorrect number!", "error")
        
        # Check the user answer
        if user_answer:
            if user_answer.lower() == "ironman":
                return render_template('final_task1.html', correct=True)
            else:
                flash("Please enter the correct answer!", "error")
    
    return render_template('final_task1.html', correct=False)

@app.route('/endpage')
def endpage():
    return render_template('endpage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
