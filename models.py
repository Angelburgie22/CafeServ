from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, func, select
from sqlalchemy import Integer, String, Boolean, DateTime, BINARY, Float
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
    id: Mapped[int] = mapped_column('platillo_id', Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(40))
    descripcion: Mapped[str] = mapped_column(String(250), default='')

class TipoAdimento(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(40))

    adimentos: Mapped[list['Adimento']] = relationship(back_populates='tipo_adimento')

class Adimento(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_id: Mapped[int] = mapped_column(ForeignKey(TipoAdimento.id))
    nombre: Mapped[str] = mapped_column(String(40))

    tipo_adimento: Mapped['TipoAdimento'] = relationship(back_populates='adimentos')


class Platillo_UnAdimento(Model):
    platillo_id: Mapped[int] = mapped_column(ForeignKey(Platillo.id), primary_key=True)
    adimento_id: Mapped[int] = mapped_column(ForeignKey(Adimento.id), primary_key=True)
    allowed: Mapped[bool] = mapped_column(Boolean)

    platillo: Mapped['Platillo'] = relationship()
    adimento: Mapped['Adimento'] = relationship()

class Platillo_TipoAdimento(Model):
    platillo_id: Mapped[int] = mapped_column(ForeignKey(Platillo.id), primary_key=True)
    tipo_adimento_id: Mapped[int] = mapped_column(ForeignKey(TipoAdimento.id), primary_key=True)

    platillo: Mapped['Platillo'] = relationship()
    tipo_adimento: Mapped['TipoAdimento'] = relationship()

fulladim_subq = select(
                        Platillo.id.label('id_platillo'),
                        Adimento.id.label('id_adimento'),
                        Adimento.nombre.label('nombre'),
                        Platillo_UnAdimento.allowed.label('allowed')
                    ).join(Platillo).join(Adimento)\
                    .union(
                            select(
                                Platillo.id,
                                Adimento.id,
                                Adimento.nombre,
                                True)
                            .join(TipoAdimento).join(Platillo_TipoAdimento).join(Platillo)
                        ).subquery()


Platillo_Adimento = view('platillo_adimento', Model.metadata,
                              select(fulladim_subq.c.id_platillo, fulladim_subq.c.id_adimento, fulladim_subq.c.nombre)
                              .group_by(fulladim_subq.c.id_platillo, fulladim_subq.c.id_adimento)
                              .having(func.min(fulladim_subq.c.allowed))
                              )

class Pedido(Model):
    id: Mapped[int] = mapped_column('pedido_id', Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(UserAccount.id), unique=True)
    status: Mapped[int] = mapped_column(TINYINT)

class Pedido_Platillo(Model):
    id: Mapped[int] = mapped_column('pedido_platillo_id', Integer, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey(Pedido.id), primary_key=True)
    platillo_id: Mapped[int] = mapped_column(ForeignKey(Platillo.id), primary_key=True)
    cantidad: Mapped[int] = mapped_column(Integer)

class Pedido_Ubicacion(Model):
    ubicacion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    coord_x: Mapped[float] = mapped_column(Float)
    coord_y: Mappped[float] = mapped_column(Float)
    pedido_id: Mapped[int] = mapped_column(ForeignKey(Pedido.id), unique=True)

class Pedido_Platillo_Adimento(Model):
    pedido_platillo_id: Mapped[int] = mapped_column(ForeignKey(Pedido_Platillo.id), primary_key=True)
    adimento_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Adimento.id), primary_key=True)
