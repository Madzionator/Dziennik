#!  /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from sqlalchemy import Column, ForeignKey, Integer, Table, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy

baza = create_engine('sqlite:///baza.db')
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
   
    groups = association_proxy("group_associations", "group", creator=lambda c: SubjectGroup(group=c))

    grades = relationship("Grade", back_populates='subject')

class Group(BazaModel):
    __tablename__ = 'Groups'
    __mapper_args__ = {'polymorphic_identity': 'Group'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    students = relationship("Student", back_populates="group")
    
    subjects = association_proxy("subject_associations", "subject", creator=lambda s: SubjectGroup(subject=s))
    

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
    weight = Column(Integer, nullable=False)

    grade_category_id = Column(Integer, ForeignKey('GradeCategories.id'))
    grade_category = relationship('GradeCategory', back_populates='grades')

    student_id = Column(Integer, ForeignKey('Students.id'))
    student = relationship('Student', back_populates='grades')

    subject_id = Column(Integer, ForeignKey('Subjects.id'))
    subject = relationship('Subject', back_populates='grades')


BazaModel.metadata.create_all(baza)

BDSesja = sessionmaker(bind=baza)
sesja = BDSesja()

if not sesja.query(GradeCategory).count():
    sesja.add(GradeCategory(name='zadanie'))
    sesja.add(GradeCategory(name='sprawozdanie'))
    sesja.add(GradeCategory(name='test'))
    sesja.add(GradeCategory(name='egzamin'))
