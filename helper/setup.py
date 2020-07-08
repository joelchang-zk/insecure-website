import psycopg2

def setUpDB():
    connection = psycopg2.connect(user="postgres", password="Jczk1241", host="localhost", port="5432", database="postgres")
    return connection