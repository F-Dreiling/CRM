import sys
import django
import mysql.connector

print(sys.version)
print(django.get_version())
print(mysql.connector.__version__)

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = ''
)

cursorObject = database.cursor()

#cursorObject.execute("DROP DATABASE testing")