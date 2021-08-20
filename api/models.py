from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    moderated = Column(Boolean)
    premium = Column(Boolean)
    subsection_id = Column(Integer, ForeignKey("sections.id"))

    subsections = relationship("Section")


class Moderator(Base):
    __tablename__ = "moderators"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    section = relationship("Section", back_populates="moderators")
    users = relationship("User", back_populates="moderators")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    paper_id = Column(Integer, ForeignKey("papers.id"))

    paper = relationship("Paper", back_populates="tags")


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(2048))
    section_id = Column(Integer, ForeignKey("sections.id"))

    section = relationship("Section", back_populates="papers")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(256))
    user_id = Column(Integer, ForeignKey("users.id"))
    responses_id = Column(Integer, ForeignKey("comments.id"))

    users = relationship("User", back_populates="moderators")
    responses = relationship("Comment")
