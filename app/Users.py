from Loader import Loader


class Users(Loader):
    def check_user(self, id) -> bool:
        self.cur.execute("SELECT id from users where id = ?", [id])
        check = self.cur.fetchone()
        if check is None:
            return False
        else:
            return True

    def reg_user(self, username, id, status):
        self.cur.execute("INSERT INTO users VALUES (?, ?, ?)", [
            username, id, status
        ])
        self.conn.commit()

    def get_users(self) -> list:
        self.cur.execute("SELECT id, username, status from users")
        users = self.cur.fetchall()
        return users

    def get_admins(self) -> list:
        self.cur.execute("SELECT id from users where status = 'admin'")
        admins = self.cur.fetchall()
        admins = [item for t in admins for item in t]  # unpack into list
        return admins