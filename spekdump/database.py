# -*- coding=UTF-8 -*-


#app
import config


class SpekDumpDAO(object):
    collection = config._get_database()
    db = collection # alias

    def get_all_documents(self):
        return self.db.find({})

    def _make_filter(self, filters=[]):
        """
        Creates a dictionary to filter in MongoDB sintaxe's find
        """
        dict_filter = {}

        if isinstance(filters, list) and filters:
            for elem in filters:
                if not isinstance(elem, tuple):
                    # TODO: to create Exceptions
                    raise TypeError(u'All elements must be tuple')
        else:
            raise TypeError(u'Filters must be a list')


        dict_filter['$and'] = []
        for f, t in filters:
            dict_filter['$and'].append({f: t})
            dict_filter['$and'].append({f: {'$exists': True}})

        return dict_filter

    def _clean_filter(self, filters, cursor, mode=0):
        """
        DEPRECATED: Because _make_filter now is  using '$and'

        The MongoDB returns queries from fields non-existent with query
        db.find({'NON-existent-field': None}). It'll return the documents
        where the field 'NON-existent-field' is None (or null like MongoDB)
        or the field NOT IS IN document. Because is need a workaround
        (for warnings).

        Args:
            filter: a dict possibly returned by _make_filter
            cursor: a cursor of a query
            mode:
                0 (warn) -> only report with output messages with warnings
                1 (strict) -> purges documents without the field
                2 (warn and strict) -> report and purge
        """
        documents = []
        warning_message = "\nWarning: The field {field} is not exists in the " \
                    "doc:\n {document}"

        for doc in cursor:
            for f, t in filters.items():
                if t is None:
                    # checking if field is contained...
                    if f not in doc:
                        if mode == 0:
                            print warning_message.format(field=f, document=doc)
                        if mode == 1:
                            continue # skip|purge or not put in array
                        if mode == 2:
                            print warning_message.format(field=f, document=doc)
                            continue # skip|purge

                    documents.append(doc)

        return documents

    def filter(self, filters=[], mode=0):
        """
        Makes a filter with base field:term

        Args:
            filters: a list of tuples with the pair (field, term). e.g:
                [('field1', 'termX'), ('field2', 'termY')]
            mode:
                0 (warn) -> only report with output messages with warnings
                1 (strict) -> purges documents without the field
                2 (warn and strict) -> report and purge

        Returns:
            a list of MongoDB's documents
        """
        dict_filter = self._make_filter(filters)
        docs = self.db.find(dict_filter)

        return docs

    def count_by(self, filters=[]):
        """

        Args:
           filters: a list of tuples with the pair (field, term). e.g:
                [('field1', 'termX'), ('field2', 'termY')]
        """
        docs_list = self.filter(filters, mode=1) # count only strict matched
        counted = len(docs_list)

        return counted