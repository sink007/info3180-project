from werkzeug.security import generate_password_hash
import random
import psycopg2
from urllib.parse import urlparse

# Predefined data
parishes = [
    "Kingston", "St. Andrew", "St. Thomas", "Portland", "St. Mary", "St. Ann",
    "Trelawny", "St. James", "Hanover", "Westmoreland", "St. Elizabeth", "Manchester", "Clarendon", "St. Catherine"
]
sexes = ["Male", "Female"]
races = ["White", "Black", "Asian"]
fav_cuisines = ["Jerk Chicken", "Curry Goat", "Ackee and Saltfish", "Ital Stew", "Fried Dumplings"]
fav_school_subjects = ["Math", "English", "Biology", "History", "Geography", "Physics", "Chemistry"]
fav_colours = ["Red", "Blue", "Green", "Yellow", "Purple", "Black"]

sql_lines = []

# Generate users (50 users)
sql_lines.append("-- Insert Users")
sql_lines.append("INSERT INTO users (username, password, name, email, photo, date_joined) VALUES")
user_entries = []
for i in range(1, 51):
    hashed_password = generate_password_hash('123', method='pbkdf2:sha256')
    user_entries.append(
        f"('user{i}', '{hashed_password}', 'User {i}', 'user{i}@example.com', 'user{i}.jpg', CURRENT_TIMESTAMP)"
    )
sql_lines.append(",\n".join(user_entries) + ";\n")

# Generate profiles (3 per user)
sql_lines.append("-- Insert Profiles")
profile_entries = []
profile_id = 1
for user_id in range(1, 51):
    for _ in range(3):
        profile_entries.append(
            f"({user_id}, 'Profile {profile_id} for user{user_id}', "
            f"'{random.choice(parishes)}', "
            f"'This is the biography for profile {profile_id} of user{user_id}.', "
            f"'{random.choice(sexes)}', "
            f"'{random.choice(races)}', "
            f"{random.randint(1980, 2005)}, "
            f"{round(random.uniform(50, 96), 1)}, "
            f"'{random.choice(fav_cuisines)}', "
            f"'{random.choice(fav_colours)}', "
            f"'{random.choice(fav_school_subjects)}', "
            f"{random.choice([True, False])}, "
            f"{random.choice([True, False])}, "
            f"{random.choice([True, False])}, "
            f"{random.randint(0, 50)})"
        )
        profile_id += 1

sql_lines.append("INSERT INTO profile (user_id_fk, description, parish, biography, sex, race, birth_year, height, fav_cuisine, fav_colour, fav_school_subject, political, religious, family_oriented, fav_count) VALUES")
sql_lines.append(",\n".join(profile_entries) + ";")

# Combine SQL statements
full_sql = "\n".join(sql_lines)

# Render database connection string
render_db_url = "postgresql://project_user:GgKw1i7jysoNpMnVvkpbvzgYjYB5ICJ2@dpg-d09sa89r0fns73f7e5a0-a.virginia-postgres.render.com/project_ps4g"
url = urlparse(render_db_url)

# Extract connection parameters
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

# Execute SQL on Render DB
try:
    with psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(full_sql)
            conn.commit()
            print("SQL executed successfully on Render PostgreSQL.")
except Exception as e:
    print(f"An error occurred: {e}")
