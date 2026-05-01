from sqlalchemy import Table, Column, ForeignKey, func, select
from sqlalchemy import Integer, String, Boolean, DateTime, BINARY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.mysql import TINYINT
from view import view
from typing import Optional
from datetime import datetime as Datetime
from database import Model

class UserAccount(Model):
    id: Mapped[int] = mapped_column('account_id', Integer, primary_key=True)
    creation_time: Mapped[Datetime] = mapped_column(DateTime)
    status: Mapped[int] = mapped_column(TINYINT)
    email: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(24))
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(24))

    login_info: Mapped['UserLoginInfo'] = relationship(back_populates='account')
    logged_sessions: Mapped[list['UserSession']] = relationship(back_populates='account')

class UserLoginInfo(Model):
    account_id: Mapped[int] = mapped_column(ForeignKey(UserAccount.id),
                                    primary_key=True)
    passwd_hash: Mapped[str] = mapped_column(String(255))

    account: Mapped['UserAccount'] = relationship(back_populates='login_info')

class UserSession(Model):
    id: Mapped[bytes] = mapped_column('session_id', String(64), primary_key=True)
    account_id: Mapped[Optional[int]] = mapped_column(ForeignKey(UserAccount.id))
    creation_time: Mapped[Datetime] = mapped_column(DateTime, server_default=func.now())
    expiration_time: Mapped[Datetime] = mapped_column(DateTime)

    account: Mapped[Optional['UserAccount']] = relationship(back_populates='logged_sessions')

class CSRFToken(Model):
    __tablename__ = 'csrf_token'
    token: Mapped[bytes] = mapped_column('csrf_token', String(64), primary_key=True)
    creation_time: Mapped[Datetime] = mapped_column(DateTime, server_default=func.now())
    expiration_time: Mapped[Datetime] = mapped_column(DateTime)


class Dish(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(250), default='')

class IngredientType(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))

    ingredients: Mapped[list['Ingredient']] = relationship(back_populates='type')

class Ingredient(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey(IngredientType.id))
    name: Mapped[str] = mapped_column(String(40))

    type: Mapped['IngredientType'] = relationship(back_populates='ingredients')


class DishIngredient(Model):
    dish_id: Mapped[int] = mapped_column(ForeignKey(Dish.id), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey(Ingredient.id), primary_key=True)
    allowed: Mapped[bool] = mapped_column(Boolean)

    dish: Mapped['Dish'] = relationship()
    ingredient: Mapped['Ingredient'] = relationship()

class DishIngredientType(Model):
    dish_id: Mapped[int] = mapped_column(ForeignKey(Dish.id), primary_key=True)
    ingredient_type_id: Mapped[int] = mapped_column(ForeignKey(IngredientType.id), primary_key=True)

    dish: Mapped['Dish'] = relationship()
    ingredient_type: Mapped['IngredientType'] = relationship()

full_dish_ingredient_subq = select(
                        Dish.id.label('id_dish'),
                        Ingredient.id.label('id_ingredient'),
                        Ingredient.name.label('name'),
                        DishIngredient.allowed.label('allowed')
                    ).join(Dish).join(Ingredient)\
                    .union(
                            select(
                                Dish.id,
                                Ingredient.id,
                                Ingredient.name,
                                True)
                            .join(IngredientType).join(DishIngredientType).join(Dish)
                        ).subquery()


DishIngredientView = view('dish_ingredient_view', Model.metadata,
                              select(full_dish_ingredient_subq.c.id_dish, full_dish_ingredient_subq.c.id_ingredient, full_dish_ingredient_subq.c.name)
                              .group_by(full_dish_ingredient_subq.c.id_dish, full_dish_ingredient_subq.c.id_ingredient)
                              .having(func.min(full_dish_ingredient_subq.c.allowed))
                              )

