import sqlalchemy as sa  # noqa pycharm

from kaiju_tools.rpc import AbstractRPCCompatible
from kaiju_db.services import SQLService

from .etc import Permission
from .tables import notifications

__all__ = ['NotificationService']


class NotificationService(SQLService, AbstractRPCCompatible):
    """Interface for (task) notifications."""

    service_name = 'notifications'
    table = notifications
    update_columns = {'marked'}

    def prepare_insert_data(self, data: dict):
        """Injecting an author id from user session."""
        session = self.app.get_session()
        user_id = self.get_user_id(session)
        data = {**data, 'author_id': user_id}
        return data

    def _set_user_condition(self, sql, session):
        user_id = self.get_user_id(session)
        sql = sql.where(sa.or_(self.table.c.author_id == user_id, self.table.c.user_id == user_id))
        return sql

    def _update_condition_hook(self, sql):
        """Places user condition if a user has no admin/system privileges for editing all the data."""
        session = self.app.get_session()
        if not self.has_permission(session, Permission.MODIFY_OTHERS_NOTIFICATIONS.value):
            sql = self._set_user_condition(sql, session)
        return sql

    def _delete_condition_hook(self, sql):
        return self._update_condition_hook(sql)

    def _get_condition_hook(self, sql):
        """Places user condition if a user has no admin/system privileges for viewing all the data."""
        session = self.app.get_session()
        if not self.has_permission(session, Permission.VIEW_OTHERS_NOTIFICATIONS.value):
            sql = self._set_user_condition(sql, session)
        return sql
