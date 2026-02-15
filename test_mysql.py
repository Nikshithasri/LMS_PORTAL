from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Geetha@77'
app.config['MYSQL_DB'] = 'lms_db'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DATABASE();")
    db = cursor.fetchone()
    return f"Connected to database: {db}"

if __name__ == "__main__":
    app.run(debug=True)
