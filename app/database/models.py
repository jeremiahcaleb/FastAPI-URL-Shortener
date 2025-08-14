from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class DBUser(Base):
    __tablename__ = "users"  # table names usually lowercase

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)

    urls = relationship("DBUrl", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DBUser(user_name='{self.user_name}', email='{self.email}')>"


class DBUrl(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String(200), nullable=False)
    short_url = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(400), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("DBUser", back_populates="urls")

    def __repr__(self):
        return f"<DBUrl(short_url='{self.short_url}', long_url='{self.long_url}')>"
