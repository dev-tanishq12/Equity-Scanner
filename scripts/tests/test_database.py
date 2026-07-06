from database.database import get_connection


def main():

    conn = get_connection()

    print("Connected Successfully!")

    conn.close()


if __name__ == "__main__":
    main()