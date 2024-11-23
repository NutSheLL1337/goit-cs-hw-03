import psycopg2
from faker import Faker
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

faker = Faker()

def create_tables(connection):
    """Creates the tables in the PostgreSQL database."""
    try:
        cursor = connection.cursor()

        # Create the `users` table
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100),
            email VARCHAR(100) UNIQUE
        );
        """)

        # Create the `status` table
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE
        );
        """)

        # Create the `tasks` table
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            description TEXT,
            status_id INTEGER REFERENCES status (id) ON DELETE CASCADE ON UPDATE CASCADE,
            user_id INTEGER REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """)

        connection.commit()
        print("Tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {e}")
        connection.rollback()

def seed_database(connection):
    """Seeds the database with fake data."""
    try:
        cursor = connection.cursor()

        # Seed the `users` table
        print("Seeding users table...")
        for _ in range(10):
            fullname = faker.name()
            email = faker.unique.email()
            cursor.execute(
                "INSERT INTO users (fullname, email) VALUES (%s, %s)",
                (fullname, email)
            )

        # Commit after users insertion to ensure data is available for later
        connection.commit()

        # Seed the `status` table
        print("Seeding status table...")
        statuses = ["To Do", "In Progress", "Completed", "Blocked"]
        for status_name in statuses:
            cursor.execute(
                "INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING",
                (status_name,)
            )

        # Commit after status insertion
        connection.commit()

        # Fetch user_ids and status_ids after the tables are populated
        print("Fetching IDs for users and statuses...")
        cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cursor.fetchall()]

        # Seed the `tasks` table
        print("Seeding tasks table...")
        for _ in range(20):
            title = faker.sentence(nb_words=6)
            description = faker.text(max_nb_chars=200)
            status_id = faker.random.choice(status_ids)
            user_id = faker.random.choice(user_ids)
            
            # Ensure that the selected user_id and status_id are valid
            if status_id not in status_ids or user_id not in user_ids:
                print(f"Invalid foreign key: user_id={user_id}, status_id={status_id}")
                continue  # Skip invalid entries

            cursor.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                (title, description, status_id, user_id)
            )

        # Commit the task insertions
        connection.commit()
        print("Seeding completed!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        connection.rollback()

if __name__ == "__main__":
    try:
        # Connect to PostgreSQL using credentials from .env
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to the PostgreSQL database!")

        # Create tables
        create_tables(connection)

        # Seed the database
        seed_database(connection)

        # Close the connection
        connection.close()
        print("Connection closed.")

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
