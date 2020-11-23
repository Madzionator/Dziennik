#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sqlalchemy import Column, ForeignKey, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

if os.path.exists('test.db'):
    os.remove('test.db')
# tworzymy instancję klasy Engine do obsługi bazy
baza = create_engine('sqlite:///baza.db')  # ':memory:'

# klasa bazowa
BazaModel = declarative_base()


'''class Lecture(BazaModel):
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
    lecturegroup = relationship("Group", back_populates="lecture") '''

    #ponizej git

class Student(BazaModel):
    __tablename__ = 'Students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    grades = relationship('Grade', back_populates='student')

    #group_id = Column(Integer, ForeignKey('Groups.id'))
    #group = relationship("Group", back_populates="student")

class GradeCategory(BazaModel):
    __tablename__ = 'GradeCategories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    grades = relationship('Grade', back_populates='grade_category')

class Grade(BazaModel):
    __tablename__ = 'Grades'
    id = Column(Integer, primary_key = True)
    value = Column(Float, nullable=False)
    grade_category_id = Column(Integer, ForeignKey('GradeCategories.id'))
    grade_category = relationship('GradeCategory', back_populates='grades')
    student_id = Column(Integer, ForeignKey('Students.id'))
    student = relationship('Student', back_populates='grades')
    #lecture_id = Column(Integer, nullable = False)


BazaModel.metadata.create_all(baza)

BDSesja = sessionmaker(bind=baza)
sesja = BDSesja()

if not sesja.query(Student).count():
    sesja.add(Student(first_name='Kryha', last_name='Szura'))
    sesja.add(Student(first_name='Madzionator', last_name='Madzik'))

if not sesja.query(GradeCategory).count():
    sesja.add(GradeCategory(name='Kolos1'))
    sesja.add(GradeCategory(name='Kolos2'))
    sesja.add(GradeCategory(name='Test'))

if not sesja.query(Grade).count():
    sesja.add(Grade(value = 4, grade_category_id = 3, student_id = 2))
    sesja.add(Grade(value = 3, grade_category_id = 2, student_id = 1))
    sesja.add(Grade(value = 5, grade_category_id = 2, student_id = 2))

#for student in sesja.query(Student).all():
#    print(student.id, student.FirstName, student.LastName)

for dane in sesja.query(Grade.value, GradeCategory.name).join(GradeCategory, GradeCategory.id == Grade.grade_category_id).all():
    print (dane)

for dane in sesja.query(Grade.value, GradeCategory.name, Student.first_name).join(GradeCategory, GradeCategory.id == Grade.grade_category_id).join(Student, Student.id == Grade.student_id).all():
    print (dane)