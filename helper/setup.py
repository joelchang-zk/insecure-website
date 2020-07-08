import psycopg2
import os

def setUpDB():
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    return connection
