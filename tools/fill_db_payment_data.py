import os
import sys

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

sys.path.append('.')

from app.common.func.app_core import read_json_file, make_slug
from app.db.payment_models import (
    PaymentRate,
    PaymentRateValues,
    PaymentAddons,
    PaymentAddonsValues,
    PaymentMatchRateAddon,
    PaymentSingleAddon,
    PaymentMatchRateSingle,
    PaymentIncrease,
    PaymentMatchRateIncrease,
    PaymentPensionDutyCoefficient,
    PaymentGlobalCoefficient, PaymentDocuments,
)
from config import FlaskConfig, BASEDIR


engine = create_engine(FlaskConfig.SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

FILE_DIR = os.path.join(BASEDIR, "tools", "data_payment")



# Заполняем данные о нормативных документах
documents_data = read_json_file(os.path.join(FILE_DIR, "documents_data.json"))
for data in documents_data:
    session.add(
        PaymentDocuments(
            name=documents_data[data].get("name"),
        )
    )
session.commit()


# Заполняем данные об окладах
rate_data = read_json_file(os.path.join(FILE_DIR, "rate_data.json"))
for rate in rate_data:
    session.add(
        PaymentRate(
            slug=make_slug(rate_data[rate].get("name"), prefix="rate_"),
            name=rate_data[rate].get("name"),
            payment_name=rate_data[rate].get("payment_name"),
            salary=rate_data[rate].get("salary"),
            pension=rate_data[rate].get("pension"),
        )
    )
    session.flush()
    rate_id = session.execute(
        select(PaymentRate.id).where(PaymentRate.name == rate_data[rate].get("name"))
    ).scalar_one()
    for record in rate_data[rate].get("data"):
        for name, value in rate_data[rate]["data"][record].get("values").items():
            session.add(
                PaymentRateValues(
                    name=name,
                    value=value,
                    rate_id=rate_id,
                    description=rate_data[rate]["data"][record].get("description"),
                    document_id=rate_data[rate]["data"][record].get('document_id'),
                )
            )
    session.commit()


# Заполняем данные о надбавках
addons_data = read_json_file(os.path.join(FILE_DIR, "addons_data.json"))
for data in addons_data:
    session.add(
        PaymentAddons(
            slug=make_slug(addons_data[data].get("name"), prefix="addon_"),
            name=addons_data[data].get("name"),
            payment_name=addons_data[data].get("payment_name"),
            salary=addons_data[data].get("salary"),
            pension=addons_data[data].get("pension"),
        )
    )
    session.flush()
    addon_id = session.execute(
        select(PaymentAddons.id).where(
            PaymentAddons.name == addons_data[data].get("name")
        )
    ).scalar_one()
    for name, value in addons_data[data].get("data").items():
        session.add(
            PaymentAddonsValues(
                name=name,
                value=value,
                description=addons_data[data].get("description"),
                addon_id=addon_id,
                document_id=addons_data[data].get("document_id"),
            )
        )
    for rate_name in addons_data[data].get("apply_to"):
        rate_id = session.execute(
            select(PaymentRate.id).where(PaymentRate.name == rate_name)
        ).scalar_one()
        session.add(
            PaymentMatchRateAddon(
                rate_id=rate_id,
                addon_id=addon_id,
            )
        )
    session.commit()


# Заполняем данные о фиксированных надбавках
single_addons_data = read_json_file(os.path.join(FILE_DIR, "single_addons_data.json"))
for data in single_addons_data:
    session.add(
        PaymentSingleAddon(
            slug=make_slug(single_addons_data[data].get("name"), prefix="single_"),
            name=single_addons_data[data].get("name"),
            payment_name=single_addons_data[data].get("payment_name"),
            value=single_addons_data[data].get("value"),
            description=single_addons_data[data].get("description"),
            document_id=single_addons_data[data].get("document_id"),
            salary=single_addons_data[data].get("salary"),
            pension=single_addons_data[data].get("pension"),
            default_state=single_addons_data[data].get("default_state"),
        )
    )
    session.flush()
    single_addon_id = session.execute(
        select(PaymentSingleAddon.id).where(
            PaymentSingleAddon.name == single_addons_data[data].get("name")
        )
    ).scalar_one()
    for rate_name in single_addons_data[data].get("apply_to"):
        rate_id = session.execute(
            select(PaymentRate.id).where(PaymentRate.name == rate_name)
        ).scalar_one()
        session.add(
            PaymentMatchRateSingle(
                rate_id=rate_id,
                single_addon_id=single_addon_id,
            )
        )
    session.commit()


# Заполняем данные об индексациях
increase_data = read_json_file(os.path.join(FILE_DIR, "increase_data.json"))
for data in increase_data:
    session.add(
        PaymentIncrease(
            name=increase_data[data].get("name"),
            value=increase_data[data].get("value"),
            document_id=increase_data[data].get("document_id"),
        )
    )
    session.flush()
    payment_increase_id = session.execute(
        select(PaymentIncrease.id).where(
            PaymentIncrease.name == increase_data[data].get("name")
        )
    ).scalar_one()
    for rate_name in increase_data[data].get("apply_to"):
        rate_id = session.execute(
            select(PaymentRate.id).where(PaymentRate.name == rate_name)
        ).scalar_one()
        session.add(
            PaymentMatchRateIncrease(
                rate_id=rate_id,
                payment_increase_id=payment_increase_id,
            )
        )
    session.commit()


# Заполняем данные о коэффициенте выслуги для расчета пенсии
pension_duty_data = read_json_file(os.path.join(FILE_DIR, "pension_duty_data.json"))
for data in pension_duty_data:
    session.add(
        PaymentPensionDutyCoefficient(
            name=pension_duty_data[data].get("name"),
            value=pension_duty_data[data].get("value"),
            document_id=pension_duty_data[data].get("document_id"),
        )
    )
    session.commit()


# Заполняем данные о глобальных коэффициентах, изменяющих общую выплату
global_coefficient_data = read_json_file(
    os.path.join(FILE_DIR, "global_coefficient_data.json")
)
for data in global_coefficient_data:
    session.add(
        PaymentGlobalCoefficient(
            slug=make_slug(global_coefficient_data[data].get("name"), prefix="coeff_"),
            name=global_coefficient_data[data].get("name"),
            value=global_coefficient_data[data].get("value"),
            payment_name=global_coefficient_data[data].get("payment_name"),
            description=global_coefficient_data[data].get("description"),
            document_id=global_coefficient_data[data].get("document_id"),
            salary=global_coefficient_data[data].get("salary"),
            pension=global_coefficient_data[data].get("pension"),
        )
    )
    session.commit()
