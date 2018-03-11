import sys
import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.hash import pbkdf2_sha512

Base = declarative_base()


class BaseMixin(object):

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True, unique=True)

    @declared_attr
    def created_at(self):
        return Column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def updated_at(self):
        return Column(DateTime, default=datetime.datetime.utcnow)


class UserAccount(Base, BaseMixin):
    __tablename__ = 'user_account'

    def __init__(self, username, passcode, mobile, email, ip_address):
        self.username = username
        self.password = pbkdf2_sha512.hash(passcode)
        self.mobile = mobile
        self.email = email
        self.ip_address = ip_address

    username = Column(String(80), nullable=False)
    password = Column(String(1000), nullable=False)
    mobile = Column(String(15), nullable=False)
    ip_address = Column(String(15), nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)

    def is_verified_check(self):
        return self.is_verified

    def decode_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)


Engine = create_engine('postgres://xlvroomeimshcb:e99dcf87bf5161aa4be30fcfd7c3835f96da539f8ecde9e9c61405c125ada391@ec2-54-247-81-88.eu-west-1.compute.amazonaws.com:5432/d8j46e8flvv4gv')
Base.metadata.create_all(Engine)