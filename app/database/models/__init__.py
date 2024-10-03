from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import *
from .travel import *
from .seat import *
from .booking import *
from .booking_seat import *
from .payment import *