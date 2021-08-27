from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Boolean, Integer, String, ForeignKey


Base = declarative_base()


UserModerators = Table("userModerators",
                       Base.metadata,
                       Column("user_id", Integer, ForeignKey("users.id")),
                       Column("section_id", Integer, ForeignKey("sections.id")))

SectionArticles = Table("sectionArticles",
                        Base.metadata,
                        Column("section_id", Integer, ForeignKey("sections.id")),
                        Column("article_id", Integer, ForeignKey("articles.id")))

TagArticles = Table("tagArticles",
                    Base.metadata,
                    Column("tag_id", Integer, ForeignKey("tags.id")),
                    Column("article_id", Integer, ForeignKey("articles.id")))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    moderated = Column(Boolean)
    premium = Column(Boolean)
    parent_section_id = Column(Integer, ForeignKey("sections.id"))

    moderators = relationship("User", secondary=UserModerators, backref="moderates")
    articles = relationship("Article", secondary=SectionArticles, backref="sections")
    subsections = relationship("Section")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "moderated": self.moderated,
            "premium": self.premium,
            "parent_section_id": self.parent_section_id,
            "subsections": self.serialize_subsections
        }

    @property
    def serialize_subsections(self):
        return [subsection.serialize for subsection in self.subsections]


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(2048))

    tags = relationship("Tag", secondary=TagArticles, backref="articles")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(256))
    response_id = Column(Integer, ForeignKey("comments.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))

    article = relationship("Article", backref="comments")
    responses = relationship("Comment")
