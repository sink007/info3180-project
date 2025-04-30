from werkzeug.security import generate_password_hash
import random
import psycopg2

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

# Generate users (50 users, no explicit id)
sql_lines.append("-- Insert Users")
sql_lines.append("INSERT INTO users (username, password, name, email, photo, date_joined) VALUES")
user_entries = []
for i in range(1, 51):
    hashed_password = generate_password_hash('123', method='pbkdf2:sha256')
    user_entries.append(
        f"('user{i}', '{hashed_password}', 'User {i}', 'user{i}@example.com', 'user{i}.jpg', CURRENT_TIMESTAMP)"
    )
sql_lines.append(",\n".join(user_entries) + ";\n")

# Generate profiles (3 per user, still need user_id_fk)
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

# Write to file
with open("profiles.sql", "w") as f:
    f.write("\n".join(sql_lines))

print("SQL statements written to profiles.sql")

# Execute the SQL
with open("profiles.sql", "r") as f:
    sql = f.read()

try:
    with psycopg2.connect(
        dbname="project",
        user="project_user",
        password="123",
        host="localhost",
        port="5432"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
except Exception as e:
    print(f"An error occurred: {e}")
