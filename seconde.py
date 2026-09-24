from first import DAL

# form
class Form1:
    def __init__(self):
        self.dal = DAL()

    def select (self, username, password, db_path):
        query = f"SELECT * FROM TBLdata WHERE username = '{username}' AND password = '{password}';"
        message = self.dal.have_output(query, db_path)
        return message

# teacher form
class Form_t:
    def __init__(self):
        self.dal = DAL()

    def insert (self, Name, Family, Math, Geographi, cursor):
        try:
            query = f"INSERT INTO {cursor[0][6][0:-3]} ('Name', 'Family', 'Math', 'geographi') VALUES ('{Name}', '{Family}',  {Math}, {Geographi});"
            message = self.dal.no_output(query, cursor[0][6])
            return message
        except Exception as error:
            return error
    
    def update (self, Name, Family, Math, Geographi, id, cursor):
        query = f"UPDATE {cursor[0][6][0:-3]} SET 'Name' = '{Name}', 'Family' = '{Family}', 'Math' = {Math}, 'Geographi' = {Geographi} WHERE id = {id}"
        message = self.dal.no_output(query, cursor[0][6])
        return message

    def select (self, cursor):
        query = f"SELECT * FROM {cursor[0][6][0:-3]};"
        message = self.dal.have_output(query, cursor[0][6])
        return message

    def search (self, filter, condition, value, cursor):
        query = f"SELECT * FROM {cursor[0][6][0:-3]} WHERE"
        try:
            match condition:
                case "Ends With":
                    query = f"{query} LOWER({filter}) LIKE '%{value.lower()}'"
                case "Starts With":
                    query = f"{query} LOWER({filter}) LIKE '{value.lower()}%'"
                case "Contains":
                    query = f"{query} LOWER({filter}) LIKE '%{value.lower()}%'"
                case "Equals":
                    if filter in ("Name", "Family"):
                        query = f"{query} LOWER({filter}) = '{value.lower()}'"
                    else:
                        query = f"{query} {filter} = {value}"
            message = self.dal.have_output(query, cursor[0][6])
            return message
        except Exception as error:
            return error
    
# student form
class Form_s:
    def __init__(self):
        self.dal = DAL()

    def select (self, id, db_path):
        query = f"SELECT database FROM TBLdata WHERE id = {id}"
        message = self.dal.have_output(query, db_path)
        return message
    
    def select2 (Self, db, id ,db_path):
        query = f"SELECT * FROM {db} WHERE id = {id}"
        message = Self.dal.have_output(query, db_path)
        return message