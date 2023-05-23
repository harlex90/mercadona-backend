import os
import mysql.connector

config = {
    'user': os.environ["MYSQL_USER"],
    'password': os.environ["MYSQL_PASSWORD"],
    'host': "mysql",
    'database': os.environ["MYSQL_DATABASE"],
}

def read_db(request):
    # Connect to the database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Execute the query to read the table
    cursor.execute(request)

    # Fetch all the rows as a list of dictionaries
    rows = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return rows
