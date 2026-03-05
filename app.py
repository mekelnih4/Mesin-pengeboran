import sqlite3

# Global variables for X and Y offsets
def get_offsets():
    return 10, 20  # Replace with actual logic to get offsets

# Database interaction
class Database:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS offsets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x_offset REAL,
                y_offset REAL
            )''')

    def insert_offsets(self, x_offset, y_offset):
        with self.conn:
            self.conn.execute('''INSERT INTO offsets (x_offset, y_offset) VALUES (?, ?)''', (x_offset, y_offset))

    def fetch_offsets(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT x_offset, y_offset FROM offsets')
        return cursor.fetchall()

# Main application logic
if __name__ == '__main__':
    database = Database('offsets.db')
    x_offset, y_offset = get_offsets()
    database.insert_offsets(x_offset, y_offset)
    offsets = database.fetch_offsets()
    print(f'Inserted offsets: {offsets}')
