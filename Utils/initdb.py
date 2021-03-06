import mysql.connector
from exceptions import InputError, MySqlError

# Define constants
DB_NAME = "healthcaredb"

TABLES = dict()
TABLES['appointments'] = (
    "CREATE TABLE IF NOT EXISTS `appointments` ("
    "   `id` INT NOT NULL AUTO_INCREMENT,"
    "   `employee_id` INT NOT NULL,"
    "   `patient_id` INT NOT NULL,"
    "   `date_time` DATETIME NOT NULL,"
    "   `completed` TINYINT NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['patients'] = (
    "CREATE TABLE IF NOT EXISTS `patients` ("
    "   `id` INT NOT NULL AUTO_INCREMENT,"
    "   `last_name` VARCHAR(30) NOT NULL,"
    "   `first_name` VARCHAR(30) NOT NULL,"
    "   `address` VARCHAR(75) NOT NULL,"
    "   `phone_number` VARCHAR(12) NOT NULL,"
    "   `email` VARCHAR(50) NOT NULL,"
    "   `ssn` VARCHAR(11) NOT NULL,"
    "   `insurance_provider` VARCHAR(50) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['employees'] = (
    "CREATE TABLE IF NOT EXISTS `employees` ("
    "   `id` INT NOT NULL AUTO_INCREMENT,"
    "   `last_name` VARCHAR(30) NOT NULL,"
    "   `first_name` VARCHAR(30) NOT NULL,"
    "   `type` TINYINT NOT NULL,"
    "   `associated_id` INT,"
    "   `password` VARCHAR(30) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['payments'] = (
    "CREATE TABLE IF NOT EXISTS `payments` ("
    "   `id` INT NOT NULL AUTO_INCREMENT,"
    "   `appointment_id` INT,"
    "   `amount` DECIMAL(7,2) ,"
    "   `method` TINYINT ,"
    "   `type` TINYINT NOT NULL,"
    "   `date_paid` DATETIME,"
    "   `reference_number` INT,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['reports'] = (
    "CREATE TABLE IF NOT EXISTS `reports` ("
    "   `id` INT NOT NULL AUTO_INCREMENT,"
    "   `type` SMALLINT NOT NULL,"
    "   `doctor_name` VARCHAR(30) NOT NULL,"
    "   `patient_count` SMALLINT NOT NULL,"
    "   `total_income` DECIMAL(10,2) NOT NULL,"
    "   `date_time` DATETIME DEFAULT CURRENT_TIMESTAMP,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['patientrecords'] = (
    "CREATE TABLE IF NOT EXISTS `patientrecords` ("
    "   `appointment_id` INT NOT NULL,"
    "   `weight` SMALLINT DEFAULT 0,"
    "   `height` SMALLINT DEFAULT 0,"
    "   `blood_pressure` SMALLINT DEFAULT 0,"
    "   `reason` VARCHAR(50),"
    "   `treatment_content` VARCHAR(50),"
    "   `prescription` VARCHAR(50),"
    "   PRIMARY KEY (`appointment_id`)"
    ") ENGINE=InnoDB")

TRIGGERS = dict()
TRIGGERS['appointment_added'] = ("CREATE TRIGGER appointment_added "
                                 "AFTER INSERT ON appointments "
                                 "FOR EACH ROW BEGIN "
                                 "INSERT INTO patientrecords (appointment_id) "
                                 "VALUES (NEW.id); "
                                 "INSERT INTO payments (appointment_id, type, "
                                 " amount) "
                                 "VALUES (NEW.id, 1, 50); "
                                 "INSERT INTO payments (appointment_id, type, "
                                 " amount) "
                                 "VALUES (NEW.id, 2, RAND()*(1300-100)+100); "
                                 "INSERT INTO payments (appointment_id, type, "
                                 " amount) "
                                 "VALUES (NEW.id, 3, 25);"
                                 "END;"
                                 )

TRIGGERS['appointment_deleted'] = ("CREATE TRIGGER appointment_deleted "
                                   "AFTER DELETE ON appointments "
                                   "FOR EACH ROW BEGIN "
                                   "DELETE FROM patientrecords WHERE "
                                   "appointment_id = OLD.id; "
                                   "DELETE FROM payments WHERE appointment_id "
                                   "= OLD.id; "
                                   "END;")

def init_connection(username=None, password=None):
    """Initializes connection to running MySQL server

    Connects to a running MySQL server using a username/password
    and returns the connection if successful.

    Args:
        username: the username of the account on the server to connect with
        password: the password of the account on the server to connect with
    Returns:
        connection: the open connection to the MySQL server
    Raises:
        InputError: The username or password input was incorrect

    """
    if not username or not password:
        username = input("Username: ")
        password = input("Password: ")

    try:
        connection = mysql.connector.connect(user=username,
                                             password=password)
    except mysql.connector.Error as err:
        raise InputError(message='There was a problem connecting. Please check'
                                 ' your username and password, and make sure'
                                 ' the server is running.',
                         args=err.args)
    return connection


def init_database(connection):
    """Initialize the database for use.

    Creates the DB_NAME database and creates any tables defined
    in TABLES dictionary inside of the newly created database

    Args:
         connection: the connection to the MySQL Server
    Raises:
         MySqlError: Raised if there is a connection error or SQL syntax error
    """
    create_db = 'CREATE DATABASE IF NOT EXISTS {}'.format(DB_NAME)
    try:
        cursor = connection.cursor()
        cursor.execute(create_db)  # Create the database
        connection.database = DB_NAME  # Connect to the database

        for name, query in TABLES.items():  # Create each table in the database
            print('Creating table {}'.format(name))
            cursor.execute(query)

        for name, sql in TRIGGERS.items():  # Create any triggers in TRIGGERS
            print('Creating trigger {}'.format(name))
            cursor.execute(sql)

        cursor.close()
    except mysql.connector.Error as err:
        raise MySqlError(message=err.msg,
                         args=err.args)


def main(username=None, password=None):
    cnx = init_connection(username, password)
    init_database(cnx)
    cnx.close()


if __name__ == '__main__':
    try:
        main()
    except (InputError, MySqlError) as db_exception:
        print(db_exception.message)
