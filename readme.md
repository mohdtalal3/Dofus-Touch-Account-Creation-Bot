# Dofus Touch Account Creation Bot

This bot automates the process of creating and setting up Dofus Touch accounts. It uses Selenium WebDriver to interact with web pages and Streamlit for the user interface.

## Prerequisites

- Python 3.7+
- Chrome browser

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/mohdtalal3/Dofus-Touch-Account-Creation-Bot.git
    ```
    ```bash
    cd dofus-touch-account-bot
    ```
2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```

    ```bash
    venv\Scripts\activate
    ```
3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
## Usage

1. Prepare your input files:
- `outlook_accounts.txt`: List of Outlook accounts (format: `email:password`, one per line)
- `GAME_NAMES.txt`: List of names to use for account creation (one per line)

2. Run the Streamlit app:

    ```bash
    streamlit run Bot_2.py
    ```
3. In the Streamlit interface:
- Choose the community (FR, ENG, or ES)
- Click "Start Bot" to begin the process

## File Descriptions

- `Bot_2.py`: Main script containing the bot logic and Streamlit interface
- `requirements.txt`: List of Python packages required to run the bot
- `outlook_accounts.txt`: Input file with Outlook account credentials
- `GAME_NAMES.txt`: Input file with names for account creation
- `verified_accounts.txt`: Output file for accounts that passed verification
- `success.txt`: Output file for accounts that completed the entire process successfully

## Output Files

- `verified_accounts.txt`: Contains email:password pairs for accounts that were successfully created and logged in.
- `success.txt`: Contains email:password pairs for accounts that completed the entire process without any errors or restrictions.

## Important Notes

- Ensure that `outlook_accounts.txt` and `GAME_NAMES.txt` are properly formatted and contain sufficient data before running the bot.
- The bot will modify `outlook_accounts.txt` during execution, removing processed accounts.
- Check `verified_accounts.txt` and `success.txt` for the results of the bot's operations.

## Troubleshooting

- If you encounter WebDriver errors, ensure that your ChromeDriver version matches your Chrome browser version.
- For any other issues, check the console output for error messages and stack traces.

Video Attached for setup.