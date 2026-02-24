import psycopg2
from faker import Faker
import random

fake = Faker()

conn = psycopg2.connect(
    dbname="books", user="hadisedaghat", password="", host="localhost", port="5432"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT,
    publisher TEXT,
    first_publish_year INTEGER,
    image_url TEXT
)
""")

NUM_BOOKS = 20000

for _ in range(NUM_BOOKS):
    title = fake.sentence(nb_words=4)
    author = fake.name()
    publisher = fake.company()
    year = random.randint(1900, 2023)
    image_url = None

    cursor.execute(
        """
    INSERT INTO books (title, author, publisher, first_publish_year, image_url)
    VALUES (%s, %s, %s, %s, %s)
    """,
        (title, author, publisher, year, image_url),
    )

conn.commit()
conn.close()
print(f"{NUM_BOOKS} books added to the database!")
