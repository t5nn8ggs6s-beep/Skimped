import sqlite3
from datetime import datetime

class DaoBases_requests:
    
    def __init__(self):
        self.cont_2 = sqlite3.connect('request.db',check_same_thread=False)
        self.cursor_2 = self.cont_2.cursor()
        self.cursor_2.execute('''CREATE TABLE IF NOT EXISTS request
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id_2 INTEGER,
                 card_number_2 INTEGER,
                 date TEXT,
                 balance_2 REAL 
                    )''')
        self.cont_2.commit()
        
        
        
    def select_request(self,user_id):
        self.cursor_2.execute('SELECT date FROM request WHERE user_id_2=?',(user_id,))
        date = self.cursor_2.fetchone()
        return date
    
    
    
    def create_request(self,user_id,amount):
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor_2.execute('INSERT INTO request (user_id_2,balance_2,date) VALUES(?,?,?)',
                              (user_id,amount,date_now))
        self.cont_2.commit()

            
class DaoBases_main:
    
    def __init__(self):
        #Создаём базу данных sql
        self.conn = sqlite3.connect('main.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS main 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            card_number INTEGER,
            caption TEXT DEFAULT 'None',
            file_id TEXT DEFAULT 'None',
            balance REAL
            )''')
        self.conn.commit()
        
        
        
    def about_balance(self,user_id):
        self.cursor.execute("SELECT balance FROM main WHERE user_id = ?",(user_id,))
        balances = self.cursor.fetchone()
        return balances
    
    
    
    def insert_balance(self,user_id,balance):
        self.cursor.execute("INSERT INTO main (balance,user_id) VALUES (?,?)",
                       (balance,user_id))
        self.conn.commit()
        
        
        
    def update_balance(self,user_id):
        amount = 0.25
        self.cursor.execute("UPDATE main SET balance = balance + ? WHERE user_id = ?",
            (amount,user_id))
        self.conn.commit()
    
    
    
    
    def minus_balance(self,user_id,amount):
        self.cursor.execute('UPDATE main SET balance = balance - ? WHERE user_id = ?',
                            (amount,user_id)
        ) 
        
        
    
    
    def select_card(self,user_id):
        self.cursor.execute('SELECT card_number FROM main WHERE user_id=?',(user_id,))
        result = self.cursor.fetchone()
        return result
    

        
        
          
    def save_card(self,user_id,card_number):
        self.cursor.execute("UPDATE main SET card_number = ? WHERE user_id = ?",
            (card_number,user_id))
        self.conn.commit()
        
        
        
class  Databace_post:
    def __init__(self):
        #Создаём базу данных sql
        self.conn = sqlite3.connect('posts.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS posts
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            caption TEXT ,
            file_id TEXT
            )''')
        self.conn.commit()
        
        
        
    def post_post (self,file_id,caption):
        # Выполняем SQL-запрос для получения всех записей из базы данных
        self.cursor.execute("SELECT file_id,caption FROM posts ORDER BY RANDOM() LIMIT 1")
        rows = self.cursor.fetchall()
        if rows is not None:
            # Отправляем каждую запись в виде сообщения пользователю
            for row in rows:
                file_id = row[0]
                caption = row[1]
        return file_id,caption
    
    
    
    def add_post(self,file_id,caption):
        self.cursor.execute('INSERT INTO posts (file_id,caption) VALUES (?, ?)',
                (file_id,caption))
        self.conn.commit() 
    

    def delete_post(self, id):
        self.cursor.execute('DELETE FROM posts WHERE id = ?', 
                            (id,))
        self.conn.commit()
        
        
        
    def list_post(self):
        self.cursor.execute('SELECT id,file_id,caption FROM posts')
        result = self.cursor.fetchall()
        return result
        

        
        
