import sqlite3


class Db:
    def __init__(self, db_name="freelance.db"):
        self.connection = sqlite3.connect(db_name)
        self.connection.isolation_level = None  # Автоматически фиксируем изменения
        self.cursor = self.connection.cursor()
        self.connection.execute('pragma foreign_keys=ON')

    def create_table_home(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS home (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT,
                    size REAL,
                    price REAL,
                    description TEXT
                );
            """)
            print("[INFO] Table home created successfully")

    def create_table_user(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT
                );
            """)
            print("[INFO] Table user created successfully")

    def create_table_order(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    home_id INTEGER,
                    user_id INTEGER,
                    date DATE,
                    status TEXT,
                    FOREIGN KEY (home_id) REFERENCES home(id),
                    FOREIGN KEY (user_id) REFERENCES user(id)
                );
            """)
            print("[INFO] Table orders created successfully")

    def insert_into_home(self, address, size, price, description):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO home (address, size, price, description)
                VALUES (?, ?, ?, ?)
            """, (address, size, price, description))
            print("[INFO] Data inserted into home table successfully")

    def select_home(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM home")
            rows = self.cursor.fetchall()
            return rows

    def select_home_name(self, address):
        with self.connection:
            self.cursor.execute("SELECT id FROM home WHERE address = ?", (address,))
            rows = self.cursor.fetchall()
            return rows

    def update_order_status(self, order_id, new_status):
        with self.connection:
            sql_query = "UPDATE orders SET status = ? WHERE id = ?"
            self.cursor.execute(sql_query, (new_status, order_id))

    def insert_into_orders(self, home_id, user_id, date, status):
        with self.connection:
            # Проверяем, существует ли бронирование на данную дату для данного дома
            self.cursor.execute("""
                SELECT * FROM orders 
                WHERE home_id = ? AND date = ?
            """, (home_id, date))
            existing_order = self.cursor.fetchone()

            # Если уже существует бронирование на эту дату, выводим ошибку
            if existing_order:
                print("[ERROR] Order for this home on this date already exists")
                raise ValueError("Order for this home on this date already exists")

            # Вставляем новое бронирование, если бронирование на эту дату ещё не существует
            self.cursor.execute("""
                INSERT INTO orders (home_id, user_id, date, status) 
                VALUES (?, ?, ?, ?)
            """, (home_id, user_id, date, status))
            print("[INFO] Order inserted successfully")

    def select_user(self, username):
        with self.connection:
            self.cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
            rows = self.cursor.fetchall()
            print(rows)
            return rows

    def select_orders_by_username(self, username):
        with self.connection:
            self.cursor.execute("""
                SELECT orders.id, home.address, orders.date, orders.status
                FROM orders
                JOIN user ON orders.user_id = user.id
                JOIN home ON orders.home_id = home.id
                WHERE user.username = ?;
            """, (username,))
            rows = self.cursor.fetchall()
            print(rows)
            return rows

    def select_all_orders_with_details(self):
        with self.connection:
            self.cursor.execute("""
                SELECT orders.id, home.address, user.username, orders.date, orders.status
                FROM orders
                JOIN home ON orders.home_id = home.id
                JOIN user ON orders.user_id = user.id;
            """)
            rows = self.cursor.fetchall()
            print(rows)
            return rows

    def select_home_by_address(self, address_word):
        with self.connection:
            self.cursor.execute("""
                SELECT * FROM home WHERE address LIKE ?;
            """, (f'%{address_word}%',))
            rows = self.cursor.fetchall()
            print(rows)
            return rows

    def add_user(self, username):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO user (username) VALUES (?);
            """, (username,))
            print(f"[INFO] User '{username}' added successfully")
db = Db()
# db.create_table_user()
# db.create_table_home()
# db.create_table_order()
# db.insert_into_home("Приволжский район, Фучика 21", 59, 3999, "Просторная квартира с двумя комнатами и балконом. Имеется стиральная машина, духовой шкаф, варочная панель, двуспальная кровать, диван и шкаф для одежды. Квартира уютная и имеет удобную планировку. Большая кухня с двумя санузлами, где установлены тёплые полы.")
# db.select_user('blinn0k')
# db.select_home()
# db.select_orders_by_username("blinn0k")
# db.update_order_status(1, "Одобрено")
# db.select_home_by_address('Приволжский')
db.add_user("blinn0k")