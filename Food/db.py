import datetime
from typing import List
# from sqlalchemy import UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
# from sqlalchemy import create_engine
# from sqlalchemy import select
# from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(100))
    user_ref: Mapped["Meal_schedule"] = relationship(back_populates="users_ref")

    def __repr__(self) -> str:
        return f"users(user_id={self.user_id!r}, login={self.login!r}, email={self.email!r}, password={self.password!r})" 
    

class Food(Base):
    __tablename__ = "food"
    food_id: Mapped[int] = mapped_column(primary_key=True)
    dish: Mapped[str] = mapped_column(String(20))
    calories: Mapped[int] = mapped_column(Integer)
    food_ref: Mapped["Meal_schedule"] = relationship(back_populates="food_ref")

    def __repr__(self) -> str:
        return f"food(food_id={self.food_id}, dish={self.dish}, calories={self.calories})"

class Meal_schedule(Base):
    __tablename__ = "meal_schedule"
    meal_schedule_id: Mapped[int] = mapped_column(primary_key=True)
    food: Mapped[List["Food"]] = mapped_column(ForeignKey("food.food_id"))
    time: Mapped[datetime.time] = mapped_column(DateTime)
    user: Mapped[List["User"]] = mapped_column(ForeignKey("users.user_id"))

    def __repr__(self) -> str:
        return f"meal_schedule(maeal_schedule_id={self.meal_schedule_id}, food={self.food}, time={self.time}, user={self.user})"