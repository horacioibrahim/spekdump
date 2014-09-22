# -*- coding=UTF-8 -*-

import csv
import re
import os
from os.path import join

# app
import config


class DocumentSpekDump(object):

    def __init__(self, **kwargs):
        self.document = kwargs

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
                for line in lines:
                    document = {}
                    # Mouting the fields with fisrt line
                    if count_first_line == 0:
                        count_first_line += 1
                        fields = []
                        for field in line:
                            fields.append(field)
                        #lines.next()
                        continue
                    else:
                        values = []
                        for value in line:
                            value = value.decode('iso-8859-1').encode('utf-8')
                            values.append(value)

                    if len(fields) == len(values):
                        for field in fields:
                            pos = fields.index(field)
                            document[field] = values[pos]
                    else:
                        raise TypeError("The lines are incosistent in csvfile\n")
                    
                    doc_spk_dump = DocumentSpekDump(**document)
                    documents.append(doc_spk_dump)

        return documents        

    def save(self):
        """
        Uses update if not exist insert rather update the objetc
        """
        collection = config.get_database()
        ticket_id = self.document['ACIONAMENTO']
        try:
            collection.update({'_id': ticket_id}, {'$set': self.document}, upsert=True)
        except:
            raise # Fix it

    


