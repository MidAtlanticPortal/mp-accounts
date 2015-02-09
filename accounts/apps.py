from django.apps import AppConfig

class AccountsAppConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals

