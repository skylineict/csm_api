from sqlmodel import SQLModel, create_engine, Session


engine = create_engine(mysql_url, echo=True)

