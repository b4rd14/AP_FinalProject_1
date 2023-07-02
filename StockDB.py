import sqlite3 as sql

conn = sql.connect("StockMarket\stock.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, birth TEXT, balance REAL)")
conn.commit()
    
def add_user( user):
    if get_user(user.id) is None:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user.id, user.name, user.birth, user.balance))
        conn.commit()
        return True
    else:
        return False
def get_user(id):
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    row = cur.fetchone()
    if row is None:
        return None
    else:
        return User(row[0], row[1], row[2], row[3])


def update_user_balance( user):
    cur.execute("UPDATE users SET balance=? WHERE id=?", (user.balance, user.id))
    conn.commit()



class User :
    stocks = {"AAPL": 0, "AMZN": 0, "FB": 0, "GOOGL": 0, "TSLA": 0}
    history = []
    def __init__(self, id, name, birth, balance):
        self.id = id
        self.name = name
        self.birth = birth
        self.balance = balance
    

while True:
    print("1. Add User")
    print("2. Get User")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        id = int(input("Enter id: "))
        name = input("Enter name: ")
        birth = input("Enter birth: ")
        balance = float(input("Enter balance: "))
        user = User(id, name, birth, balance)
        if add_user(user):
            print("User added successfully")
        else:
            print("User already exists")
    elif choice == 2:
        id = int(input("Enter id: "))
        user = get_user(id)
        if user is None:
            print("User not found")
        else:
            print(user.id, user.name, user.birth, user.balance)
    elif choice == 3:
        break
    else:
        print("Invalid choice")
