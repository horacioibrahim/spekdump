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
import config


class DocumentSpekDump(object):

    def __init__(self, **kwargs):
        self.document = kwargs


    def _has_pattern_date(self, value):
        """ If value has your pattern as date to convert it in datetime
        """
        re_date_format = re.compile(r"[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}")
        res = re_date_format.match(value)

        if res:
            date_formated = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return date_formated
        else:
            pass
        
    def _get_csv_spekx(self, workdir):
        """ Analysis all files in workdir that match to rex and returns
        a list with the results
        
        Args:
            workdir: absolute path to directory that contains the files

        """
        if workdir is None:
            workdir = os.path.curdir
        else:
            assert os.path.isabs(workdir)

        csvfiles = []
        rex = re.compile(r"[\d]+_[\d]+_[\d]+_[\d]+_[\d]+_[\d]+_CSV")
        walkobj = os.walk(workdir).next()
        dirname = walkobj[0]
        all_files = walkobj[2]

        for f in all_files:
            resx = rex.match(f)
            
            if resx:
                absfile = join(dirname, f)
                csvfiles.append(absfile)
        
        return csvfiles         

    def get_tickets(self, workdir):
        """
        Returns a dict containing all tickets inserted in the csvfiles exported 
        from Spekx as a DocumentSpekDump's instance
        """
        csvfiles = self._get_csv_spekx(workdir)
        documents = []

        for csvfile in csvfiles:
            with open(csvfile) as csvcurrent:
                count_first_line = 0
                lines = csv.reader(csvcurrent)
                # Each line is one document
                fields = [] # fields occurs only first loop
                for line in lines:
                    document = {}
                    # Mounting the fields with first line
                    if count_first_line == 0:
                        count_first_line += 1
                        for field in line:
                            fields.append(field)
                        #lines.next()
                        continue
                    else:
                        values = []
                        for value in line:
                            value = value.decode('iso-8859-1').encode('utf-8')
                            date_checked = self._has_pattern_date(value)
                            if date_checked:
                                value = date_checked
                            values.append(value)

                    if len(fields) == len(values):
                        for field in fields:
                            pos = fields.index(field)
                            document[field] = values[pos]
                    else:
                        raise TypeError("The lines are incosistent in " \
                            "csvfile %s" % csvcurrent.name)
                    
                    doc_spk_dump = DocumentSpekDump(**document)
                    documents.append(doc_spk_dump)

        return documents

    def register_tickets(self, workdir):
        """
        Save all tickets returned by get_tickets in database. This is a
        shorthand to avoid a for loop as:

        dumps = instance.get_tickets()
        for doc in dumps:
            doc.save()

        Otherwise. You can to call:
        dumps.register_tickets()

        Args:
            workdir: directory that contains all CSV files (in level)

        Returns:
            quantity of documents saved

        """
        documents = self.get_tickets(workdir)
        count = 0

        for doc in documents:
            doc.save()
            count += 1

        return count


    def save(self):
        """
        Uses update if not exist insert rather update the objetc
        """
        collection = config._get_database()
        ticket_id = self.document['ACIONAMENTO']
        try:
            collection.update({'_id': ticket_id}, {'$set': self.document}, upsert=True)
        except:
            raise # Fix it

    


