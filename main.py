from argparser import cli_parser

from db import Database
from format_factory import FormatFactory


def create_tables(db):
    """ Creates tables in database """

    create_queries = {
        'room':
            """ 
            CREATE TABLE room 
            (
                id INT PRIMARY KEY, 
                name VARCHAR(20) NOT NULL
            ); 
            """,

        'student':
            """ 
            CREATE TABLE student 
            (
                id INT PRIMARY KEY, 
                room_id INT NOT NULL, 
                name TEXT NOT NULL, 
                birthday DATETIME NOT NULL, 
                sex ENUM("F", "M") NOT NULL, 
                CONSTRAINT student_room_fk FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE
            );
            """
    }

    for table_name in reversed(create_queries.keys()):
        db.execute_query(f"DROP TABLE IF EXISTS {table_name}")

    for query in create_queries.values():
        db.execute_query(query)


def insert_data(db, rooms, students):
    """ Inserts initial data to database """
    insert_room_query = """
                            INSERT INTO room (id, name) 
                            VALUES (%s, %s);
                        """
    insert_stud_query = """
                            INSERT INTO student (birthday, id, name, room_id, sex)
                            VALUES (%s, %s, %s, %s, %s);
                        """

    for room in rooms:
        values = tuple(room.values())
        db.execute_query(insert_room_query, *values)

    for stud in students:
        values = tuple(stud.values())
        db.execute_query(insert_stud_query, *values)

    db.commit()


def create_index(db):
    """ Creates indexes to improve efficiency (of 2nd and 3rd select queries from the task) """

    db.execute_query("ALTER TABLE student ADD COLUMN age INT;")
    db.execute_query("UPDATE student SET age = timestampdiff(YEAR, birthday, now());")
    db.execute_query("ALTER TABLE student ADD INDEX age_room_index(age, room_id);")
    db.commit()


def data_selection(db):
    """ Selects required data from database"""

    select_queries = [
        """
        SELECT room_id, 
               COUNT(id) AS number_of_students
        FROM student
        GROUP BY room_id;
        """,

        """
        SELECT room_id,
               AVG(age)+0E0 AS average_age
        FROM student
        GROUP BY room_id
        ORDER BY average_age
        LIMIT 5;
        """,

        """
        SELECT room_id,
               MAX(age) - MIN(age) AS age_difference
        FROM student
        GROUP BY room_id
        ORDER BY age_difference DESC
        LIMIT 5;
        """,

        """
        SELECT room_id
        FROM student
        GROUP BY room_id
        HAVING COUNT(DISTINCT sex) > 1;
        """
    ]

    result = []
    for query in select_queries:
        db.execute_query(query)
        result.append(db.fetch_result())

    return result


def main():
    factory = FormatFactory()

    # CLI parser
    database_file, students_file, rooms_file, dump_format = cli_parser()

    # load source dicts
    format_to_load = 'json'
    serializer_json = factory.get_format(format_to_load)
    students = serializer_json.load(students_file)
    rooms = serializer_json.load(rooms_file)
    database_info = serializer_json.load(database_file)

    # working with database
    db = Database(**database_info)

    create_tables(db)
    insert_data(db, rooms, students)
    create_index(db)
    selected_data = data_selection(db)

    # dump results
    serializer = factory.get_format(dump_format)
    for index, data in enumerate(selected_data):
        serializer.dump(data, f"file{index}.{dump_format}")


if __name__ == "__main__":
    main()
