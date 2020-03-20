import sqlite3


class SqliteConnect(object):
    """initalize the database
    Database Table:
    if no gulid id then create table
    | userid | timestamp | emojiid |
    """
    def __init__(self, path='../data/emoji.db'):
        self.conn = sqlite3.connect(path)

    def __enter__(self):
        cursor = self.conn.cursor()
        return cursor

    def __exit__(self, *args, **kwargs):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    with SqliteConnect() as session:
        res = session.execute("SELECT emoji_id\
                               FROM `452726035138740256`\
                               WHERE emoji_id = 'e';")
        print(res.fetchone())
