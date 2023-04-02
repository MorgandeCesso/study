from ast import Add
from typing import List

from sqlalchemy import UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Checkers(Base):
    __tablename__ = "checkers"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(15))
    secondname: Mapped[str] = mapped_column(String(15))
    lastname: Mapped[str] = mapped_column(String(15))
    sp_ref: Mapped["Second_Parts"] = relationship(back_populates="checkers_ref")

    def __repr__(self) -> str:
        return f"checkers(id={self.id!r}, firstname={self.firstname!r}, secondnamne={self.secondname!r}, lastname={self.lastname!r})"
    
class Subjects(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(15))
    ticket_ref: Mapped["Ticket"] = relationship(back_populates="subject_ref")

    def __repr__(self) -> str:
        return f"subjects(id={self.id!r}, subject_name={self.subject_name!r})"
    
class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    variant: Mapped[int] = mapped_column(Integer)
    subject_id: Mapped[List["Subjects"]] = mapped_column(ForeignKey("subjects.id"))
    subject_ref: Mapped["Subjects"] = relationship(back_populates="ticket_ref")
    samples_ref: Mapped["First_Part_Samples"] = relationship(back_populates="ticket_ref")
    students_ref: Mapped["Students"] = relationship(back_populates="ticket_ref")
    fp_ref: Mapped["First_Parts"] = relationship(back_populates="ticket_ref")
    sp_ref: Mapped["Second_Parts"] = relationship(back_populates="ticket_ref")
    
    def __repr__(self) -> str:
        return f"ticket(id={self.id!r}, variant={self.variant!r})"

class First_Part_Samples(Base):
    __tablename__ = "samples"
    id: Mapped[int] = mapped_column(primary_key= True)
    question_number: Mapped[int] = mapped_column(Integer)
    correct_answer: Mapped[int] = mapped_column(Integer)
    ticket_id: Mapped[List["Ticket"]] = mapped_column(ForeignKey("tickets.id"))
    ticket_ref: Mapped["Ticket"] = relationship(back_populates="samples_ref")

    def __repr__(self) -> str:
        return f"first_part_samples(id={self.id!r}, question_number={self.question_number!r}, correct_answer={self.correct_answer!r})"
    
class Students(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(15))
    secondname: Mapped[str] = mapped_column(String(15))
    lastname: Mapped[str] = mapped_column(String(15))
    passport: Mapped[int] = mapped_column(Integer)
    ticket_id: Mapped[List["Ticket"]] = mapped_column(ForeignKey("tickets.id"))
    ticket_ref: Mapped["Ticket"] = relationship(back_populates="students_ref")
    __table_args__ = (UniqueConstraint(passport),)

    def __repr__(self) -> str:
        return f"students(id={self.id!r}, firstname={self.firstname!r}, secondname={self.secondname!r}, lastname={self.lastname!r}, passport={self.passport!r}, ticket_id={self.ticket_id!r})"

class First_Parts(Base):
    __tablename__ = "first_part"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_number: Mapped[int] = mapped_column(Integer)
    reply: Mapped[int] = mapped_column(Integer)
    ticket_id: Mapped[List["Ticket"]] = mapped_column(ForeignKey("tickets.id"))
    ticket_ref: Mapped["Ticket"] = relationship(back_populates="fp_ref")
    def __repr__(self) -> str:
        return f"first_part(id={self.id!r}, question_number={self.question_number!r}, reply={self.reply!r}, ticket_id={self.ticket_id!r})"


class Second_Parts(Base):
    __tablename__ = "second_parts"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_number: Mapped[int] = mapped_column(Integer)
    reply: Mapped[str] = mapped_column(String(100))
    checker_id: Mapped[List["Checkers"]] = mapped_column(ForeignKey("checkers.id"))
    ticket_id: Mapped[List["Ticket"]] = mapped_column(ForeignKey("tickets.id"))
    checkers_ref: Mapped["Checkers"] = relationship(back_populates="sp_ref")
    ticket_ref: Mapped["Ticket"] = relationship(back_populates="sp_ref")

engine = create_engine("postgresql+psycopg2://postgres:Maximsid2003@localhost:5432/test", echo=True)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:

    checker1 = Checkers(
        firstname = "Олег",
        secondname = "Иванович",
        lastname = "Шукшин",
    )

    checker2 = Checkers(
        firstname = "Иван",
        secondname = "Петрович",
        lastname = "Зиновьев",
    )

    subject = Subjects(
        subject_name = "Математика"
    )
    session.add_all([checker1, checker2, subject])
    session.commit()

    st = select(Checkers.id, Checkers.firstname).order_by(Checkers.id.desc())
    print()
    print("Печать запроса")
    print(st)

    print()
    print("Выполнение запроса")
    result = session.execute(st).fetchall()

    print()
    print("Результат")
    for i in result:
        print(i)