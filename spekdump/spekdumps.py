# -*- coding=UTF-8 -*-
#
# The scope this module is to make upload of data from SPEK's CSV files
# to MongoDB. The method save() must be the unique point of contact of the
# module with a database. All others operations with database must be performed
# by database.py module.
#

import csv
import re
import os
from os.path import join
from datetime import datetime

# app
import database

class CSVMongo(object):


    def __init__(self, date_format=None, **kwargs):
        self.date_format = date_format

    def _has_pattern_date(self, value,
             dt_pattern=r"[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}"):
        """
        Checks if a string value match with a pattern.
        The pattern is custom by user. Or return None if no match occurred.

        :param dt_pattern: a raw string of regex to make the match with date
        format.
        :param value: is a string, provably with date formatted that will be
        translate to the type date/datetime if matched.
        """
        re_date_format = re.compile(dt_pattern) # date pattern
        res = re_date_format.match(value)
        if res:
            return self._convert_str_to_datetime(value)

    def _convert_str_to_datetime(self, value, str_format='%Y-%m-%d %H:%M:%S'):
        """
        Convert datetime string in a datetime object.

        :param value: string value will be converted
        :str_format: the date/datetime format wanted.
        """
        date_formated = datetime.strptime(value, str_format)
        return date_formated


class DocumentSpekDump(CSVMongo):

    def __init__(self, date_format=None, **kwargs):
        super(DocumentSpekDump, self).__init__(self, **kwargs)
        self.document = kwargs
        self.date_format = r"[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}"
        
    def _get_csv_spekx(self, workdir, file_pattern=r".csv",
                       ignorecase=True):
        """ Analysis all files in workdir that match to file_pattern and returns
        a list with the results.

        :param workdir: absolute path to directory that contains the files. If
        None current directory is workdir
        :param file_pattern: a regex pattern that combines with all files
        :param ignorecase: if True file_pattern can be CSV or csv, etc.
        """
        if workdir is None:
            workdir = os.path.curdir
        else:
            assert os.path.isabs(workdir)

        csvfiles = []
        rex = re.compile(file_pattern)
        walkobj = os.walk(workdir).next()
        dirname = walkobj[0]
        all_files = walkobj[2]

        for f in all_files:
            if ignorecase:
                resx = rex.match(f, re.IGNORECASE)
            else:
                resx = rex.match(f)
            
            if resx:
                absfile = join(dirname, f)
                csvfiles.append(absfile)
        
        return csvfiles         

    def get_tickets(self, workdir):
        """
        Returns a dict containing all tickets/lines inserted in a csvfiles.
        """
        csvfiles = self._get_csv_spekx(workdir,
                      file_pattern=r"[\d]+_[\d]+_[\d]+_[\d]+_[\d]+_[\d]+_CSV")
        documents = []

        for csvfile in csvfiles:
            with open(csvfile) as csvcurrent:
                dict_reader = csv.DictReader(csvcurrent)
                for document in dict_reader:
                    # Fixes encoding...
                    for k, v in document.items():
                        if v is not None:
                            v = v.decode('iso-8859-1').encode('utf-8')
                        date_checked = self._has_pattern_date(v) # pattern default
                        if date_checked:
                            document[k] = date_checked

                    spk = DocumentSpekDump(**document)
                    documents.append(spk)

        return documents

    def register_tickets(self, workdir, id_field="ACIONAMENTO"):
        """
        Save all tickets (or lines) returned by get_tickets in database.
        This is a shorthand to avoid a for loop as:

        dumps = instance.get_tickets()
        for doc in dumps:
            doc.save()

        Now. You can to call:
        dumps.register_tickets()

        Args:
            workdir: directory that contains all CSV files (in level)
            id_field: field to index, e.g.: in mailchimp it'is email,
            a system of tickets, the ticket id can be a id

        Returns:
            quantity of documents saved

        """
        # TODO: support multiple indexes

        documents = self.get_tickets(workdir)
        count = 0

        for doc in documents:
            doc.save(id_field)
            count += 1

        return count


    def save(self, id_field):
        """
        Uses update if not exist insert rather update the objetc
        """
        if self.document:
            return database.SpekDumpDAO().save(self.document, id_field)
        else:
            raise TypeError("save() require that instance has the document "
                            "attribute loaded.")

