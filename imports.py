import random
import psycopg2

# === Static Data ===
parishes = [
    "Kingston", "St. Andrew", "St. Thomas", "Portland", "St. Mary", "St. Ann",
    "Trelawny", "St. James", "Hanover", "Westmoreland", "St. Elizabeth", "Manchester", "Clarendon", "St. Catherine"
]
sexes = ["Male", "Female"]
races = ["White", "Black", "Asian"]
fav_cuisines = ["Jerk Chicken", "Curry Goat", "Ackee and Saltfish", "Ital Stew", "Fried Dumplings"]
fav_school_subjects = ["Math", "English", "Biology", "History", "Geography", "Physics", "Chemistry"]
fav_colours = ["Red", "Blue", "Green", "Yellow", "Purple", "Black"]

# === Descriptions ===
description_phrases = [
    "Spontaneous energy ⚡", "Introvert with a wild side", "Certified vibe curator", "Your favorite distraction",
    "Future playlist co-creator", "Just enough chaos", "Lover of vibes and peace", "Read the room, then own it",
    "In my main character arc", "A little awkward, a lot genuine", "Minimal effort, maximum charm",
    "Not everyone's cup of tea—more like rum", "Heart full of dreams, playlist full of vibes",
    "Bold but soft—like my morning coffee", "Living proof that overthinking is an art",
    "Plot twist in someone’s story", "Part-time romantic, full-time realist", "Inconsistent texter, consistent vibes",
    "Quiet until I’m comfortable", "Here for a good time and a real one", "Vibe check? Passed.",
    "Soft launch specialist", "Made of stars and sarcasm", "Underrated and unbothered", "Soft spoken but sharp",
    "Complex simplicity", "Emotionally fluent", "Made of coffee and contradictions",
    "The one your mom warned you about (in a good way)", "Mystery with a playlist", "Somewhere between shy and savage",
    "Romantic realist", "Catching flights and feelings", "Currently in my peace era", "Sweet, but I will ghost you",
    "Loyal like a dog, confusing like a cat", "Out of likes, still swiping", "Zero drama, full depth",
    "Sassy but wholesome", "The vibe your therapist warned you about", "High standards, low maintenance",
    "Basically a walking moodboard", "Not everyone's cup of tea—more like straight espresso",
    "Running on vibes and deep thoughts", "Nice until proven otherwise", "Loves too hard, replies too slow",
    "The blueprint, not the prototype", "Eye contact and silence > small talk", "Random, chaotic, and oddly charming",
    "Wild but deeply introspective", "Built different but still figuring it out",
    "Just trying to romanticize this soft life", "Ghosted by 8am, journaling by 9", "Sugar, spice, and questionable decisions",
    "Chronically online and emotionally available", "Lowkey wild, highkey healing", "I bring vibes, not explanations",
    "Just here for the memes (and maybe you)", "Soft voice, loud thoughts", "Still healing, still slaying",
    "Authenticity over aesthetics", "Emotionally safe, mentally on edge"
]

# === Bio sentence parts ===
bio_templates = [
    "Hi, I'm someone who {0}, {1}, and {2}. Looking to connect!",
    "You’ll usually find me {0} or {1}. I also {2} on weekends.",
    "{0}. {1}. That’s pretty much me. Oh, and I {2}.",
    "Just a soul that {0}, {1}, and definitely {2}. Let’s chat!",
    "Life’s short—I {0}, {1}, and always {2}.",
    "People say I {0}, but I like to think I {1}. Oh, and I also {2}.",
    "My vibe? Probably someone who {0}, {1}, and {2}.",
    "In a world where everyone {0}, I {1} and {2}.",
    "I {0}, I {1}, and I {2}. That’s the vibe.",
    "I live for the moments when I {0}, {1}, and maybe even {2}.",
    "Who am I? Someone who {0}, then {1}, and ends the day {2}.",
    "I believe everyone should {0}. Me? I also {1} and {2}.",
    "On most days I {0}, but when the mood hits, I {1} and {2}."
]

bio_traits = [
    "get lost in deep convos", "sing terribly in the shower", "romanticize the little things",
    "binge-watch shows and then forget the plot", "write love letters in their head", "go for walks to clear their mind",
    "zone out during small talk", "stay up way too late thinking", "laugh at their own jokes",
    "dance when nobody's watching", "believe music can fix anything", "crave real connections",
    "give great advice but never take it", "pretend they’re fine when they’re not", "say 'I’m fine' and mean the opposite",
    "text back in their head", "ghost people unintentionally", "start books and never finish them",
    "keep playlists for every mood", "notice the small things people do"
]

# === User name data ===
names_dict = {
    i + 1: name for i, name in enumerate([
        "Liam Smith", "Olivia Johnson", "Noah Williams", "Emma Brown", "Oliver Jones",
        "Ava Garcia", "Elijah Miller", "Charlotte Davis", "William Rodriguez", "Sophia Martinez",
        "James Hernandez", "Amelia Lopez", "Benjamin Gonzalez", "Mia Wilson", "Lucas Anderson",
        "Harper Thomas", "Henry Taylor", "Evelyn Moore", "Alexander Jackson", "Abigail Martin",
        "Sebastian Lee", "Emily Perez", "Jack White", "Ella Thompson", "Daniel Harris",
        "Scarlett Sanchez", "Matthew Clark", "Luna Lewis", "Jackson Robinson", "Chloe Walker"
    ])
}

sql_lines = []

# === Insert Users ===
sql_lines.append("-- Insert Users")
sql_lines.append("INSERT INTO users (username, password, name, email, photo, date_joined) VALUES")
user_entries = []
for i in range(1, 31):
    password = '123'
    name = names_dict[i]
    user_entries.append(
        f"('user{i}', '{password}', '{name}', 'user{i}@example.com', 'user{i}.jpg', CURRENT_TIMESTAMP)"
    )
sql_lines.append(",\n".join(user_entries) + ";\n")

# === Insert Profiles ===
sql_lines.append("-- Insert Profiles")
profile_entries = []
profile_id = 1
for user_id in range(1, 31):
    user_gender = random.choice(sexes)
    user_race = random.choice(races)
    birth_year = random.randint(1980, 2005)
    for _ in range(3):
        description = random.choice(description_phrases)
        bio = random.choice(bio_templates).format(
            random.choice(bio_traits),
            random.choice(bio_traits),
            random.choice(bio_traits)
        )

        description = description.replace("'", "''")
        bio = bio.replace("'", "''")
        
        profile_entries.append(
            f"({user_id}, '{description}', "
            f"'{random.choice(parishes)}', "
            f"'{bio}', "
            f"'{user_gender}', "
            f"'{user_race}', "
            f"{birth_year}, "
            f"{round(random.uniform(50, 96), 1)}, "
            f"'{random.choice(fav_cuisines)}', "
            f"'{random.choice(fav_colours)}', "
            f"'{random.choice(fav_school_subjects)}', "
            f"{random.choice([True, False])}, "
            f"{random.choice([True, False])}, "
            f"{random.choice([True, False])}, "
            f"{random.randint(1, 30)})"
        )
        profile_id += 1

sql_lines.append("INSERT INTO profile (user_id_fk, description, parish, biography, sex, race, birth_year, height, fav_cuisine, fav_colour, fav_school_subject, political, religious, family_oriented, fav_count) VALUES")
sql_lines.append(",\n".join(profile_entries) + ";")

# === Write & Execute SQL ===
with open("profiles.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_lines))

print("SQL statements written to profiles.sql")

with open("profiles.sql", "r", encoding="utf-8") as f:
    sql = f.read()

try:
    with psycopg2.connect(
        dbname="project_ps4g",
        user="project_user",
        password="GgKw1i7jysoNpMnVvkpbvzgYjYB5ICJ2",
        host="dpg-d09sa89r0fns73f7e5a0-a.virginia-postgres.render.com",
        port="5432"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
            print("SQL executed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
