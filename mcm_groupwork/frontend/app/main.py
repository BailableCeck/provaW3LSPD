"""
Frontend module for the Flask application.

This module defines a simple Flask application that 
serves as the frontend for the project.
"""

from flask import Flask, render_template
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

"""Configuration for the FastAPI backend URL."""
FASTAPI_BACKEND_HOST = 'http://backend'
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'

class QueryForm(FlaskForm):
    """
    Form class to handle query input from the user.
    """

    person_name = StringField('Destination:')
    piscina_checkbox = BooleanField('Piscina Checkbox')
    accesso_disabili_checkbox = BooleanField('Accesso Disabili Checkbox')
    fitness_checkbox = BooleanField('Fitness Checkbox')
    sauna_checkbox = BooleanField('Sauna Checkbox')
    aria_condizionata_checkbox = BooleanField('Aria Condizionata Checkbox')
    animali_amessi_checkbox = BooleanField('Animali Ammessi Checkbox')
    submit = SubmitField('Search')


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Fetch the data from the backend
    return render_template('index.html')


@app.route('/padova')
def padova():
    """
    Render the Padova page.

    Returns:
        str: Rendered HTML content for the Padova page.
    """
    return render_template('padova.html')


@app.route('/venezia')
def venezia():
    """
    Render the Venezia page.

    Returns:
        str: Rendered HTML content for the Venezia page.
    """
    return render_template('venezia.html')


@app.route('/verona')
def verona():
    """
    Render the Verona page.

    Returns:
        str: Rendered HTML content for the Verona page.
    """
    return render_template('verona.html')


@app.route('/belluno')
def belluno():
    """
    Render the Belluno page.

    Returns:
        str: Rendered HTML content for the Belluno page.
    """
    return render_template('belluno.html')


@app.route('/treviso')
def treviso():
    """
    Render the Treviso page.

    Returns:
        str: Rendered HTML content for the Treviso page.
    """
    return render_template('treviso.html')


@app.route('/vicenza')
def vicenza():
    """
    Render the Vicenza page.

    Returns:
        str: Rendered HTML content for the Vicenza page.
    """
    return render_template('vicenza.html')


@app.route('/rovigo')
def rovigo():
    """
    Render the Rovigo page.

    Returns:
        str: Rendered HTML content for the Rovigo page.
    """
    return render_template('rovigo.html')


@app.route('/internal', methods=['GET', 'POST'])
def internal():
    """
    Render the internal search page.

    Returns:
        str: Rendered HTML content for the internal search page.
    """
    form = QueryForm()
    error_message = None

    if form.validate_on_submit():
        comune = form.person_name.data

        """Obtain checkbox's values from form."""
        piscina_filter = form.piscina_checkbox.data
        accesso_disabili_filter = form.accesso_disabili_checkbox.data
        fitness_filter = form.fitness_checkbox.data
        sauna_filter = form.sauna_checkbox.data
        aria_condizionata_filter = form.aria_condizionata_checkbox.data
        animali_amessi_filter = form.animali_amessi_checkbox.data

        """Update URL to include filters"""
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{comune}?piscina={piscina_filter}&accesso_disabili={accesso_disabili_filter}&fitness={fitness_filter}&sauna={sauna_filter}&aria_condizionata={aria_condizionata_filter}&animali_ammessi={animali_amessi_filter}'

        """Make a GET request to the FastAPI backend."""
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            """Extract and display the result from the FastAPI backend."""
            data = response.json()
            accomodations = data.get('risultati', [])

            if accomodations:
                result_strutture = []
                for struttura in accomodations:
                    if "link" in struttura:
                        result_strutture.append({"nome": struttura["nome"], "link": struttura["link"]})
                    else:
                        result_strutture.append({"nome": struttura["nome"]})

                # Debug print to check the value of result_strutture
                print("Result_strutture:", result_strutture)

                if not result_strutture:
                    result_strutture = [{"nome": f'No accommodations available for {comune}'}]
            else:
                result_strutture = [{"nome": f'No accommodations available for {comune}'}]

            """Extract museum's information."""
            musei_consigliati = data.get('musei_consigliati', [])
            result_musei = ', '.join(musei_consigliati) if musei_consigliati else f'No recommended museums for {comune}'

            return render_template('internal.html', form=form, result_strutture=result_strutture, result_musei=result_musei, error_message=error_message)
        else:
            error_message = f'Error: Unable to fetch accommodations for {comune} from FastAPI Backend'

    return render_template('internal.html', form=form, result_strutture=None, result_musei=None, error_message=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

