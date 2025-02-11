# app/models.py

# Placeholder for potential future database models
class User:
    def __init__(self, account_number, password):
        self.account_number = account_number
        self.password = password

class Story:
    def __init__(self, user_account, theme, content):
        self.user_account = user_account
        self.theme = theme
        self.content = content