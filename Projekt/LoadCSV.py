import cx_Oracle
import csv

db_username_read = open('db_username.txt')
db_username = db_username_read.read()
db_username_read.close()

db_password_read = open('db_password.txt')
db_password = db_password_read.read()
db_password_read.close()

db_host_read = open('db_host.txt')
db_host = db_host_read.read()
db_host_read.close()

csv_file_path = 'gamesales.csv'

def load_data_to_oracle():
    connection = cx_Oracle.connect(user=db_username, password=db_password, dsn=db_host)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM game_sales")
    cursor.execute("DELETE FROM platforms")
    cursor.execute("DELETE FROM publishers")
    cursor.execute("DELETE FROM developers")
    cursor.execute("DELETE FROM genres")
    cursor.execute("DELETE FROM ratings")

    # Usuwanie i tworzenie sekwencji
    sequences = ['platforms_seq', 'publishers_seq', 'developers_seq', 'genres_seq', 'games_seq', 'ratings_seq']
    for seq in sequences:
        try:
            cursor.execute(f"DROP SEQUENCE {seq}")
        except cx_Oracle.DatabaseError:
            pass
        cursor.execute(f"CREATE SEQUENCE {seq} START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE")

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        next(csv_reader, None)

        developers_dict = {}
        publishers_dict = {}
        genres_dict = {}
        platforms_dict = {}
        ratings_dict = {}

        for row in csv_reader:
            platform_name = row['Platform']
            publisher_name = row['Publisher']
            developer_name = row['Developer']
            genre_name = row['Genre']
            rating_name = row['Rating']

            # Tworzenie ID dla platformy, wydawcy, dewelopera, gatunku i ratingu
            platform_id = platforms_dict.get(platform_name)
            if platform_id is None:
                platform_id = cursor.execute("SELECT platforms_seq.NEXTVAL FROM DUAL").fetchone()[0]
                platforms_dict[platform_name] = platform_id

            publisher_id = publishers_dict.get(publisher_name)
            if publisher_id is None:
                publisher_id = cursor.execute("SELECT publishers_seq.NEXTVAL FROM DUAL").fetchone()[0]
                publishers_dict[publisher_name] = publisher_id

            developer_id = developers_dict.get(developer_name)
            if developer_id is None:
                developer_id = cursor.execute("SELECT developers_seq.NEXTVAL FROM DUAL").fetchone()[0]
                developers_dict[developer_name] = developer_id

            genre_id = genres_dict.get(genre_name)
            if genre_id is None:
                genre_id = cursor.execute("SELECT genres_seq.NEXTVAL FROM DUAL").fetchone()[0]
                genres_dict[genre_name] = genre_id

            rating_id = ratings_dict.get(rating_name)
            if rating_id is None:
                rating_id = cursor.execute("SELECT ratings_seq.NEXTVAL FROM DUAL").fetchone()[0]
                ratings_dict[rating_name] = rating_id

        # Wstawianie do tabel
        for platform in platforms_dict:
            platform_id = platforms_dict[platform]
            cursor.execute(
                "INSERT INTO platforms (platform_id, platform_name) VALUES (:platform_id, :platform_name)",
                {'platform_id': platform_id, 'platform_name': platform}
            )

        for publisher in publishers_dict:
            publisher_id = publishers_dict[publisher]
            cursor.execute(
                "INSERT INTO publishers (publisher_id, publisher_name) VALUES (:publisher_id, :publisher_name)",
                {'publisher_id': publisher_id, 'publisher_name': publisher}
            )

        for developer in developers_dict:
            developer_id = developers_dict[developer]
            cursor.execute(
                "INSERT INTO developers (developer_id, developer_name) VALUES (:developer_id, :developer_name)",
                {'developer_id': developer_id, 'developer_name': developer}
            )

        for genre in genres_dict:
            genre_id = genres_dict[genre]
            cursor.execute(
                "INSERT INTO genres (genre_id, genre_name) VALUES (:genre_id, :genre_name)",
                {'genre_id': genre_id, 'genre_name': genre}
            )

        for rating in ratings_dict:
            rating_id = ratings_dict[rating]
            cursor.execute(
                "INSERT INTO ratings (rating_id, rating_name) VALUES (:rating_id, :rating_name)",
                {'rating_id': rating_id, 'rating_name': rating}
            )

    # Wstawianie danych do tabeli game_sales
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:

                platform_id = platforms_dict[row['Platform']]
                publisher_id = publishers_dict[row['Publisher']]
                developer_id = developers_dict[row['Developer']]
                genre_id = genres_dict[row['Genre']]
                rating_id = ratings_dict[row['Rating']]

                if None in (platform_id, publisher_id, developer_id, genre_id, rating_id):
                    print(f"Brak odpowiedniego id dla gry {row['Name']}. Pomijanie wpisu.")
                    continue

                game_id = cursor.execute("SELECT games_seq.NEXTVAL FROM DUAL").fetchone()[0]

                cursor.execute("""
                    INSERT INTO game_sales (
                        game_id,
                        game_name, 
                        platform_id, 
                        publisher_id, 
                        developer_id,
                        rating_id, 
                        genre_id, 
                        na_sales, 
                        eu_sales, 
                        jp_sales, 
                        other_sales, 
                        critic_score,
                        critic_count,
                        user_score,
                        user_count, 
                        release_date
                    ) 
                    VALUES (
                        :game_id,
                        :game_name, 
                        :platform_id, 
                        :publisher_id, 
                        :developer_id,
                        :rating_id,  
                        :genre_id, 
                        :na_sales, 
                        :eu_sales, 
                        :jp_sales, 
                        :other_sales, 
                        :critic_score,
                        :critic_count,
                        :user_score,
                        :user_count, 
                        :release_date
                    )
                """, {
                    'game_id': game_id,
                    'game_name': row['Name'],
                    'platform_id': platform_id,
                    'publisher_id': publisher_id,
                    'developer_id': developer_id,
                    'rating_id': rating_id,
                    'genre_id': genre_id,
                    'na_sales': int(float(row['NA_Sales']) * 1000000),
                    'eu_sales': int(float(row['EU_Sales']) * 1000000),
                    'jp_sales': int(float(row['JP_Sales']) * 1000000),
                    'other_sales': int(float(row['Other_Sales']) * 1000000),
                    'critic_score': float(row['Critic_Score']),
                    'critic_count': int(float(row['Critic_Count'])),
                    'user_score': float(row['User_Score']),
                    'user_count': int(float(row['User_Count'])),
                    'release_date': int(float(row['Release_Date']))
                })

        connection.commit()
        print("Pomyślnie załadowano dane o grach")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    finally:
        cursor.close()
        connection.close()

load_data_to_oracle()
