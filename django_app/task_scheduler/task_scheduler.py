import pickle
from datetime import datetime
from .db_con import get_connection


class TaskScheduler:
    interval = None
    quiet_mode = True

    def __init__(self, quiet_mode: bool = True):
        self.quiet_mode = quiet_mode
        # create db table if not exists
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS task_objects("
            "id INTEGER primary key autoincrement,"
            "object TEXT NOT NULL,"
            "finished BOOL DEFAULT 0,"
            "datetime DATETIME DEFAULT CURRENT_TIMESTAMP"
            ")"
        )
        self.last_time = ""

    @classmethod
    def run_unfinished_tasks(cls):
        def ___load_task(query_row):
            task_obj = pickle.loads(query_row["object"])
            task_obj.task_id = query_row["id"]
            return task_obj

        cur = get_connection().cursor()
        response = cur.execute("SELECT * FROM task_objects where finished=False;").fetchall()

        for task in [___load_task(obj) for obj in response]:
            if not task.finished:
                task.run()

    @staticmethod
    def __get_timestamp(time_string):
        return datetime.strptime(time_string, "%Y:%m:%d %h:%m:%s")

    @classmethod
    def check_for_unfinished_tasks(cls) -> bool:
        if not cls.quiet_mode:
            print("checked db at " + str(datetime.now()))
        cur = get_connection().cursor()
        res = cur.execute("SELECT * FROM task_objects where finished=False;").fetchone()
        return False if res is None else len(res) >= 1