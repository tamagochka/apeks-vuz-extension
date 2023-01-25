from sqlalchemy import create_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from app.db.models import UserRoles, User
from config import FlaskConfig

engine = create_engine(FlaskConfig.SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


tables = {
    UserRoles: {
        FlaskConfig.ROLE_ADMIN: 'Администратор',
        FlaskConfig.ROLE_METOD: 'Методист',
        FlaskConfig.ROLE_BIBL: 'Библиотека',
        FlaskConfig.ROLE_USER: 'Пользователь',
    }
}

for table in tables:
    for slug, name in tables[table].items():
        session.add(table(slug=slug, name=name))
        session.commit()

for record in tables[UserRoles]:
    new_user = User(username=record)
    new_user.role = session.execute(
        select(UserRoles).where(UserRoles.slug == record)
    ).scalar_one()
    new_user.set_password(record)
    session.add(new_user)
    session.commit()