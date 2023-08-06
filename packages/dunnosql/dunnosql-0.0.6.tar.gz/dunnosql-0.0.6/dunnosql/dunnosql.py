import mariadb as mdb
import psycopg2 as psg

class Dunnosql():
    def __init__(self, engine='postgresql'):
        self.engine = engine.lower()
    def connect(self, host_ip, your_database, db_user, db_password, port='default',log=False):
        """ Connect to chosen database server.

        Arguments:
        ------------
            host_ip: string (IP of server you're trying to connect)

            your_database: string (database you're trying to connect)

            db_user: string(which user you're trying to log into with connection)

            db_password: string(password to the user above)

            port: int (port you want to connect with; defaults are 3306[MariaDB] and 5432[PostgreSQL])

            log: either you want to log if operation was success or not.
        """
        if port == 'default':
            if self.engine == 'mariadb':
                self.db_port = 3306
            elif self.engine == 'postgresql':
                self.db_port = 5432
        else:
            self.db_port = port
        if self.engine == 'mariadb':
            try:
                self.conn = mdb.connect(
                    user=db_user,
                    password=db_password,
                    host=host_ip,
                    database= your_database,
                    port=self.db_port                
                )
                self.cursor = self.conn.cursor()
                if log: print("Connected")
            except:
                raise AttributeError(f"DunnoSQL: Couldn't connect to {your_database} with {self.engine}.")
        elif self.engine == 'postgresql':
            try:
                self.conn = psg.connect(
                database=your_database,
                host=host_ip,
                user=db_user,
                password=db_password,
                port=self.db_port
                )
                self.cursor = self.conn.cursor()
                if log: print("Connected")
            except:
                raise AttributeError(f"DunnoSQL: Couldn't connect to {your_database} with {self.engine}.")
        else:
            raise NotImplementedError("DunnoSQL: Only MariaDB and PostgreSQL are supported for now.")
    def get_data(self, table, all=True, column='Specific column', where='WHERE syntax'):
        """ Get data from SQL table.

        Arguments
        ------------
            table: string (name of table you want to get data from.)

            all: bool (True is SELECT * FROM table, for specific set to False)

            column: string (if not using all this is column you want to specify)

            where: string (if not using all this is where you put your filter e.g. LIKE '?text?'. Leave as it is if you want to ignore it.)
        """
        try:
            if all:
                if where != 'WHERE syntax':
                    if 'where' in where.lower():
                        where = where[5:]
                    self.cursor.execute(f"SELECT * FROM {table} WHERE {where};")
                else:
                    self.cursor.execute(f"SELECT * FROM {table};")
            else:
                if where != 'WHERE syntax':
                    if 'where' in where.lower():
                        where = where[5:]
                    self.cursor.execute(f"SELECT {column} FROM {table} WHERE {where};")
                else:
                    self.cursor.execute(f"SELECT {column} FROM {table};")
            
            data = self.cursor.fetchall()
            return data
        except:
            raise NameError(f"DunnoSQL: Error occured when trying to get data from {table}.")
    def get_columns(self,table,table_schema='public'):
        """ Get column of chosen table.

        Arguments
        ---------
            table: string (chosen table from connected database)

            table_schema: string (PostgreSQL uses table_schema, change if needed.)
        
        """
        if self.engine == 'mariadb':
            self.cursor.execute(f"SHOW COLUMNS FROM {table};")     
        else:
            self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{table_schema}' AND table_name = '{table}';")    
        data = self.cursor.fetchall()
        return data   
    def get_tables(self):
        """Get tables of database you're connected to.
        """
        if self.engine == 'mariadb':
            self.cursor.execute("SHOW TABLES;")
        else:
            self.cursor.execute("SELECT * FROM pg_catalog.pg_tables;")
        data = self.cursor.fetchall()
        return data
    def insert(self,table,values):
        """Insert data to chosen table.

        Arguments
        ---------
            table: string (table to insert data)

            values: list (list of values you want to insert)
        """

        query = f"INSERT INTO {table} VALUES("
        for value in values:
            query += f"'{value}', "
        query = f"{query[:-2]});"

        self.cursor.execute(query)
        self.conn.commit()
    def update(self,table,columns_to_include,new_values,where=''):
        """Update records in table

        Arguments
        ---------
            table: string (table to update)

            columns_to_include: list/str (list of columns to update, might be string if only one)

            new_values: list/str (list of new values or string if only one - MUST BE SAME LEN AS COLUMNS ABOVE)

            where: string (WHERE syntax, leave blank to ignore. Also doesn't matter if WHERE is included in syntax or not)
        """

        query = f"UPDATE {table} SET "

        if 'where' in where.lower():
            where = where[5:]
        if isinstance(columns_to_include,str):
            columns_to_include = [columns_to_include]
        if isinstance(new_values,str):
            new_values = [new_values]

        for x in range(len(columns_to_include)):
            query += f"{columns_to_include[x]}='{new_values[x]}', "

        query = query[:-2]
        if len(where)>0:
            query += f" WHERE {where}"
        query +=  ";"
        print(query)

        self.cursor.execute(query)
        self.conn.commit()
    def delete(self, table, where=''):
        """Delete from table

        Arguments
        ---------
            table: string (table to delete from)
            
            where: string (where syntax, doesn't matter if keyword WHERE is included)
        """

        if 'where' in where.lower():
            where = where[5:]
        self.cursor.execute(f"DELETE FROM {table} WHERE {where};")
        self.conn.commit()
    def custom(self, query):
        """ Type SQL query and execute. Simple as it is.
        """

        if query[0:5].lower() == 'SELECT':
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            return data
        else:
            self.cursor.execute(query)
            self.conn.commit()