from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.accounts'

    def ready(self):
        # Ensures signals are loaded when the app is ready
        import src.accounts.signals  
