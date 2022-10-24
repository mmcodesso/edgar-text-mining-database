from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class form_index(Base):
    __tablename__ = "form_index"

    form_index = Column(String, primary_key=True)
    status = Column(Integer)
    
    def __repr__(self) -> str:
        return f"form_index(form_index={self.form_index!r}, status={self.status!r})"