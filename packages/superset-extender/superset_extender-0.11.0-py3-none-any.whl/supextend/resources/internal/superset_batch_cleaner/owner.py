import random

from supextend.utils.superset import color_generator
from supextend.resources.internal.superset_batch_cleaner import OwnerCleaner
from supextend.core import MetastoreConnManager
from supextend.models.owners import Owner
from supextend.initialization import bcrypt
from supextend.loggers.config import LoggingConfig


class OwnerIntern(OwnerCleaner):
    """A class to represent an Owner of a chart/dashboard."""

    @staticmethod
    def create_intern_resource(**kwargs):
        """ Add deleted owners to the metastore """

        owner = Owner(
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            username=kwargs.get('username'),
            color=kwargs.get('color', random.choice(color_generator())),
            password=bcrypt.generate_password_hash(kwargs.get('password'))
            .decode('utf-8') if kwargs.get('password', None) else None
        )
        with MetastoreConnManager() as session:
            session.add(owner)
            session.commit()
            LoggingConfig.logger.success(
                    f"Added the owner: {owner.first_name} {owner.last_name}.")
            return owner

    def update_intern_resource(self, pk, **kwargs):
        """ Updates owners in the metastore """

        o = self.get_intern_resource(pk)
        o.password = bcrypt.generate_password_hash(
                kwargs.get('password', o.password)).decode('utf-8')
        with MetastoreConnManager() as session:
            session.add(o)
            session.commit()
            LoggingConfig.logger.success(f"Updated the owner: {o.username}.")
            return o

    @staticmethod
    def list_intern_resource():
        return Owner.query.all()

    def delete_intern_resource(self, pk):
        owner = self.get_intern_resource(pk)
        username = owner.username
        with MetastoreConnManager() as session:
            session.delete(owner)
            session.commit()
            LoggingConfig.logger.success(f"Removed the owner: {username}.")

    @staticmethod
    def get_intern_resource(pk):
        return Owner.query.get(pk)
