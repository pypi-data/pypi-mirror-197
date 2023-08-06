from __future__ import annotations

import uuid
from typing import List, Dict, Iterable

import os
from os.path import splitext
import logging
import importlib
import drb.utils.plugins
from jsonschema.exceptions import ValidationError

from .topic_dao import DrbTopicDao
from .yaml_dao import YamlDao
from drb.topics.topic import DrbTopic
from drb.exceptions.core import DrbException, DaoException


logger = logging.getLogger('DrbTopic')


def _load_all_drb_topic_dao() -> Dict[uuid.UUID, DrbTopicDao]:
    """
    Loads topics defined in the Python context
    """
    entry_point_group = 'drb.topic'
    result = {}

    for ep in drb.utils.plugins.get_entry_points(entry_point_group):
        # load module
        try:
            module = importlib.import_module(ep.value)
        except ModuleNotFoundError as ex:
            logger.warning(f'Invalid entry point {ep.name}: {ex.msg}')
            continue

        try:
            path = os.path.join(module.__path__[0], 'cortex.yml')
            dao = DaoFactory().create(path)
            topics = dao.read_all()
            for topic in topics:
                if topic.id in result:
                    logger.warning(
                        f'Topic definition conflict: id ({topic.id}) defined '
                        f'in {result[topic.id]} and {dao}')
                else:
                    result[topic.id] = dao

        except (FileNotFoundError, ValidationError) as ex:
            logger.warning(
                f'Invalid topic description(s) from {ep.name}: {ex.msg}')
            continue
    return result


class DaoFactory:
    """
    The DaoFactory class instantiates a DAO.
    The factory shall be aware of the supported/known dao(s) to instantiate
    and build a relation between the physical data and its virtual topic
    representation.
    """
    __instance = None
    __known_dao = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DaoFactory, cls).__new__(cls)
            from .xml_dao import XmlDao
            cls.__known_dao = {'.yml': YamlDao, '.owl': XmlDao}
        return cls.__instance

    def create(self, path: str) -> DrbTopicDao:
        ext = splitext(path)[1]
        try:
            dao = self.__known_dao[ext]
            return dao(path)
        except KeyError:
            raise DaoException(f'Unknown format by DAO: {path}')


class ManagerDao:
    """
    Manages loading and retrieving of topics defined in the Python
    context.
    """
    __instance = None
    __added_dao = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ManagerDao, cls).__new__(cls)
            cls.__topic_dao = _load_all_drb_topic_dao()

        return cls.__instance

    def get_all_drb_topics(self) -> Iterable[DrbTopic]:
        """
        Returns all loaded topics.
        Returns:
            Iterable: An iterable containing all loaded topics.
        """
        topics = []

        for identifier in self.__topic_dao.keys():
            topic = self.__topic_dao[identifier].read(identifier)
            topics.append(topic)

        return topics

    def get_drb_topic(self, identifier: uuid.UUID) -> DrbTopic:
        """
        Retrieves a topic.
        Parameters:
            identifier (UUID): topic UUID
        Returns:
            DrbTopic: the topic identified by the given UUID.
        """
        if identifier in self.__topic_dao.keys():
            dao = self.__topic_dao[identifier]
            return dao.read(identifier)

        raise DrbException('No DrbTopic found')

    def is_subclass(self, actual: DrbTopic, expected: DrbTopic) -> bool:
        """
        Check if a topic is subclass of another.

        Parameters:
            actual(DrbTopic): topic to check
            expected(DrbTopic): expected parent topic
        Returns:
            bool: ``True`` if the given actual topic is a child of the
                  expected one, otherwise ```False``
        """

        if actual.id == expected.id:
            return True

        if actual.subClassOf is None:
            return False

        for parent_id in actual.subClassOf:

            return self.is_subclass(self.get_drb_topic(parent_id),
                                    expected)

    def get_parents(self, topic: DrbTopic) -> List[DrbTopic]:

        parents = []

        for parent in topic.subClassOf:

            if parent in self.__topic_dao.keys():
                dao = self.__topic_dao[topic.id]
                parents.append(dao.read(parent))

        return parents

    def get_children(self, topic: DrbTopic) -> List[DrbTopic]:

        children = []

        for identifier in self.__topic_dao.keys():
            child = self.__topic_dao[identifier].read(identifier)
            if child.subClassOf is not None and topic.id in child.subClassOf:
                children.append(child)

        return children

    def save(self, topic: DrbTopic, dao: DrbTopicDao) -> DrbTopic:
        """
        Saves a topic.
        Parameters:
            topic (DrbTopic): topic to save
            dao (DrbTopicDao): dao to be used for topic save
        Returns:
            DrbTopic: the topic saved into source
        """

        self.__topic_dao[topic.id] = dao
        if dao not in self.__added_dao:
            self.__added_dao.append(dao)
        try:
            return dao.update(topic)
        except DrbException:
            return dao.create(topic)

    def delete(self, identifier: uuid.UUID):
        """
        Deletes a topic.
        Parameters:
            identifier (UUID): identifier of topic to delete
        """

        if identifier in self.__topic_dao.keys():
            dao = self.__topic_dao[identifier]
            if dao in self.__added_dao:
                dao.delete(identifier)
                self.__topic_dao.pop(identifier)
            else:
                raise DrbException('DrbTopic cannot be deleted from '
                                   'protected environment')

        else:
            raise DrbException('No DrbTopic found')

    def add_dao(self, path: str) -> DrbTopicDao:
        """
        Adds a new DAO to the list of available dao(s).
        Parameters:
            path (str): the path to the dao to add
        Returns:
            DrbTopicDao: dao can be used to read/write topic(s)
                """

        dao = DaoFactory().create(path)
        self.__added_dao.append(dao)
        topics = dao.read_all()
        for topic in topics:
            self.__topic_dao[topic.id] = dao

        return dao
