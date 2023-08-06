import unittest
import os
import uuid
from drb.topics.topic import DrbTopic
from drb.topics.dao.xml_dao import XmlDao
from drb.exceptions.core import DrbException


class TestXmlDao(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'landsat.owl')
        cls.dao = XmlDao(path)

    def test_read(self):
        identifier = uuid.UUID('dc26dbe5-d09e-3d53-a555-802844716688')
        label = 'Landsat-8 Level-1 GeoTIFF Image'
        topic = self.dao.read(identifier)

        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(identifier, topic.id)
        self.assertEqual(label, topic.label)

    def test_find(self):
        label = 'Landsat-8 Level-1 GeoTIFF Abstract'
        topic = self.dao.find(label)

        self.assertIsNotNone(topic)
        self.assertIsInstance(topic, DrbTopic)
        self.assertEqual(label, topic.label)
        with self.assertRaises(DrbException):
            self.dao.find("None")

    def test_read_all(self):
        topics = self.dao.read_all()

        self.assertIsNotNone(topics)
        self.assertEqual(13, len(list(topics)))

    def test_create(self):
        label = 'Landsat-8 Level-1 Metadata Text File'
        topic = self.dao.find(label)

        with self.assertRaises(NotImplementedError):
            self.dao.create(topic)

    def test_update(self):
        label = 'Landsat-8 Level-1 Ground Control Points File'
        topic = self.dao.find(label)

        with self.assertRaises(NotImplementedError):
            self.dao.create(topic)

    def test_delete(self):
        identifier = uuid.UUID('cf502e4c-b410-312d-9b16-089c9f299a22')
        with self.assertRaises(NotImplementedError):
            self.dao.delete(identifier)
