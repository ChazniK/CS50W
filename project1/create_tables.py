import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# database engine object from SQLAlchemy that manages connections to the database
# DATABASE_URL is an environment variable that indicates where the database lives
engine = create_engine(os.getenv("DATABASE_URL"))

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))

def create_tables():
    db.execute("""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL)""")

    db.execute("""
    DROP TABLE IF EXISTS books;
    CREATE TABLE books(
        id SERIAL PRIMARY KEY,
        isbn VARCHAR(50) UNIQUE NOT NULL,
        title VARCHAR(50) NOT NULL,
        author VARCHAR(100) NOT NULL,
        year SMALLINT NOT NULL)""")

    db.execute("""
    DROP TABLE IF EXISTS ratings;
    CREATE TABLE ratings(
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        rating VARCHAR NOT NULL)""")
        
    db.commit()

def main():
    create_tables()

if __name__ == "__main__":
    main()
