from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, DateTime, BINARY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.mysql import TINYINT
from typing import Optional
from database import Model

class UserAccount(Model):
    id: Mapped[int] = mapped_column('account_id', Integer, primary_key=True)
    creation_time: Mapped[str] = mapped_column(DateTime)
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

    account: Mapped[Optional['UserAccount']] = relationship(back_populates='logged_sessions')

class CSRF_Token(Model):
    __tablename__ = 'csrf_token'
    token: Mapped[bytes] = mapped_column('csrf_token', String(64), primary_key=True)

