# DataMirror

## Description

This project is a command-line tool that exports data from a source (file or PostgreSQL) to a target (file or PostgreSQL). It provides flexibility in choosing the source and target types, allowing users to easily transfer data between different storage mediums.

## Installation

To use this tool, follow these steps:

    Clone the repository: git clone <repository_url>
    Install the required dependencies: pip install -r requirements.txt


## Usage

Run the tool with the following command:

```cmd
python main.py --source <source> --target <target>
```

Replace <source> with the link or path of the source. If the source is a file, provide the directory path. If the source is PostgreSQL, provide the PostgreSQL DSN.

Similarly, replace <target> with the link or path of the target. If the target is a file, provide the directory path. If the target is PostgreSQL, provide the PostgreSQL DSN.


### File Structure

Note: If the type is "file", the provided directory should have the following four fixed directories:

- json_data：This directory stores the data from the tables in JSON format. This means that the data from each table is saved in the corresponding file in JSON format.

- stored_procedures：This directory contains the SQL statements for the stored procedures in the database.

- table：This directory contains the SQL statements for all the tables in the database. These SQL statements are sorted based on foreign key indexes, and the filenames are named accordingly. These SQL statements describe the structure and constraints of each table.

- trigger：This directory contains the SQL statements for the triggers in the database. 

> example: [test directory](/test/source)

## Examples

Export data from a PostgreSQL source to a file target:

```cmd
python main.py --source postgresql://user:password@localhost:5432/database --target /path/to/target/directory
```


Export data from a file source to a PostgreSQL target:

```cmd
python main.py --source /path/to/source/directory --target postgresql://user:password@localhost:5432/database
```

Note: It is also possible to export data from PostgreSQL to PostgreSQL or from file to file by providing the appropriate source and target types and links.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License.