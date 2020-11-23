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
    __tablename__ = 'Lectures'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    group = relationship("LectureGroup", back_populates="lecture")

class Group(BazaModel):
    __tablename__ = 'Groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    group = relationship("LectureGroup", back_populates="group")
    student = relationship("Student", back_populates="group")

class LectureGroup(BazaModel):
    __tablename__ = 'LectureGroups'
    id = Column(Integer, primary_key=True)
    id_Lecture = Column(Integer, nullable=False)
    id_Group = Column(Integer, nullable=False)

    lecture = Column(Integer, ForeignKey('Lectures.id'))
    lecturegroup = relationship("Lecture", back_populates="group")

    group_id = Column(Integer, ForeignKey('Groups.id'))
    lecturegroup = relationship("Group", back_populates="lecture")


class Student(BazaModel):
    __tablename__ = 'Students'
    id = Column(Integer, primary_key=True)
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    id_group = Column(Integer, nullable=False)

    group_id = Column(Integer, ForeignKey('Groups.id'))
    group = relationship("Group", back_populates="student")

BazaModel.metadata.create_all(baza)