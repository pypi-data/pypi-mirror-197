import random

from supextend.utils.superset import color_generator
from supextend.resources.internal.superset_batch_cleaner import TagCleaner
from supextend.core import MetastoreConnManager
from supextend.models.tags import Tag
from supextend.loggers.config import LoggingConfig


class TagIntern(TagCleaner):

    @staticmethod
    def create_intern_resource(**kwargs):
        """ Add deleted tags to the metastore """

        title = kwargs.get('title')
        color = kwargs.get('color', random.choice(color_generator()))
        tag = Tag(
            title=title,
            color=color
        )
        with MetastoreConnManager() as session:
            session.add(tag)
            session.commit()
            LoggingConfig.logger.success(
                    f"Successfully added the tag: {title}.")
            return tag

    def update_intern_resource(self, pk, **kwargs):
        """ Updates tags in the metastore """

        t = self.get_intern_resource(pk)
        t.title = kwargs.get('title', t.title)
        with MetastoreConnManager() as session:
            session.add(t)
            session.commit()
            LoggingConfig.logger.success(f"Updated the tag: {t.title}.")
            return t

    @staticmethod
    def list_intern_resource():
        return Tag.query.all()

    def delete_intern_resource(self, pk):
        tag = self.get_intern_resource(pk)
        username = tag.title
        with MetastoreConnManager() as session:
            session.delete(tag)
            session.commit()
            LoggingConfig.logger.success(f"Removed the tag: {username}.")

    @staticmethod
    def get_intern_resource(pk):
        return Tag.query.get(pk)
