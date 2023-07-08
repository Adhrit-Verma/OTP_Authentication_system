import mysql.connector as connector
class creator:
    def __init__(self):
        try:
            self.con = connector.connect(host='localhost', port='3306', user='root', password='root')
            print("Successfully connected!")
            self.cur = self.con.cursor()
            self.create_db()
            self.create_cols()
        except connector.Error as e:
            print(f"Connection failed: {e}")

    def create_db(self):
        try:
            self.cur.execute("CREATE DATABASE IF NOT EXISTS Users")
            self.con.commit()
            print("(Users) Database created successfully")
            self.cur.execute("USE Users")
            self.con.commit()
        except connector.Error as e:
            print(f"Error creating database: {e}")

    def create_cols(self):
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_name VARCHAR(35) NULL,
                    password VARCHAR(35) NULL,
                    phone VARCHAR(14) NULL
                )
            ''')
            self.con.commit()
            print("Created Table: Users")
        except connector.Error as e:
            print(f"Error creating table: {e}")

        self.cur.close()
        self.con.close()


class check:
    def __init__(self, phone, password):
        self.ph = phone
        self.p = password
        self.con = connector.connect(host='localhost', port='3306', user='root', password='root', database="users")
        self.cur = self.con.cursor()
        self.cur.execute('SELECT phone FROM users WHERE phone = %s', (self.ph,))
        result = self.cur.fetchall()
        if self.ph in [row[0] for row in result]:
            self.result = self.pass_check()
        else:
            self.result = False

    def pass_check(self):
        self.cur.execute('SELECT password FROM users WHERE phone = %s', (self.ph,))
        result = self.cur.fetchall()
        if result and str(result[0][0]) == str(self.p):
            self.cur.close()
            self.con.close()
            return True
        else:
            self.cur.close()
            self.con.close()
            return False


    def get_result(self):
        return self.result


class db_check:
    def __init__(self, dbase):
        self.db = dbase
        try:
            con = connector.connect(host='localhost', port='3306', user='root', password='root')
            cur = con.cursor()
            cur.execute('SHOW DATABASES')
            results = cur.fetchall()
            self.db_exists = False
            for database in results:
                (database_name,) = database
                if database_name == self.db:
                    cur.execute('SHOW TABLES')
                    results=cur.fetchall()
                    for tables in results:
                        (table_name,)=tables
                        if table_name==self.db:
                            self.db_exists=True
                            break
                        else:
                            creator.create_cols()
                            self.db_exists=True
                            break
                    self.db_exists = True
                    break
        except Exception as e:
            print(f"Connection failed: {e}")

    def check_exists(self):
        return self.db_exists





        