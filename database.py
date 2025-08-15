from peewee import *

db = SqliteDatabase('rental.db')

class House(Model):
    name = CharField()
    rent = FloatField()
    status = CharField(default='vacant')  # 'vacant' or 'occupied'
    class Meta:
        database = db

class Tenant(Model):
    name = CharField()
    house = ForeignKeyField(House, backref='tenants')
    paid_status = BooleanField(default=False)  # Track payment status
    due_date = DateField()  # Add if missing
    class Meta:
        database = db

db.create_tables([House, Tenant])