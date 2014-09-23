# -*- coding=UTF-8 -*-


#app
import config

class SpekDumpDAO(object):

	collection = config._get_database()
	db = collection # alias

	def get_documents(self):
		return self.db.find({})

	@property	
	def count_document_by_date(self, field_dt='DATA_EMISSAO'):
		""" It counts how much docs by date based in field and
		return a dictionary containing {date: integer} 
		
		Args:
		    field_at: default filter date is DATA_EMISSAO

		"""
		docs = self.get_documents()
		docs_date = {}

		for d in docs:

			try:
				key = d[field_dt]
			except KeyError, e:
				raise TypeError(u'Date field is not exist!')

			if key in docs_date:
			    docs_date[key] += 1
			else:
				docs_date[key] = 1

		return docs_date





