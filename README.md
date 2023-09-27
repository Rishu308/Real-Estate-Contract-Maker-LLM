# Real Estate Contract Chat Bot LLM

Generate real estate contracts through conversational AI with an LLM.

## Installation

```bash
pip install Flask openai mysql-connector-python pyyaml
```
# Getting Started
- Run `run_contract_bot.bat` file.
- Enter your OpenAI secret key, MySQL configuration details in the command prompt that pops up.
- If it crashes after inputting config details, try running
  ```bash
  pip install urllib3==1.25.11```
- If you get a different error saying "open ai module does not exist" or "Flask module..." etc. then try running a virtual environment:
  ```bash
  cd <path where you extracted the project root directory>
  python -m venv venv
  source venv/bin/activate
  run_contract_bot.bat```
- If valid and everything runs, then type in the link that comes up in your browser to use the application.

# Usage
- Log in with a username and password for bookkeeping purposes.
- Click "Log In" to access the chatbot.
- Send a message specifying your real estate needs or wants.
   
    ## Example message:
    ```bash
    Generate a real estate contract for the following property:

    Property Details:
    Acreage: 5 acres
    Building: 3-storey
    Amenities: Attached pool
    Please include the following clauses as a real estate agent would, all numbered while leaving newline characters after each point for good presentation:

    Ownership and Title
    Purchase Price and Terms
    Closing Date and Possession
    Additional Terms (if any)
    ```

- The bot will generate a contract which can be further edited using further messaging.
- On the top right there is a button that toggles the menu.
- Click the "Save" to save your contract in the database under the table "users" along with your username and password in the same record.
- Click "Go back to login" to return to the login page.
- You can check the table "users" in your database to check what has been saved.

# Notes
- The bot may take 10-15 seconds to respond. Be specific and concise in your prompts.
- Ensure you have a valid OpenAI secret key and MySQL configuration details for smooth operation.
- At the moment, edit button is just for display.

# Troubleshooting
While trying to run the 'run_contract_bot.bat' file:
- Enter your OpenAI secret key, MySQL configuration details in the command prompt that pops up.
- If it crashes after inputting config details, try running
  ```bash
  pip install urllib3==1.25.11```
- If you get a different error saying "open ai module does not exist" or "Flask module..." etc. then try running a virtual environment:
  ```bash
  cd <path where you extracted the project root directory>
  python -m venv venv
  source venv/bin/activate
  run_contract_bot.bat```
- If valid and everything runs, then type in the link that comes up in your browser to use the application.

# License
MIT License




