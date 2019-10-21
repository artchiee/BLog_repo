from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'Accounts'

    #  Getting signals ready to fire 
    def ready(self):
        import Accounts.signals
