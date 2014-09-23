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
