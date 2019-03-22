# screening_db_with_bs

script that takes molecular formulas as input and screens the NIST [1] database (using beatiful soup librarie from python) for heat of formations (returning heat of fomrations, type of experiment, literature and the InChI of the molecule)

using as
```
python3 hof.py mol_formulas.txt
```

where mol_fornulas.txt the is the file containing the molecular formulas (one per line).


_______________________________________________________________
[1] https://webbook.nist.gov/
