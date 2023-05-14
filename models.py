from sqlalchemy import Table, Column, ForeignKey, func
from sqlalchemy import Integer, String, Boolean, DateTime, BINARY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.mysql import TINYINT
from typing import Optional
from datetime import datetime as Datetime
from database import Model

class UserAccount(Model):
    id: Mapped[int] = mapped_column('account_id', Integer, primary_key=True)
    creation_time: Mapped[Datetime] = mapped_column(DateTime)
    status: Mapped[int] = mapped_column(TINYINT)
    email: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(24))
    nombre: Mapped[str] = mapped_column(String(32))
    apellido_p: Mapped[Optional[str]] = mapped_column(String(24))
    apellido_m: Mapped[Optional[str]] = mapped_column(String(24))

    login_info: Mapped['UserLoginInfo'] = relationship(back_populates='account')
    logged_sessions: Mapped[list['UserSession']] = relationship(back_populates='account')

class UserLoginInfo(Model):
    account_id: Mapped[int] = mapped_column(ForeignKey(UserAccount.id),
                                    primary_key=True)
    passwd_hash: Mapped[bytes] = mapped_column(String(128))

    account: Mapped['UserAccount'] = relationship(back_populates='login_info')

class UserSession(Model):
    id: Mapped[bytes] = mapped_column('session_id', String(64), primary_key=True)
    account_id: Mapped[Optional[int]] = mapped_column(ForeignKey(UserAccount.id))
    creation_time: Mapped[Datetime] = mapped_column(DateTime, server_default=func.now())
    expiration_time: Mapped[Datetime] = mapped_column(DateTime)

    account: Mapped[Optional['UserAccount']] = relationship(back_populates='logged_sessions')

class CSRF_Token(Model):
    __tablename__ = 'csrf_token'
    token: Mapped[bytes] = mapped_column('csrf_token', String(64), primary_key=True)
    creation_time: Mapped[Datetime] = mapped_column(DateTime, server_default=func.now())
    expiration_time: Mapped[Datetime] = mapped_column(DateTime)


class Platillo(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(40))
    descripcion: Mapped[Optional[str]] = mapped_column(String(250))

class TipoAdimento(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(40))

    adimentos: Mapped[list['Adimento']] = relationship(back_populates='tipo_adimento')

class Adimento(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_id: Mapped[int] = mapped_column(ForeignKey(TipoAdimento.id))
    nombre: Mapped[str] = mapped_column(String(40))

    tipo_adimento: Mapped['TipoAdimento'] = relationship(back_populates='adimentos')


class Platillo_Adimento(Model):
    __tablename__ = 'platillo_adimento'
    platillo_id: Mapped[int] = mapped_column(ForeignKey(Platillo.id), primary_key=True)
    adimento_id: Mapped[int] = mapped_column(ForeignKey(Adimento.id), primary_key=True)
    allowed: Mapped[bool] = mapped_column(Boolean)

    platillo: Mapped['Platillo'] = relationship()
    adimento: Mapped['Adimento'] = relationship()

class Platillo_TipoAdimento(Model):
    __tablename__ = 'platillo_tipo_adimento'
    platillo_id: Mapped[int] = mapped_column(ForeignKey(Platillo.id), primary_key=True)
    tipo_adimento_id: Mapped[int] = mapped_column(ForeignKey(TipoAdimento.id), primary_key=True)

    platillo: Mapped['Platillo'] = relationship()
    tipo_adimento: Mapped['TipoAdimento'] = relationship()

