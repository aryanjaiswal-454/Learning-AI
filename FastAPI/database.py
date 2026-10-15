import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(r"D:\GenAI\.env")

DATABASE_URL = os.getenv("DATABASE_URL")

engine=create_engine(DATABASE_URL)

metadata = MetaData()

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()