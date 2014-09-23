SPEKDUMPS
==========
It's a lib to handling the spekx CSV files. We suppress the 
letter 'x' because the 'X' presuppose power. This not real in the Spekx :(
 

Quick Install
-----------
```
pip install git+https://github.com/horacioibrahim/spekdump.git
```


Quick Usage
-----------
```
from spekdump import spekdumps

dumps = spekdumps.DocumentSpekDump()
workdir = "/ABSOLUTE/PATH/FOR/CSV_FILES"
documents = dumps.get_tickets(workdir) # All documents from all *.csv in workdir

# Saves all documents in database ...
for doc in documents:
    doc.save() # if exist is updated or it's created a new document

# or

# Prints each ticket as dict
for doc in documents:
    doc.document 

```

Advanced Usage
----------------
You can to use any lib to plot a graph. We're showing how make it 
with https://plot.ly/ with a Demo Account. 

*Step one:*
To install the lib plotly
```
pip install plotly

See > https://plot.ly/python/getting-started/
```

*Step two: Initialization and test*
```
python -c "import plotly; plotly.tools.set_credentials_file(username='DemoAccount', api_key='lr1c37zw81')"
```

*Step three*
We're to generate the numbers of demands by day 
```
from spekdump import database

dic_date_numbers = database.SpekDumpDAO().count_document_by_date
data = [{'y': dic_date_numbers.values(), 'x': dic_date_numbers.keys()}]
unique_url = py.plot(data, filenam='daily')

```
