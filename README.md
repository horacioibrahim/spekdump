SPEKDUMPS
==========
It's a lib to handling the spekx CSV files. We suppress the 
letter 'x' because the 'X' presuppose power. This not real in the Spekx :(
 

Quick Usage
-----------
```
import spekdumps

dumps = spekdumps.DocumentSpekDump()
workdir = "/ABSOLUTE/PATH/FOR/CSV_FILES"
documents = dumps.get_tickets(workdir) # All documents from all *.csv in workdir

for doc in documents:
    doc.save() # if exist is updated or it's created a new document

```
