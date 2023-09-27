from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import openai
import yaml
import mysql.connector

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

database_config = config['database']
def create_database():
    conn = mysql.connector.connect(
        host=database_config['host'],
        user=database_config['user'],
        password=database_config['password'],
        database=database_config['database']
    )

    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), contract_text TEXT)''')
    conn.commit()
    conn.close()


app = Flask(__name__)


app.config.update(config)

# Initialize OpenAI
openai.api_key = app.config['openai_api_key']
app.secret_key = app.config['openai_api_key']

def is_real_estate_related(input_text):
    # Define keywords related to real estate
    real_estate_keywords = ['add','put','property', 'price', 'purchase', 'money', 'clause', 'dollars', 'currency', 'real estate', 'plot', 'building',
        'contract', 'clauses',
        'land', 'house', 'apartment', 'mortgage', 'tenant', 'landlord',
        'rent', 'lease', 'title deed', 'zoning', 'appraisal', 'valuation',
        'valuation report', 'closing costs', 'escrow', 'foreclosure',
        'home inspection', 'home appraisal', 'listing agent', 'buyer agent',
        'escrow officer', 'title company', 'title insurance', 'surveyor',
        'land survey', 'deed', 'easement', 'encumbrance', 'lien', 'lease agreement',
        'rental agreement', 'property tax', 'condominium', 'co-op',
        'homeowner association', 'HOA fees', 'land use', 'land development',
        'building codes', 'zoning laws', 'property management', 'real estate agent',
        'real estate broker', 'buyer', 'seller', 'investment property', 'rehabilitation',
        'flip property', 'flipper', 'home improvement', 'renovation', 'capital gains',
        'rental income', 'property value', 'appraiser', 'home inspector',
        ' closing date', 'earnest money', 'down payment', 'listing price', 'asking price']

    return any(keyword in input_text.lower() for keyword in real_estate_keywords)

def save_user_to_database(username, password):
    conn = mysql.connector.connect(
        host=database_config['host'],
        user=database_config['user'],
        password=database_config['password'],
        database=database_config['database']
    )
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

    cursor.close()
    conn.close()


def save_generated_contract_to_database(generated_contract):
    conn = mysql.connector.connect(
        host=database_config['host'],
        user=database_config['user'],
        password=database_config['password'],
        database=database_config['database']
    )
    cursor = conn.cursor()

    update_query = """
        UPDATE users
        SET contract_text = %s
        WHERE username IS NOT NULL
          AND password IS NOT NULL
          AND contract_text IS NULL
    """

    cursor.execute(update_query, (generated_contract,))
    conn.commit()

    cursor.close()
    conn.close()

@app.route('/back_to_login')
def back_to_login():
    return redirect(url_for('login'))

@app.route('/feedback', methods=['POST'])
def feedback():
    selected_rating = request.json['rating']

    return jsonify({'message': f'Thank you for providing feedback! You rated {selected_rating} stars.'})

@app.route('/save_contract', methods=['POST'])
def save_contract():
    generated_contract = session.get('generated_contract')

    if generated_contract:
        save_generated_contract_to_database(generated_contract)
        return jsonify({'message': 'Contract saved successfully'})
    else:
        return jsonify({'message': 'No generated contract found'})


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    save_user_to_database(username, password)

    return redirect(url_for('index'))

@app.route('/index')
def index():
    session['conversation_history'] = []  # Initialize conversation history
    initial_system_message = "Please provide your preferences or specific clauses you would like to add in the contract."

    # Append the initial system message to the conversation history
    session['conversation_history'].append({'role': 'system', 'content': initial_system_message})

    return render_template('index.html', initial_system_message=initial_system_message)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    app.secret_key = app.config['openai_api_key']
    user_input = request.json['user_input']

    if 'conversation_history' not in session:
        session['conversation_history'] = []

    if not is_real_estate_related(user_input):
        return jsonify({'user_message': user_input, 'system_message': 'We only generate contracts related to the real estate domain.'})

    conversation_history = session['conversation_history']

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": 'You are a real estate agent. Generate a well-defined real estate contract tailored to user input. Include relevant clauses as a real estate agent would, all numbered.'},
            *conversation_history,  # Include the entire conversation history
            {"role": "user", "content": user_input}  # Add the current user input
        ]
    )

    generated_contract = response.choices[0]['message']['content']

    session['generated_contract'] = generated_contract

    conversation_history.append({'role': 'user', 'content': user_input})
    conversation_history.append({'role': 'assistant', 'content': generated_contract})
    return jsonify({
        'user_message': user_input,
        'system_message': generated_contract
    })


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
