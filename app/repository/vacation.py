from enum import Enum as enum
from app.model.vacation import VacationModel
from app.repository.base import BaseRepository
import logging


class _VacationRepository(BaseRepository):
    def create(self, session, obj_in):
        logging.debug(f"Creating new vacation with data {obj_in=}")
        new_vacation = self.model(**obj_in)
        session.add(new_vacation)
        session.commit()
        session.refresh(new_vacation)
        return new_vacation

    def update(self, session, id, data):
        logging.debug(f"Updating vacation {id!r} with {data=}")
        vacation = self.get(session=session, id=id)
        logging.debug(f"current vacation is {vacation.__dict__}")
        for var, value in data.items():
            if isinstance(value, enum):
                value = value.value
            setattr(vacation, var, value)
        logging.debug(f"modified vacation is {vacation.__dict__}")
        session.commit()
        session.refresh(vacation)
        return vacation

    def delete(self, session, id):
        logging.debug(f"Deleting vacation with {id=} ...")
        vacation = self.get(session=session, id=id)
        session.delete(vacation)
        session.commit()
        return True

    def get_by_id(self, session, vacation_id):
        return self._query(session).filter(self.model.id == vacation_id).one_or_none()

    def get_from_date_range(self, session, range_start_date, range_end_date):
        return (
            self._query(session)
            .filter(
                self.model.start_date <= range_start_date,
                self.model.end_date >= range_end_date,
            )
            .all()
        )

    def get_by_employee_id(self, session, employee_id, order_by=None):
        logging.debug(f"Getting vacations for employee_id {employee_id} ...")
        query = self._query(session).filter(self.model.employee_id == employee_id)
        logging.debug(f"Query: {query}")
        if order_by == "start_date":
            query = query.order_by(self.model.start_date)
        result = query.all()
        logging.debug(f"{result=}")
        return result


VacationRepository = _VacationRepository(model=VacationModel)
