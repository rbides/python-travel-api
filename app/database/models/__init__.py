# flake8: noqa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .role import *

# to avoid breaking table relationships
from .user import *
