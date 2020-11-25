#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sqlalchemy import Column, ForeignKey, Integer, Table, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy

if os.path.exists('test.db'):
    os.remove('test.db')
# tworzymy instancję klasy Engine do obsługi bazy
baza = create_engine('sqlite:///baza.db')  # ':memory:'

# klasa bazowa
BazaModel = declarative_base()

class SubjectGroup(BazaModel):
    __tablename__ = "SubjectGroups"
    subject_id = Column(Integer, ForeignKey('Subjects.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('Groups.id'), primary_key=True)

    subject = relationship("Subject", backref="group_associations")
    group = relationship("Group", backref="subject_associations")

class Subject(BazaModel):
    __tablename__ = 'Subjects'
    __mapper_args__ = {'polymorphic_identity': 'Subject'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
   
    groups = association_proxy("group_associations", "Group", creator=lambda c: SubjectGroup(group=c))

    grades = relationship("Grade", back_populates='subject')

class Group(BazaModel):
    __tablename__ = 'Groups'
    __mapper_args__ = {'polymorphic_identity': 'Group'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    students = relationship("Student", back_populates="group")
    
    subjects = association_proxy("subject_associations", "Subject", creator=lambda s: SubjectGroup(subject=s))
    

class Student(BazaModel):
    __tablename__ = 'Students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    grades = relationship('Grade', back_populates='student')

    group_id = Column(Integer, ForeignKey('Groups.id'))
    group = relationship('Group', back_populates='students')


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

    subject_id = Column(Integer, ForeignKey('Subjects.id'))
    subject = relationship('Subject', back_populates='grades')


BazaModel.metadata.create_all(baza)

BDSesja = sessionmaker(bind=baza)
sesja = BDSesja()

if not sesja.query(Subject).count():
    sesja.add(Subject(name = 'WDP'))
    sesja.add(Subject(name = 'C'))

if not sesja.query(Group).count():
    sesja.add(Group(name = 'EF'))
    sesja.add(Group(name = '2'))

if not sesja.query(SubjectGroup).count():
    sesja.add(SubjectGroup(subject_id = 1, group_id = 1))
    sesja.add(SubjectGroup(subject_id = 2, group_id = 1))
    sesja.add(SubjectGroup(subject_id = 2, group_id = 2))

if not sesja.query(Student).count():
    sesja.add(Student(first_name='Kryha', last_name='Szura', group_id = 1))
    sesja.add(Student(first_name='Madzionator', last_name='Madzik', group_id = 1))

if not sesja.query(GradeCategory).count():
    sesja.add(GradeCategory(name='Kolos1'))
    sesja.add(GradeCategory(name='Kolos2'))
    sesja.add(GradeCategory(name='Test'))

if not sesja.query(Grade).count():
    sesja.add(Grade(value = 5, grade_category_id = 3, student_id = 2, subject_id = 2))
    sesja.add(Grade(value = 5, grade_category_id = 3, student_id = 2, subject_id = 1))
    sesja.add(Grade(value = 5, grade_category_id = 2, student_id = 2, subject_id = 1))
    sesja.add(Grade(value = 2, grade_category_id = 3, student_id = 1, subject_id = 2))
    sesja.add(Grade(value = 3, grade_category_id = 1, student_id = 1, subject_id = 1))
    sesja.add(Grade(value = 3.5, grade_category_id = 2, student_id = 1, subject_id = 1))

#for dane in sesja.query(Grade.value, GradeCategory.name).join(GradeCategory, GradeCategory.id == Grade.grade_category_id).all():
#    print (dane)

#for dane in sesja.query(Grade.value, GradeCategory.name, Student.first_name).join(GradeCategory, GradeCategory.id == Grade.grade_category_id).join(Student, Student.id == Grade.student_id).all():
#    print (dane)

#for dane in sesja.query(Student.first_name, Student.last_name, Group.name).join(Group, Group.id == Student.group_id).all():
#    print (dane)

#for dane in sesja.query(Subject.name).all():
#    print(dane)

'''for dane in sesja.query(Student.first_name, 
                        Student.last_name, 
                        Grade.value,
                        GradeCategory.name,
                        Group.name,
                        Subject.name).join(
                            Group, 
                            Group.id == Student.group_id).join(
                                Grade, 
                                Grade.student_id == Student.id).join(
                                    Subject).join(
                                        GradeCategory, 
                                        Grade.grade_category_id == GradeCategory.id).order_by(Student.id).all():
    print(dane)'''

sesja.query()