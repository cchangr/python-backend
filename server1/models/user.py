from server1.models import Model


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        users = User.all()
        for user in users:
            if user.username == self.username and user.password == self.password:
                return True
        return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2
