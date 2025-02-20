from app.model.employee import EmployeeModel
from app.repository.base import BaseRepository
import logging


class _EmployeeRepository(BaseRepository):
    def get_by_id(self, session, employee_id):
        return self._query(session).filter(self.model.id == employee_id).one_or_none()

    def get_by_ids(self, session, employee_ids):
        return self._query(session).filter(self.model.id.in_(employee_ids)).all()

    def get_by_name(self, session, first_name, last_name):
        # What if there are some employees with the same name, only differentiated by their team ?
        # TODO: find a way to deal with this case
        return (
            self._query(session)
            .filter(
                self.model.first_name == first_name, self.model.last_name == last_name
            )
            .first()
        )

    def get_by_team(self, session, team_id):
        return self._query(session).filter(self.model.team_id == team_id).all()

    def create(self, session, obj_in):
        logging.debug(f"Creating new employee with data {obj_in=}")
        new_employee = self.model(**obj_in)
        # new_employee = self.model(first_name = obj_in['first_name'], last_name = obj_in['last_name'], team_id = obj_in['team_id'])
        logging.debug(f"Creating new employee {new_employee=}")

        session.add(new_employee)
        session.commit()
        session.refresh(new_employee)
        return new_employee


EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
