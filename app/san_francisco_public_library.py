
import mysql.connector

config = {
        "user" : "root",
        "password" : "MyFunP@ssw0rd",
        "host" : "127.0.0.1",
        "database" : "san_francisco_public_library"
        }
connection = mysql.connector.connect(**config)

def execute_operation(operation):
    if (operation == "exit"):
        return False
    elif(operation == "0"):
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")

        print("\nTables in this database:")
        for table in cursor.fetchall():
            print(table[0])

    return True


is_running = True
while (is_running):
    operation = input("\nWhat would you like to do?\n").casefold()
    is_running = execute_operation(operation)


connection.close()