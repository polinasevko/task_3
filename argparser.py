import argparse
from pathlib import Path


def cli_parser():
    parser = argparse.ArgumentParser(description='Task 1')
    parser.add_argument('-db', '--database', type=Path,
                        help="File with info about database to connect")
    parser.add_argument('-s', '--students', type=Path,
                        help="File to upload data about students")
    parser.add_argument('-r', '--rooms', type=Path,
                        help="File to upload data about rooms")
    parser.add_argument('-f', '--format', type=str,
                        help="Dump format")
    console_args = parser.parse_args()
    database_info = console_args.database
    students_file = console_args.students
    rooms_file = console_args.rooms
    dump_format = console_args.format
    return database_info, students_file, rooms_file, dump_format
