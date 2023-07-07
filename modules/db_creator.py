import mysql.connector as connector
class creator():
    def __init__(self):
        try:
            self.con=connector.connect(host='localhost',port='3306',user='root',password='root')
            print("Successfully connected!")
            self.cur=self.con.cursor()
            stat=self.create_db()
            if stat.__bool__():
                try:
                    self.create_cols()
                except Exception as e:
                    print(e)
        except Exception as e:
            print(f"Connection failed :{e}")
    
    def create_db(self):
        self.cur.execute("Create database if not exists Users")
        self.cur.fetchall()
        print("(Users) Database created successfully")
        self.cur.execute("Use Users")
        return True
    def create_cols(self):
        self.cur.execute('''Create table if not exists Users(
                         id int auto_increment primary key,
                         user_name varchar(35) NULL,
                         password varchar(35)  NULL,
                         phone varchar(14) NULL
        )''')
        print("Created Table : Users")
        self.cur.close()
        self.con.close()

class check():
    def __init__(self,phone):
        ph=int(input(phone))
        self.con=connector.connect(host='localhost',port='3306',user='root',password='root')
        self.cur=self.con.cursor()
        self.cur.execute('Select phone from users where phone = %s',(ph,))
        result=self.cur.fetchall()
        if result == ph:
            return True
        else:
            return False