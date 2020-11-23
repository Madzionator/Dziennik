#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

if os.path.exists('test.db'):
    os.remove('test.db')
# tworzymy instancję klasy Engine do obsługi bazy
baza = create_engine('sqlite:///test.db')  # ':memory:'

# klasa bazowa
BazaModel = declarative_base()

class Lecture(BazaModel):
    __tablename__ = 'przedmiot'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Group(BazaModel):
    __tablename__ = 'grupa'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class LectureGroup(BazaModel):
    __tablename__ = 'przedmiot_grupa'
    id = Column(Integer, primary_key=True)
    id_Lecture = Column(Integer, nullable=False)
    id_Group = Column(Integer, nullable=False)

class Student(BazaModel):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    id_group = Column(Integer, nullable=False)
