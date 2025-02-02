# ./models.py
from sqlalchemy import INTEGER, Column, ForeignKey, String, DECIMAL, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(INTEGER(), primary_key=True)

class User(BaseModel):
    __tablename__ = "user"
    full_name = Column(String())
    email = Column(String(), unique=True)
    hashed_password = Column(String())

    def to_dict(self):
        return {"id": self.id,
             "email": self.email,
             "full_name": self.full_name
         }
    accounts = relationship("Account", back_populates='user')


class Administrator(BaseModel):
    __tablename__ = "administrator"

    full_name = Column(String())
    email = Column(String())
    hashed_password = Column(String())

class Account(BaseModel):
    __tablename__ = "account"

    balance = Column(DECIMAL(12, 2))
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates='accounts')

    replenishments = relationship("Replenishment", back_populates='account')
    def to_dict(self):
        return {"id": self.id,
                "balance": self.balance,
                "user_id": self.user_id}

class Replenishment(BaseModel):
    __tablename__ = "replenishment"

    amount = Column(DECIMAL(12, 2))
    account_id = Column(ForeignKey("account.id", ondelete="CASCADE"))
    is_executed = Column(Boolean())

    account = relationship("Account", back_populates='replenishments')

if __name__ == '__main__':
    from sqlalchemy import create_engine
    DB_CONN = 'postgresql://test:5qJZDWLLNlHFEdR56rn8mJRg03sno3V1@dpg-cueg6thu0jms73caudl0-a.oregon-postgres.render.com/db_cvs5'

    engine = create_engine(DB_CONN)
    Base.metadata.create_all(engine)
