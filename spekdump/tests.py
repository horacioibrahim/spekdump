# -*- coding: UTF-8 -*-
""" Test the spekdump package"""

import unittest
import os
import tempfile
import pymongo
from datetime import datetime
from time import sleep

# APP
from spekdump import spekdumps, database, config


def get_client(*args, **kwargs):
    host = os.environ.get("MONGO_IP", "localhost")
    port = os.environ.get("MONGO_PORT", 27017)
    return pymongo.MongoClient(host, port, *args, **kwargs)

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.spekdb = database.SpekDumpDAO()
        self.spekdb.db = {'database':'test', 'collection': 'spekdumps'}
        doc1 = {'_id': 1, 'b': 2, 'c': 3}
        doc2 = {'_id': 4, 'b': 5, 'c': 6}
        doc3 = {'_id': 7, 'b': 8}
        self.spekdb.save(doc1)
        self.spekdb.save(doc2)
        self.spekdb.save(doc3)

    def tearDown(self):
        self.spekdb.db.drop()

    def test_db_setter_exception(self):
        spekdb = database.SpekDumpDAO()
        self.assertRaises(TypeError, spekdb.db, 'csvfields')

    def test_init_args(self):
        spekdb = database.SpekDumpDAO()
        spekdb.db = {'database':'test', 'collection': 'spekdumps_init'}
        doc = {'_id': 1, 'b': 2, 'c': 7}
        success = spekdb.save(doc)
        self.assertEqual(success, 0)
        spekdb.db.drop()

    def test_init_default_without_args(self):
        spekdb = database.SpekDumpDAO()
        self.assertEqual(spekdb.db.database.name, config.DATABASE)
        self.assertEqual(spekdb.db.name, config.COLLECTION)

    def test_get_all_documents(self):
        docs = self.spekdb.get_all_documents()
        self.assertEqual(3, docs.count())

    def test__make_filter(self):
        filters = {'name': 'Horacio'}
        obj = database.SpekDumpDAO()
        res = obj._make_filter(filters=filters.items())
        self.assertIsInstance(res, dict)
        self.assertIsInstance(res['$and'], list)
        self.assertEqual(res['$and'][0]['name'], 'Horacio')

    def test__clean_filter_mode_0(self):
        """
        Test if filter return all documents only warning messages
        """
        filters = {'c': None} # get when c field is null
        docs = self.spekdb.get_all_documents()
        result = self.spekdb._clean_filter(filters, docs, mode=0)
        self.assertIsInstance(result, list)
        self.assertEqual(3, len(result))

    def test__clean_filter_mode_1(self):
        """Test if one document will be purged because the field c is None
        """
        filters = {'c': None} # get when c field is null
        docs = self.spekdb.get_all_documents()
        result = self.spekdb._clean_filter(filters, docs, mode=1)
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))

    def test__clean_filter_mode_2(self):
        """Test if one document will be purged because the field c is None
        and print messages of warnings
        """
        filters = {'c': None} # get when c field is null
        docs = self.spekdb.get_all_documents()
        result = self.spekdb._clean_filter(filters, docs, mode=2)
        self.assertIsInstance(result, list)
        self.assertEqual(2, len(result))

    def test_filter_to_none(self):
        """Test if return zero document or a document with null value
        in database
        """
        filters = [('c', None)] # get when c field is null
        docs = self.spekdb.filter(filters)
        self.assertEqual(0, docs.count())
        doc4 = {'_id': 11, 'b': 5, 'c': None}
        self.spekdb.save(doc4)
        docs = self.spekdb.filter(filters)
        self.assertEqual(1, docs.count())

    def test_count_by(self):
        """Test if return one document"""
        filters = [('_id', 1)]
        self.assertEqual(1, self.spekdb.count_by(filters))

    def test_save(self):
        """Saves an existent or non-existent document"""
        new_doc = {'_id': 'test_save_w_update', 'b': 10, 'c': 100}
        obj = database.SpekDumpDAO()
        obj.save(new_doc)
        one = obj.db.find_one({'_id': 'test_save_w_update'})
        self.assertEqual(new_doc['_id'], one['_id'])
        new_doc['b'] = 200
        res = obj.save(new_doc)
        self.assertEqual(0, res)














class TestSpekDump(unittest.TestCase):

    def setUp(self):
        self.mongo = get_client()
        self.db = self.mongo.test.csvfields
        self.instance = spekdumps.DocumentSpekDump()

        # CSV for tests
        self.tempdir = tempfile.mkdtemp()
        self.f1 = os.path.join(self.tempdir, '2014_01_10_10_22_20_CSV')
        self.f2 = os.path.join(self.tempdir, '2014_02_10_10_22_20_CSV')
        self.ff1 = open(self.f1, "w+")
        self.ff2 = open(self.f2, "w+")

        # writing in csv
        self.ff1.write('Nome, Lugar, Objeto')
        self.ff1.write('\n')
        self.ff1.write('Canpbell, Cappadocia, Chair')
        self.ff1.write('\n')
        self.ff1.write('Cameron Dias, California, Cone')
        self.ff1.write('\n')
        self.ff1.close()

        self.ff2.write('Nome, Lugar, Objeto')
        self.ff2.write('\n')
        self.ff2.write('Michael Jordan, Maryland, Mocock')
        self.ff2.write('\n')
        self.ff2.close()

    def tearDown(self):
        os.remove(self.f1)
        os.remove(self.f2)
        os.rmdir(self.tempdir)
        self.db.drop()

    def test__has_pattern_date(self):
        """
        Test uf returns None or datetime values if string is a datetime
        """
        fake_date = "2014-09-10"
        str_date = "2014-09-10 10:22:20"
        self.assertIsInstance(self.instance._has_pattern_date(str_date),
                              datetime)
        self.assertNotIsInstance(self.instance._has_pattern_date(fake_date),
                                 datetime)
        self.assertIsNone(self.instance._has_pattern_date(fake_date))

    def test__get_csv_spekx(self):
        """
        Test the returns of a list of CSV files that match pattern with
        exported by Spekx in a Workdir
        """
        tempdir = tempfile.mkdtemp()
        f1 = os.path.join(tempdir, '2014_09_10_10_22_20_CSV')
        f2 = os.path.join(tempdir, '2014_10_10_10_22_20_CSV')
        f3 = os.path.join(tempdir, '2014_09_10_10_22_20')
        ff1 = open(f1, "w+")
        ff2 = open(f2, "w+")
        ff3 = open(f3, "w+")
        container = self.instance._get_csv_spekx(tempdir)

        # remove temp dir
        os.remove(f1)
        os.remove(f2)
        os.remove(f3)
        os.rmdir(tempdir)

        # Tests
        self.assertIsInstance(container, list)
        self.assertEqual(2, len(container))
        abs_path = os.path.join(tempdir, '2014_09_10_10_22_20_CSV')
        self.assertIn(abs_path, container)


    def test_get_tickets(self):
        """
        Test if return DocumentSpekDump, if raise error with inconsistent
        columns.
        """
        tempdir = tempfile.mkdtemp()
        f1 = os.path.join(tempdir, '2014_09_10_10_22_20_CSV')
        f2 = os.path.join(tempdir, '2014_10_10_10_22_20_CSV')
        ff1 = open(f1, "w+")
        ff2 = open(f2, "w+")

        # writing in csv
        ff1.write('Nome, Lugar, Objeto')
        ff1.write('\n')
        ff1.write('Canpbell, Cappadocia, Chair')
        ff1.write('\n')
        ff1.write('Cameron Dias, California, Cone')
        ff1.write('\n')
        ff1.close()

        ff2.write('Nome, Lugar, Objeto')
        ff2.write('\n')
        ff2.write('Michael Jordan, Maryland, Mocock')
        ff2.write('\n')
        ff2.close()

        # tests...and clean temp files
        result = self.instance.get_tickets(tempdir)
        os.remove(f1)
        os.remove(f2)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0].document, dict)

        for elem in result:
            self.assertIsInstance(elem, spekdumps.DocumentSpekDump)

        # fields inconsistent
        f3 = os.path.join(tempdir, '2014_11_10_10_22_20_CSV')
        ff3 = open(f3, "w+")
        ff3.write('Nome, Lugar, Objeto')
        ff3.write('\n')
        ff3.write('Michael Jordan, Maryland')
        ff3.write('\n')
        ff3.close()
        self.assertRaises(TypeError,self.instance.get_tickets, tempdir)
        # Removing more files
        os.remove(f3)
        os.rmdir(tempdir)

    def test_register_tickets(self):
        """
        Test if returns the quantity documents saved
        """
        self.assertIsInstance(self.instance.register_tickets(self.tempdir,
                                                            "Nome"), int)

    def test_save(self):
        docs = self.instance.get_tickets(self.tempdir)
        res = docs[0].save(id_field="Nome")
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()





