import sqlite3


class Field:
    db_type = None

    def __init__(self):
        pass


class IntegerField(Field):
    db_type = "INTEGER"


class CharField(Field):
    db_type = "CHARACTER VARYING"


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


class ModelMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if not hasattr(cls, "fields"):
            cls.fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                cls.fields[key] = value


class Model(metaclass=ModelMeta):
    _db = None

    @classmethod
    def connect(cls, db_file):
        cls._db = Database(db_file)

    @classmethod
    def disconnect(cls):
        cls._db.close()

    @classmethod
    def create_table(cls):
        table_name = cls.__name__.lower()
        field_definitions = []
        for field_name, field in cls.fields.items():
            field_definitions.append(f"{field_name} {field.db_type}")
        field_definitions_str = ", ".join(field_definitions)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions_str})"
        cls._db.execute(query)
        cls._db.commit()

    @classmethod
    def drop_table(cls):
        table_name = cls.__name__.lower()
        query = f"DROP TABLE IF EXISTS {table_name}"
        cls._db.execute(query)
        cls._db.commit()

    @classmethod
    def insert(cls, **kwargs):
        table_name = cls.__name__.lower()
        columns = []
        values = []
        for key, value in kwargs.items():
            columns.append(key)
            values.append(value)
        columns_str = ", ".join(columns)
        placeholders_str = ", ".join(["?"] * len(values))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders_str})"
        cls._db.execute(query, values)
        cls._db.commit()

    @classmethod
    def select(cls, **kwargs):
        table_name = cls.__name__.lower()
        query = f"SELECT * FROM {table_name} WHERE "
        values = []
        for key, value in kwargs.items():
            query += f"{key}=? AND "
            values.append(value)
        query = query[:-5]
        cls._db.execute(query, values)
        rows = cls._db.cursor.fetchall()
        results = []
        for row in rows:
            instance = cls()
            for i, field_name in enumerate(cls.fields):
                setattr(instance, field_name, row[i])
            results.append(instance)
        return results


class User(Model):
    name = CharField()
    age = IntegerField()
    email = CharField()


if __name__ == "__main__":
    # Example usage
    User.connect("test.db")
    User.create_table()
    User.insert(name="Alice", age=25, email="alice@example.com")
    User.insert(name="Bob", age=30, email="bob@example.com")
    users = User.select(name="Alice")

    for user in users:
        print(user.name, user.age, user.email)
        