from first import DAL

class login:
    def __init__(self):
        self.dal = DAL()

    def select (self, username, password, db_path):
        query = f"SELECT * FROM TBLdata WHERE username = '{username}' AND password = '{password}';"
        message = self.dal.have_output(query, db_path)
        return message

class add:
    def __init__(self):
        self.dal = DAL()

    def insert (self, Name, Family, Math, Geographi, user_data):
        query = f"INSERT INTO {user_data[0][6][0:-3]} ('Name', 'Family', 'Math', 'geographi') VALUES ('{Name.title()}', '{Family.title()}',  {Math}, {Geographi});"
        message = self.dal.no_output(query, user_data[0][6])
        return message

class update:
    def __init__(self):
        self.dal = DAL()

    def update (self, Name, Family, Math, Geographi, student_id, user_data):
        query = f"UPDATE {user_data[0][6][0:-3]} SET 'Name' = '{Name.title()}', 'Family' = '{Family.title()}', 'Math' = {Math}, 'Geographi' = {Geographi} WHERE id = {student_id}"
        message = self.dal.no_output(query, user_data[0][6])
        return message

class show:
    def __init__(self):
        self.dal = DAL()

    def select (self, user_data):
        query = f"SELECT * FROM {user_data[0][6][0:-3]};"
        message = self.dal.have_output(query, user_data[0][6])
        return message

class search:
    def __init__(self):
        self.dal = DAL()

    def search (self, filter, condition, value, user_data):
        query = f"SELECT * FROM {user_data[0][6][0:-3]} WHERE"
        match condition:
            case "Ends with":
                query = f"{query} LOWER({filter}) LIKE '%{value.lower()}'"
            case "Starts with":
                query = f"{query} LOWER({filter}) LIKE '{value.lower()}%'"
            case "Contain":
                query = f"{query} LOWER({filter}) LIKE '%{value.lower()}%'"
            case "Equals":
                if filter in ("Name", "Family"):
                    query = f"{query} LOWER({filter}) = '{value.lower()}'"
                else:
                    query = f"{query} {filter} = {value}"
        message = self.dal.have_output(query, user_data[0][6])
        return message

class student:
    def __init__(self):
        self.dal = DAL()

    def select (self, student_id, db_path):
        query = f"SELECT database FROM TBLdata WHERE id = {student_id}"
        message = self.dal.have_output(query, db_path)
        return message
    
    def select2 (self, db, student_id ,db_path):
        query = f"SELECT * FROM {db} WHERE id = {student_id}"
        message = self.dal.have_output(query, db_path)
        return message
