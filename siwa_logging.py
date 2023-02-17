'''custom log handler to store logs as SQLite
to simplify storage and retrieval'''

#standard library
import time, logging, sqlite3

#our stuff
import constants as c

#NOTE: these db columns are named exactly the same as
#the record.__dict__ keys to make it easy
create_table_sql = """CREATE TABLE IF NOT EXISTS log(
                    created REAL,
                    name TEXT,
                    threadName TEXT,
                    thread INTEGER,
                    levelname TEXT,
                    msg TEXT)"""

insert_log_line_sql = '''INSERT INTO log VALUES
                        (:created, :name, :threadName,
                        :thread, :levelname, :msg)'''

class SQLite_Handler(logging.Handler):
    def __init__(self):
        super().__init__()
        #create table if it doesnt exist yet in a new siwa install
        conn = sqlite3.connect(c.LOGGING_PATH)
        conn.execute(create_table_sql)
        conn.commit()
        conn.close()
        self.propagate = False

    def emit(self, record):
        log_data = record.__dict__
        conn = sqlite3.connect(c.LOGGING_PATH)
        conn.execute(insert_log_line_sql, log_data)
        conn.commit()
        conn.close()
        return None
