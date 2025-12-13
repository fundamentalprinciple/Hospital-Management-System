If you're unfamiliar with python development, follow these steps to run my webapp:
1) Clone the repo
2) Make a python3 virtual environment (run this command for ubuntu: python3 -m venv [name of the venv])
3) Activate the venv (run: source [name of the venv]/bin/activate)
4) Install the python dependancies (run: pip install -r requirements.txt )
5) Set up your own environment variables (run: echo -e 'SECRET_KEY="put_a_very_long_random_string_here"\nSECURITY_PASSWORD_SALT="put_another_very_long_random_string_here"\nADMIN_PASSWORD="strong_admin_password_here"' > .env )

6) Run: py main.py
7) In a browser, visit: http://localhost:8000
