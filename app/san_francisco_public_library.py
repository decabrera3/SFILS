
import mysql.connector
import pandas as pd

RESET_COLOR = "\033[0m"
RED_COLOR = "\033[31m"
YELLOW_COLOR = "\033[33m"
CYAN_COLOR = "\033[36m"
GREEN_COLOR = "\033[32m"

SHOW_TABLES_COMMAND = "0"
QUERY_TABLE_COMMAND = "1"
CUSTOM_COMMAND = "2"
CUSTOM_QUERY_COMMAND = "3"
RESET_DATABASE_COMMAND = "100"
HELP_COMMAND = "help"
EXIT_COMMAND = "exit"
TEST_COMMAND = "test"

DATABASE = "san_francisco_public_library"

config = {
        "user" : "root",
        "password" : "MyFunP@ssw0rd",
        "host" : "127.0.0.1",
        "database" : DATABASE
        }
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

data = pd.DataFrame()

def get_boolean_input(prompt: str = ""):

    print(f"{prompt} [{CYAN_COLOR}y{RESET_COLOR},{CYAN_COLOR}N{RESET_COLOR}]")
    answer = input(f"   > {YELLOW_COLOR}").casefold()
    print(RESET_COLOR, end="")
    if (answer == "y" or answer == "yes"):
        return True
    return False

def print_command(command: int, description: str):
    num_of_spaces = len(command)

    for i in range(5 - num_of_spaces):
        print(" ", end="")
    print(f"{CYAN_COLOR} {command} {RESET_COLOR} | {description}")

def print_help():

    print("Command | Description")
    print("--------------------------------------------")
    print_command(SHOW_TABLES_COMMAND, "Shows all the tables in the database.")
    print_command(QUERY_TABLE_COMMAND, "Shows all the data from a table.")
    print_command(CUSTOM_COMMAND, "Execute command directly into MySQL server.")
    print_command(CUSTOM_QUERY_COMMAND, "Execute command directly into MySQL server and print output.")
    print_command(RESET_DATABASE_COMMAND, "Clears the database and adds all data to it.")
    print()
    print_command(HELP_COMMAND, "Prints all the available commands.")
    print_command(EXIT_COMMAND, "Exits the program.")

def print_formated_table():
    query = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    print(query.to_markdown(index=False, tablefmt="psql"))

def does_table_exist(table_name: str):

    cursor.execute("SHOW TABLES")
    for table in cursor.fetchall():
        if (table[0] == table_name.upper()):
            return True
    return False

def insert_patron_type():

    if (not does_table_exist("PATRON_TYPE")):
        print(f"{RED_COLOR}Insertion Failed: PATRON_TYPE does not exist.{RESET_COLOR}")
        return False

    code = 0
    description = "test"

    cursor.execute(f"INSERT INTO PATRON_TYPE (PatronTypeCode, PatronTypeDescription) VALUES ({code}, \"{description}\");")
    return True

def reset_database():
    global data

    if (not get_boolean_input("This may potentially corrupt the database. Continue?")):
        return

    print("Opening data file...")
    data = pd.read_excel("../Data.xlsx")

    print("Clearing database...")
    cursor.execute("SHOW TABLES")
    tables = []
    for table in cursor.fetchall():
        tables.append(table[0])

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in tables:
        cursor.execute(f"TRUNCATE TABLE {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    print("Inserting data into database...")
    if (not insert_patron_type()):
        print(f"{RED_COLOR}Aborting database insertion{RESET_COLOR}")
        return

    print(f"{GREEN_COLOR}Operation Completed Succesfully{RESET_COLOR}")

def query_table():

    query_table = input(f"Which table would you like to query?\n   > {YELLOW_COLOR}").upper()
    print(RESET_COLOR, end="")

    if (not does_table_exist(query_table)):
        print(f"{RED_COLOR}Invalid Table.{RESET_COLOR}")
        return

    cursor.execute(f"SELECT * FROM {query_table}")
    print_formated_table()


def execute_operation(operation):

    if (operation == EXIT_COMMAND):
        return False
    
    elif (operation == HELP_COMMAND):
        print_help()
    
    elif(operation == SHOW_TABLES_COMMAND):
        cursor.execute("SHOW TABLES")

        print("\nTables in this database:")
        for table in cursor.fetchall():
            print(table[0])
    
    elif (operation == QUERY_TABLE_COMMAND):
        query_table()
    
    elif (operation == RESET_DATABASE_COMMAND):
        reset_database()
    
    elif (operation == "test"):
        print(data.head(8))
    
    else:
        print(f"{RED_COLOR}Invalid Command.{RESET_COLOR}")

    return True


print_help()

is_running = True
while (is_running):

    operation = input(f"\nWhat would you like to do?\n>> {YELLOW_COLOR}").casefold()
    print(RESET_COLOR, end="")
    is_running = execute_operation(operation)


connection.close()