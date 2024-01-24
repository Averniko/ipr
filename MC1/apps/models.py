from sqlalchemy import Integer, Column, Sequence, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "message"

    message_id_seq = Sequence("message_id_seq", metadata=Base.metadata, start=1)
    id = Column(Integer, message_id_seq, primary_key=True, index=True, server_default=message_id_seq.next_value())
    session_id_seq = Sequence("session_id_seq", metadata=Base.metadata, start=1)
    session_id = Column(Integer, index=True, nullable=False)
    mc1_timestamp = Column(DateTime, nullable=True)
    mc2_timestamp = Column(DateTime, nullable=True)
    mc3_timestamp = Column(DateTime, nullable=True)
    end_timestamp = Column(DateTime, nullable=True)
