"""Test MySQL Connection"""
from app import app
from app import mysql

if __name__ == "__main__":
    with app.app_context():
        try:
            cursor = mysql.cursor()
            cursor.execute('SELECT DATABASE();')
            result = cursor.fetchone()
            
            print('=' * 50)
            print('✓ MySQL Connection Successful!')
            print('=' * 50)
            print(f'Database: {result}')
            print(f'Host: {app.config["MYSQL_HOST"]}')
            print(f'User: {app.config["MYSQL_USER"]}')
            print(f'Port: 3306 (default)')
            print('=' * 50)
            
            # List tables
            cursor.execute('SHOW TABLES;')
            tables = cursor.fetchall()
            print(f'\nTables in database ({len(tables)} total):')
            for table in tables:
                print(f'  - {table}')
            
            cursor.close()
            print('\n✓ All systems ready!')
            
        except Exception as e:
            print(f'✗ Connection Error: {e}')
