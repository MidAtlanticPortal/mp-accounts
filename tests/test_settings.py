# Minimal settings file required to run tests.

SECRET_KEY = 'poodles-puddles'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'social',
    'tests',
    'accounts.apps.AccountsAppConfig',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'some.db',
    }
}

ROOT_URLCONF = 'tests.urls'

SHARING_TO_PUBLIC_GROUPS = ['Share with Public']
SHARING_TO_STAFF_GROUPS = ['Share with Staff']

SOCIAL_AUTH_GOOGLE_PLUS_KEY = 'BLAH'
SOCIAL_AUTH_GOOGLE_PLUS_SCOPES = ['EMAIL']