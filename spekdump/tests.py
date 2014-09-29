# -*- coding: UTF-8 -*-
""" Test the spekdump package"""

import unittest
import os
import tempfile
import pymongo
from datetime import datetime

# APP
from spekdump import spekdumps


def get_client(*args, **kwargs):
    host = os.environ.get("MONGO_IP", "localhost")
    port = os.environ.get("MONGO_PORT", 27017)
    return pymongo.MongoClient(host, port, *args, **kwargs)

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.mongo = get_client()
        self.db = self.mongo.test.csvfields

    def tearDown(self):
        pass


class TestSpekDump(unittest.TestCase):

    def setUp(self):
        self.mongo = get_client()
        self.db = self.mongo.test.csvfields
        self.instance = spekdumps.DocumentSpekDump()

    def tearDown(self):
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



if __name__ == "__main__":
    unittest.main()





