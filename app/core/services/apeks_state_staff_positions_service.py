from dataclasses import dataclass

from config import ApeksConfig
from .base_apeks_api_service import ApeksApiDbService
from ..repository.apeks_api_repository import ApeksApiRepository


@dataclass
class ApeksStateStaffPositionsService(ApeksApiDbService):
    """
    Класс для CRUD операций модели StateStaff.

    Пример данных модели:
    {'id': '71',
     'name': 'администратор',
     'name_short': 'администратор',
     'category_id': '1',
     'sort': '40',
     'min_hours_all': None,
     'max_hours_all': None,
     'min_hours_classroom': None,
     'max_hours_classroom': None}
    """

    pass


def get_apeks_state_staff_positions_service(
    table: str = ApeksConfig.STATE_STAFF_POSITIONS_TABLE,
    repository: ApeksApiRepository = ApeksApiRepository(),
    token: str = ApeksConfig.TOKEN,
) -> ApeksStateStaffPositionsService:
    """Возвращает CRUD сервис для таблицы state_staff_positions."""
    return ApeksStateStaffPositionsService(
        table=table, repository=repository, token=token
    )