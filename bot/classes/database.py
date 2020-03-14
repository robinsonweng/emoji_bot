import sqlite3


class SqliteConnect(object):
    """initalize the database
    Database Table:
    if no gulid id then create table
    | userid | timestamp | emojiid |
    """
    def __init__(self, path='../bot/data/emoji.db'):
        self.conn = sqlite3.connect(path)

    def __enter__(self):
        cursor = self.conn.cursor()
        return cursor

    def __exit__(self, *args, **kwargs):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    with SqliteConnect() as session:
        print('s')
