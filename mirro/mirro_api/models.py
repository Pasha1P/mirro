# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Acces(models.Model):
    pk_acces = models.AutoField(primary_key=True)
    fk_users = models.ForeignKey('Users', models.DO_NOTHING, db_column='fk_users')
    fk_wall = models.ForeignKey('Wall', models.DO_NOTHING, db_column='fk_wall')

    class Meta:
        managed = False
        db_table = 'acces'


class Elements(models.Model):
    pk_element = models.AutoField(primary_key=True)
    json = models.JSONField()
    fk_type = models.ForeignKey('Type', models.DO_NOTHING, db_column='fk_type')
    fk_wall = models.ForeignKey('Wall', models.DO_NOTHING, db_column='fk_wall')

    class Meta:
        managed = False
        db_table = 'elements'


class Type(models.Model):
    pk_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'type'


class Users(models.Model):
    pk_users = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=45)
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'users'


class Vievs(models.Model):
    pk_vievs = models.AutoField(primary_key=True)
    like = models.CharField(max_length=1, blank=True, null=True)
    fk_users = models.ForeignKey(Users, models.DO_NOTHING, db_column='fk_users')
    fk_wall = models.ForeignKey('Wall', models.DO_NOTHING, db_column='fk_wall')

    class Meta:
        managed = False
        db_table = 'vievs'


class Wall(models.Model):
    pk_wall = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'wall'
