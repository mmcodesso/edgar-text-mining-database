from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class form_index(Base):
    __tablename__ = "index"

    form_index = Column(String, primary_key=True)
    status = Column(Integer)
    
    def __repr__(self) -> str:
        return f"form_index(form_index={self.form_index!r}, status={self.status!r})"

class form(Base):
    __tablename__ = "form"

    form_id = Column(String,primary_key=True)
    form_type = Column(String)
    company_name = Column(String)
    cik = Column(String)
    date_filed = Column(String)
    file_name =  Column(String)
    form_index = Column(String)
    index_url = Column(String)
    index_htm = Column(String)
    status = Column(Integer)

    def __repr__(self) -> str:
        return f"form(form_id={self.form_id!r},form_type={self.form_type!r},company_name={self.company_name!r},cik={self.cik!r},date_filed={self.date_filed!r},file_name={self.file_name!r},form_index={self.form_index!r},index_url={self.index_url!r},index_htm={self.index_htm!r},status={self.status!r})"
    