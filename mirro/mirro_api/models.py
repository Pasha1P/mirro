# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccessToEdit(models.Model):
    pk_access_to_edit = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey('User', models.DO_NOTHING, db_column='fk_user')
    fk_board = models.ForeignKey('Board', models.DO_NOTHING, db_column='fk_board')
    author = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'access_to_edit'


class Board(models.Model):
    pk_board = models.AutoField(primary_key=True)
    total_likes = models.IntegerField()
    title = models.CharField(max_length=100)
    is_published = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'board'


class Shape(models.Model):
    pk_shape = models.AutoField(primary_key=True)
    properties = models.JSONField()
    fk_type = models.ForeignKey('Type', models.DO_NOTHING, db_column='fk_type')
    fk_board = models.ForeignKey(Board, models.DO_NOTHING, db_column='fk_board')

    class Meta:
        managed = False
        db_table = 'shape'


class Type(models.Model):
    pk_type = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'type'


class User(models.Model):
    pk_user = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'
