from app.model.team import TeamModel
from app.repository.base import BaseRepository


class _TeamRepository(BaseRepository):
    def get_by_id(self, session, team_id):
        return self._query(session).filter(self.model.id == team_id).one_or_none()

    def get_by_name(self, session, team_name):
        return (
            self._query(session).filter(self.model.team_name == team_name).one_or_none()
        )


TeamRepository = _TeamRepository(model=TeamModel)
