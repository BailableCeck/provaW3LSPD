"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves as the frontend for the project.
"""

from flask import Flask, render_template
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'  # Replace with the actual URL of your FastAPI backend
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'


class QueryForm(FlaskForm):
    person_name = StringField('Person Name:')
    submit = SubmitField('Get Birthday from FastAPI Backend')


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Fetch the date from the backend
    
    return render_template('index.html')

@app.route('/padova')
def padova():
    return render_template('padova.html')

@app.route('/venezia')
def venezia():
    return render_template('venezia.html')

@app.route('/verona')
def verona():
    return render_template('verona.html')

@app.route('/belluno')
def belluno():
    return render_template('belluno.html')

@app.route('/treviso')
def treviso():
    return render_template('treviso.html')

@app.route('/vicenza')
def vicenza():
    return render_template('vicenza.html')

@app.route('/rovigo')
def rovigo():
    return render_template('rovigo.html')

@app.route('/internal', methods=['GET', 'POST'])
def internal():
    """
    Render the internal page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = QueryForm()
    error_message = None  # Initialize error message

    if form.validate_on_submit():
        comune = form.person_name.data  # Modifica il nome del campo nel form

        # Make a GET request to the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{comune}'  # Aggiorna l'URL per includere il comune
        response = requests.get(fastapi_url)
        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            accomodations = data.get('denominazione_alloggio', [])
            result = ', '.join(accomodations) if accomodations else f'No accomodations available for {comune}'
            return render_template('internal.html', form=form, result=result, error_message=error_message)
        else:
            error_message = f'Error: Unable to fetch accommodation for {comune} from FastAPI Backend'

    return render_template('internal.html', form=form, result=None, error_message=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
