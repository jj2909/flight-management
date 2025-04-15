from dataclasses import Field
from base.connection import db_connection
from base.logger import logger
import inspect
from typing import Type, Iterable


class DB:
    __SUBCLASSES__: dict[[str, Type["DB"]]] = {}

    __TYPE_MAP: dict[str, str] = {
        "int": "INTEGER",
        "str": "TEXT",
        "NoneType": "NULL",
        "float": "REAL",
    }

    def __init_subclass__(cls, primary_key="id", **kwargs):
        cls.primary_key = primary_key
        DB.__SUBCLASSES__[cls.__name__] = cls

    @staticmethod
    def get_class_fields(cls: Type["DB"]) -> Iterable[Field]:
        members = inspect.getmembers(cls)
        return dict(members)["__dataclass_fields__"].values()

    @classmethod
    def intialise_all(cls):
        with db_connection() as connection:
            for k, v in DB.__SUBCLASSES__.items():
                logger.info(f"{k} creating key automatically")
                fields = DB.get_class_fields(v)

                sqlite_fields = []
                fk_fields = []
                for field in fields:

                    if field.name == v.primary_key:
                        primary_type = DB.__TYPE_MAP.get(field.type.__name__, "INTEGER")

                    if field.name != v.primary_key:
                        sqlite_fields.append(
                            f'{field.name} {DB.__TYPE_MAP.get(field.type.__name__, "TEXT")}'
                        )
                    if field.metadata.get("foreign_key"):
                        fk_fields.append(
                            f'FOREIGN KEY ({field.name}) REFERENCES {field.metadata.get("foreign_key")["table"]}({field.metadata.get("foreign_key")["column"]})'
                        )

                if fk_fields:
                    sqlite_fields.extend(fk_fields)

                create_table = f"CREATE TABLE IF NOT EXISTS {k} ({v.primary_key} {primary_type} PRIMARY KEY, {", ".join(sqlite_fields)})"
                logger.info(f"running sql {create_table}")
                connection.execute(create_table)

    def drop_table(cls) -> None:
        with db_connection() as connection:
            drop_table = f"DROP TABLE IF EXISTS {cls.__name__}"
            logger.info(f"running sql {drop_table}")
            connection.execute(drop_table)

    def drop_all() -> None:
        with db_connection() as connection:
            for k, _ in DB.__SUBCLASSES__.items():
                drop_table = f"DROP TABLE IF EXISTS {k}"
                logger.info(f"running sql {drop_table}")
                connection.execute(drop_table)

    def insert(self) -> None:
        fields = DB.get_class_fields(self.__class__)
        names = [field.name for field in fields]
        names_key = ",".join(names)
        questions = ",".join(["?"] * len(names))
        insert_query = (
            f"INSERT INTO {self.__class__.__name__}({names_key}) VALUES ({questions})"
        )

        with db_connection() as connection:
            cursor = connection.cursor()
            logger.info(f"running following insert query {insert_query}")
            cursor.execute(insert_query, tuple([getattr(self, name) for name in names]))
            connection.commit()

    @staticmethod
    def get_foreign_keys(cls: Type["DB"]) -> list[dict]:
        result = []
        for f in DB.get_class_fields(cls):
            fk_meta = f.metadata.get("foreign_key")
            if fk_meta:
                result.append(
                    {
                        "from_column": f.name,
                        "to_table": fk_meta["table"],
                        "to_column": fk_meta["column"],
                        "alias": fk_meta.get("alias", fk_meta["table"]),
                    }
                )
        return result

    @classmethod
    def find_all(cls) -> list[dict]:
        with db_connection() as connection:
            cursor = connection.cursor()
            rows = cursor.execute(f"SELECT * FROM {cls.__name__}")
            # return [cls(**row) for row in rows]
            return [dict(row) for row in rows]

    @classmethod
    def find_all_with_details(cls) -> list[dict]:

        def get_columns_with_alias(table: str, alias: str, connection) -> list[str]:
            cursor = connection.execute(f"PRAGMA table_info({table})")
            return [
                f"{alias}.{row[1]} AS {alias.lower()}_{row[1]}"
                for row in cursor.fetchall()
            ]

        with db_connection() as connection:
            select_clauses = get_columns_with_alias(
                cls.__name__, cls.__name__, connection
            )

        fk = DB.get_foreign_keys(cls)
        select_tables = [f"{cls.__name__}.*"]
        joins = []
        for key in fk:
            select_clauses += get_columns_with_alias(
                key["to_table"], key["alias"], connection
            )
            select_tables.append(f"{key['alias']}.*")
            joins.append(
                f"LEFT JOIN {key['to_table']} AS {key['alias']} ON {cls.__name__}.{key['from_column']} = {key['alias']}.{key['to_column']}"
            )

        query = (
            f"SELECT {', '.join(select_clauses)} FROM {cls.__name__} {' '.join(joins)}"
        )

        with db_connection() as connection:
            cursor = connection.cursor()
            logger.info(f"running find_all_with_details query: {query}")
            rows = cursor.execute(query).fetchall()
            return [dict(row) for row in rows]

    @classmethod
    def find_by_id(cls, ids: list[int], key: str = None):
        questions = ", ".join(["?"] * len(ids))
        query = f"SELECT * FROM {cls.__name__} WHERE {key if key else cls.primary_key} IN ({questions})"
        with db_connection() as connection:
            cursor = connection.cursor()
            logger.info(f"running find_by_id query: {query} with ids {ids}")
            rows = cursor.execute(query, ids)
            return [dict(row) for row in rows]

    @classmethod
    def delete_by_id(cls, ids: list[int], key: str = None) -> None:
        questions = ", ".join(["?"] * len(ids))
        query = f"DELETE FROM {cls.__name__} WHERE {key if key else cls.primary_key} IN ({questions})"
        with db_connection() as connection:
            cursor = connection.cursor()
            logger.info(f"running delete query: {query} with ids {ids}")
            cursor.execute(query, ids)
            connection.commit()

    @classmethod
    def update_by_id(cls, data: dict, key: str = None) -> None:
        if not key:
            key = cls.primary_key

        if key not in data:
            raise ValueError(f"Key {key} missing")

        questions = ", ".join([f"{col} = ?" for col in data if col != key])
        values = [v for col, v in data.items() if col != key]
        values.append(data[key])

        query = f"UPDATE {cls.__name__} SET {questions} WHERE {key} = ?"
        with db_connection() as connection:
            cursor = connection.cursor()
            logger.info(f"running update query: {query} with values {values}")
            cursor.execute(query, values)
            connection.commit()
