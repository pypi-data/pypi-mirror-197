#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text

from slpkg.configs import Configs


DATABASE_URI: str = os.path.join(f'sqlite:///{Configs.db_path}', Configs.database_name)

engine = create_engine(DATABASE_URI)

session = sessionmaker(engine)()
Base = declarative_base()


@dataclass
class SBoTable(Base):
    """ The main table for the SBo repository. """

    __tablename__ = 'sbotable'

    id: int = Column(Integer, primary_key=True)   # type: ignore 
    name: str = Column(Text)   # type: ignore 
    location: str = Column(Text)   # type: ignore 
    files: str = Column(Text)   # type: ignore 
    version: str = Column(Text)   # type: ignore 
    download: str = Column(Text)  # type: ignore 
    download64: str = Column(Text)  # type: ignore 
    md5sum: str = Column(Text)  # type: ignore 
    md5sum64: str = Column(Text)   # type: ignore 
    requires: str = Column(Text)   # type: ignore 
    short_description: str = Column(Text)   # type: ignore


@dataclass
class PonceTable(Base):
    """ The main table for the SBo repository. """

    __tablename__ = 'poncetable'

    id: int = Column(Integer, primary_key=True)   # type: ignore
    name: str = Column(Text)   # type: ignore
    location: str = Column(Text)   # type: ignore
    files: str = Column(Text)   # type: ignore
    version: str = Column(Text)   # type: ignore
    download: str = Column(Text)  # type: ignore
    download64: str = Column(Text)  # type: ignore
    md5sum: str = Column(Text)  # type: ignore
    md5sum64: str = Column(Text)   # type: ignore
    requires: str = Column(Text)   # type: ignore
    short_description: str = Column(Text)   # type: ignore


@dataclass
class LogsDependencies(Base):
    """ The table that stores the dependencies after installing a package. """

    __tablename__ = 'logsdependencies'

    id: int = Column(Integer, primary_key=True)   # type: ignore 
    name: str = Column(Text)   # type: ignore 
    requires: str = Column(Text)   # type: ignore 


Base.metadata.create_all(engine)
