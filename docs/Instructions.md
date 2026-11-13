# Project Documentation

### Part A) Setup
This documentation assumes that you are running Linux (specifically Ubuntu) on your device. You should also have the following software:
- MySQL
- MySQL Workbench
- Python 3
- Git

### Part B) Creating the Database

1. Clone the repository.
2. Start MySQL Workbench.
3. Connect to your localhost.
4. Open the *san_francisco_public_library.sql* file in your localhost. The file is located in the script directory.
5. Run the script.

### Part C) Run the Program

1. Open the Terminal.
2. Navigate to the directory in which the project is located
3. Create a Python Virtual Environment by executing the command:`python3 -m venv .venv`
4. Then, activate the Virtual Environment by executing the command: `source .venv/bin/activate`
5. Install the following Python packages while the Virtual Environment is active by running `pip install [package_name]`:
- mysql-connector-python
- pandas
- python-dotenv
- tabulate
- openpyxl

6. Next, create an file for holding environmental variables. Execute the command `touch .env`
7. Edit the *.env* file by executing the command: `nano .env`
8. Inside, write: `MYSQL_ROOT_PASSWORD=[password]`. Replace `[password]` with your actual password for the root user.
9. Save and exit the file.
10. change your working directory to the app directory.
11. Run the program by executing the command: `python3 san_francisco_public_library.py`
12. If this is your first time running the program, enter `100` then `y` to add all data to the database.
13. Enter `2` followed by the age range code to get stats about that age range.
14. Enter `exit` to end the program.
