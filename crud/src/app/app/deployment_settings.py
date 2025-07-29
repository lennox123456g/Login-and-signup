
import os #add this 
import dj_database_url
from .settings import * 
from .settings import BASE_DIR


ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ.get('RENDER_EXTERNAL_HOSTNAME')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')#generate it in render

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # for production




# Application definition



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 👈 Add this line
    'whitenoise.middleware.WhiteNoiseMiddleware',#add the whitenoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'


WSGI_APPLICATION = 'app.wsgi.application'


# Database
# Static files (CSS, JavaScript, Images)
STORAGES = {
    "default":{
        "BACKEND" : "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND" : "whitenoise.storage.CompressedStaticFilesStorage",
    },

}


#loggers





# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#Custom User Model
AUTH_USER_MODEL = 'appsot.UserAccount'  # Remove the comma at the end

#added
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    'https://render-deploy-tutorial-reactjs-code.onrender.com'
]

#Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}



DATABASES = {
    'default': dj_database_url.config(
        default= os.environ['DATABASE_URL'], 
        conn_max_age=600
    )
}


#Emailsp
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'testingalways953@gmail.com'
EMAIL_HOST_PASSWORD = 'joci cmfo svdu jtqj'#this app password should be with gaps as provided by google
EMAIL_USE_TLS = True
#when they say user always appears yet not,run python manage.py flush the reload and resubmit request


#Active Campaign Settings
ACTIVE_CAMPAIGN_URL = 'https://crickettonurture.activehosted.com'
ACTIVE_CAMPAIGN_KEY = 'd91653c2b0e9a47577cabac9315c86e54e8a7f298eb17b9751956e80c8320c95dd448d40'


# Replace these with your actual IDs from Active Campaign
AC_MASTER_LIST_ID = '3'  # Your actual master list ID  
AC_EBOOK_TAG_ID = '2'    # Your actual tag ID