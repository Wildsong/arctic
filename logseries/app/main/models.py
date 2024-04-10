from werkzeug.security import generate_password_hash, check_password_hash


class User():
    # ...
    password_hash = 'This is my hash string.'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

if __name__ == '__main__':
    user = User()
    user.password = 'secret'
    user.verify_password('secret')
    user.verify_password('no')

