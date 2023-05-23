import os
import psycopg2
import psycopg2.extras

config = {
    'user': os.environ["POSTGRES_USER"],
    'password': os.environ["POSTGRES_PASSWORD"],
    'host': "postgres",
    'dbname': os.environ["POSTGRES_DB"],
}

def read_db(request):
    # Connect to the database
    cnx = psycopg2.connect(**config)
    cursor = cnx.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Execute the query to read the table
    cursor.execute(request)

    # Fetch all the rows as a list of dictionaries
    rows = [dict(row) for row in cursor.fetchall()]

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return rows

def update_db(request, data):
    # Connect to the database
    cnx = psycopg2.connect(**config)
    cursor = cnx.cursor()

    # Execute the query to update the table
    cursor.execute(request, data)

    # Commit the changes
    cnx.commit()

    # Get the number of affected rows
    affected_rows = cursor.rowcount

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return affected_rows
