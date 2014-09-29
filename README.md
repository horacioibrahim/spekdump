SPEKDUMPS
==========
It's a lib to handling the spekx CSV files. We suppress the 
letter 'x' because the 'X' presuppose power. This not real in the Spekx :(
 

Quick Install
-----------
```
pip install git+https://github.com/horacioibrahim/spekdump.git
```

Requirements
------------
It's required that you have exported the files CSV from SPEKX in a
directory (or workdir). No stress with order, if exists duplicate ticket
in distinct files, etc. You ONLY need to export the field 'ACIONAMENTO'
from SPEKX in all files (CSV).


Quick Usage
-----------
To register all documents in database:

```
from spekdump import spekdumps

dumps = spekdumps.DocumentSpekDump()
workdir = "/ABSOLUTE/PATH/FOR/CSV_FILES"
documents = dumps.register_tickets(workdir)

```

If you want to handling lines from CSV files. You can doing working with
dictionary objects

```
from spekdump import spekdumps

dumps = spekdumps.DocumentSpekDump()
workdir = "/ABSOLUTE/PATH/FOR/CSV_FILES"
documents = dumps.get_tickets(workdir)

# Prints each ticket as dict
for doc in documents:
    print doc.document

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
import plotly.plotly as py

from spekdump import database

dic_date_numbers = database.SpekDumpDAO().count_document_by_date
data = [{'y': dic_date_numbers.values(), 'x': dic_date_numbers.keys()}]
unique_url = py.plot(data, filenam='daily')

```
