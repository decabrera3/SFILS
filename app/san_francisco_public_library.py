
import mysql.connector
import pandas as pd
import os
from time import perf_counter
from dotenv import load_dotenv

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

DATABASE = "san_francisco_public_library"

PATRON_TYPE = {
    "table": "PATRON_TYPE",
    "database code": "PatronTypeCode",
    "database description": "PatronTypeDescription",
    "file code": "Patron Type Code\npatron_type_code",
    "file description": "Patron Type Definition\n"
}
NOTIFICATION_MEDIUM = {
    "table": "NOTIFICATION_MEDIUM",
    "database code": "NotificationMediumCode",
    "database description":"NotificationDescription",
    "file code": "Notification Preference Code\nnotification_medium_code",
    "file description": "Notification Code Definition"
}
HOME_LIBRARY = {
    "table": "HOME_LIBRARY",
    "database code": "HomeLibraryCode",
    "database description": "HomeLibraryDescription",
    "file code": "Home Library Code\nhome_library_code",
    "file description":"Home Library Definition\n"
}
AGE_RANGE = {
    "table": "AGE_RANGE",
    "database code": "AgeRangeCode",
    "database description": "AgeRangeDescription",
    "file code": "Age Range\n",
    "file description": "Age Range\n"
}
PATRON = {
    "table": "PATRON"
}

load_dotenv()

config = {
        "user": "root",
        "password": os.environ.get("MYSQL_ROOT_PASSWORD"),
        "host": "127.0.0.1",
        "database": DATABASE
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

def does_table_exist(table_name: str) -> bool:

    cursor.execute("SHOW TABLES")
    for table in cursor.fetchall():
        if (table[0] == table_name.upper()):
            return True
    return False

def insert_basic_table(table: dict, is_string: bool) -> bool:

    used_codes = set()

    if (not does_table_exist(table["table"])):
        print(f"{RED_COLOR}Insertion Failed: {table["table"]} does not exist.{RESET_COLOR}")
        return False

    command = f"INSERT INTO {table["table"]} ({table["database code"]}, {table["database description"]}) VALUES (%s, %s);"

    for i in range(len(data)):

        code = data.at[i, table["file code"]]
        if (not is_string):
            code = int(code)

        if (code in used_codes):
            continue
        used_codes.add(code)
        description = data.at[i, table["file description"]]
        cursor.execute(command, (code, description))

    connection.commit()
    return True

def insert_age_range() -> bool:

    used_age_ranges = set()

    if (not does_table_exist(AGE_RANGE["table"])):
        print(f"{RED_COLOR}Insertion Failed: {AGE_RANGE["table"]} does not exist.{RESET_COLOR}")
        return False

    command = f"INSERT INTO {AGE_RANGE["table"]} ({AGE_RANGE["database code"]}, {AGE_RANGE["database description"]}) VALUES (%s, %s);"

    for i in range(len(data)):

        age_range = data.at[i, AGE_RANGE["file code"]]

        if ((age_range in used_age_ranges) or (age_range == "")):
            continue
        used_age_ranges.add(age_range)
        cursor.execute(command, (len(used_age_ranges), age_range))

    connection.commit()
    return True

def insert_patron() -> bool:

    if (not does_table_exist("PATRON")):
        print(f"{RED_COLOR}Insertion Failed: PATRON does not exist.{RESET_COLOR}")
        return False

    command = f"""
    INSERT INTO PATRON (PatronTypeCode, AgeRangeCode, NotificationPreference, HomeLibraryCode,
    CheckoutTotal, RenewalTotal, CirculationActiveMonth, CirculationActiveYear, ProvidedEmailAddress, WithinSanFranciscoCounty, YearPatronRegistered
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    months = {
        "January": "0",
        "February": "1",
        "March": "2",
        "April": "3",
        "May": "4",
        "June": "5",
        "July": "6",
        "August": "7",
        "September": "8",
        "October": "9",
        "November": "10",
        "December": "11"
    }

    age_ranges = {}

    cursor.execute("SELECT * FROM AGE_RANGE")
    for i in cursor.fetchall():
        age_ranges[i[1]] = i[0]

    for i in range(len(data)):
        patron_type_code = int(data.at[i, PATRON_TYPE["file code"]])
        age_range_code = data.at[i, AGE_RANGE["file code"]]
        if ((age_range_code != None) and (age_range_code != '')):
            age_range_code = age_ranges[age_range_code]
        else:
            age_range_code = None

        notification_preference = data.at[i, NOTIFICATION_MEDIUM["file code"]]
        home_library_code = data.at[i, HOME_LIBRARY["file code"]]
        
        checkout_total = int(data.at[i, "Total Checkouts\ncheckout_total"])
        renewal_total = int(data.at[i, "Total Renewals\nrenewal_total"])
        circulation_active_month = 0
        circulation_active_year = 0
        if ((data.at[i, "Circulation Active Month\n"] != "") and (data.at[i, "Circulation Active Month\n"] != " ")):
            circulation_active_month = int(months[data.at[i, "Circulation Active Month\n"]])
        else:
            circulation_active_month = None
        if (data.at[i, "Circulation Active Year\n"] != ""):
            circulation_active_year = int(data.at[i, "Circulation Active Year\n"])
        else: circulation_active_year = None
        provided_email_address = data.at[i, "Provided Email Address\n"]
        within_san_francisco_county = data.at[i, "Within San Francisco County"]
        year_patron_registered = int(data.at[i, "Year Patron Registered"])

        cursor.execute(command, (patron_type_code, age_range_code, notification_preference, home_library_code, 
                       checkout_total, renewal_total, circulation_active_month, circulation_active_year, 
                       provided_email_address, within_san_francisco_county, year_patron_registered))

    connection.commit()
    return True

def reset_database():
    global data

    if (not get_boolean_input("This may potentially corrupt the database. Continue?")):
        return

    start_time = perf_counter()

    print("Opening data file...")
    data = pd.read_excel("../Data.xlsx", keep_default_na=False)

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
    if (not insert_basic_table(PATRON_TYPE, False)):
        print(f"{RED_COLOR}Aborting database insertion{RESET_COLOR}")
        return
    if (not insert_age_range()):
        print(f"{RED_COLOR}Aborting database insertion{RESET_COLOR}")
        return
    if (not insert_basic_table(NOTIFICATION_MEDIUM, True)):
        print(f"{RED_COLOR}Aborting database insertion{RESET_COLOR}")
        return
    if (not insert_basic_table(HOME_LIBRARY, True)):
        print(f"{RED_COLOR}Aborting database insertion{RESET_COLOR}")
        return
    if (not insert_patron()):
        print(f"{RED_COLOR}Aborting database insertion{RESET_COLOR}")
        return

    stop_time = perf_counter()
    total_time = stop_time - start_time
    print(f"<{total_time:.2f}>")

    print(f"{GREEN_COLOR}Operation Completed Succesfully{RESET_COLOR}")

def query_table():

    query_table = input(f"Which table would you like to query?\n   > {YELLOW_COLOR}").upper()
    print(RESET_COLOR, end="")

    start_time = perf_counter()

    if (not does_table_exist(query_table)):
        print(f"{RED_COLOR}Invalid Table.{RESET_COLOR}")
        return

    cursor.execute(f"SELECT * FROM {query_table}")
    print_formated_table()

    stop_time = perf_counter()
    total_time = stop_time - start_time
    print(f"<{total_time:.2f}>")

def show_tables():

    start_time = perf_counter()
        
    cursor.execute("SHOW TABLES")

    print("\nTables in this database:")
    for table in cursor.fetchall():
        print(table[0])

        
    stop_time = perf_counter()
    total_time = stop_time - start_time
    print(f"<{total_time:.2f}>")


def execute_operation(operation):

    if (operation == EXIT_COMMAND):
        return False
    
    elif (operation == HELP_COMMAND):
        print_help()
    
    elif(operation == SHOW_TABLES_COMMAND):
        show_tables()
    
    elif (operation == QUERY_TABLE_COMMAND):
        query_table()
    
    elif (operation == RESET_DATABASE_COMMAND):
        reset_database()
    
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