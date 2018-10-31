from server1.models import Model


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        users = User.all()
        for user in users:
            if user.username == self.username and user.password == self.password:
                return True
        return False

    def validate_register(self):
        return len(self.username) > 3 and len(self.password) > 2
