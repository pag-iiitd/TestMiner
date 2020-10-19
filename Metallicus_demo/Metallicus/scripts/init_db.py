"""This file contains the code to generate the DB schema."""

from peewee import (SqliteDatabase, Model, AutoField, CharField, TextField,
                    ForeignKeyField, DoubleField, BooleanField, IntegerField)

db = SqliteDatabase('crosslib_final_full.db')


class BaseModel(Model):
    """Base model to attach table to the database."""

    class Meta:
        """Defines which db to use."""

        database = db


class Functions(BaseModel):
    """This class provides abstract model for Functions table."""

    fn_id = IntegerField(primary_key=True)  # Primary Key
    fn_signature = CharField(max_length=100, index=True, null=False)
    documentation = TextField(index=True, null=True)
    repo_path = TextField(null=False)
    library_name = CharField(max_length=100, index=True, null=False)
    code = TextField(null=False)
    test_fp = TextField(null=True)


class Cluster_Functions(BaseModel):
    """This class provides abstract model for Cluster Function map."""
    cluster_id = CharField(max_length=10, index=True, null=False)
    fn_id = ForeignKeyField(Functions)
    sm_id = CharField(max_length=20, index=True, null=True)


# class Function_Tests(BaseModel):
#     """This class provides an abstract model for Matches table."""
#     fn_id = ForeignKeyField(Functions)
#     test_fp = TextField(null=False)


# Connect to our database.
db.connect()

# Create the tables.
db.create_tables([Functions, Cluster_Functions])
