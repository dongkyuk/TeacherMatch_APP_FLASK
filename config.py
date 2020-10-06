
import os
import logging


# Set sql uri
SQLALCHEMY_DATABASE_URI = 'mysql://root:password@127.0.0.1:3306/the_mentor'

# Turn On Testing
TESTING = True  

# Set Secret key
SECRET_KEY = os.urandom(24)
