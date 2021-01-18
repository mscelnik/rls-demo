""" MyDB SQL model definition.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Unicode, ForeignKey, DateTime, BigInteger
from sqlalchemy import String as UniqueIdentifier, UniqueConstraint
from sqlalchemy.orm import relationship
from .common import GUID


Base = declarative_base()


class User(Base):
    """ Individual user; must belong to a customer company.
    """
    __tablename__ = 'users'
    ID = Column(GUID, primary_key=True)
    Name = Column(Unicode(50), nullable=False)
    Email = Column(Unicode(50), nullable=False)
    CompanyID = Column(GUID, ForeignKey('companies.ID'))


class Company(Base):
    """ Customer company.
    """
    __tablename__ = 'companies'
    ID = Column(GUID, primary_key=True)
    Name = Column(Unicode(50), nullable=False)
    users = relationship('User', backref='company')


class Asset(Base):
    """ A physical asset for which we have data.
    """
    __tablename__ = 'assets'
    ID = Column(GUID, primary_key=True)
    Name = Column(Unicode(50), nullable=False)


class CompanyAssets(Base):
    """ Cross-reference table linking companies to one or more assets.
    Note, an asset can be shared with different companies too.
    """
    __tablename__ = 'company_assets'
    ID = Column(GUID, primary_key=True)
    CompanyID = Column(GUID, ForeignKey('companies.ID'), nullable=False)
    AssetID = Column(GUID, ForeignKey('assets.ID'), nullable=False)


class AssetData(Base):
    """ Some actual data our app stores per asset.
    Users should only be able to view data for assets associated with the user's company.
    """
    __tablename__ = 'asset_data'
    ID = Column(GUID, primary_key=True)
    AssetID = Column(GUID, ForeignKey('assets.ID'), nullable=False)
    Parameter = Column(Unicode(50))
    Value = Column(Unicode)
    Description = Column(Unicode)
