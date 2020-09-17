import sqlite3
import anno

#Database access
connection = sqlite3.connect('family_M.db')
cursor = connection.cursor()

#Import annotations
mvi = anno.get(mviFile)
vep = anno.get(vepFile)



#Write to table
cursor.execute('INSERT INTO GeneralInformation(HGVS, RSID, VarType, gnomADE, gnomADG, Gene, EnsemblGene) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Bob', 'is', 'your', 0.00, 0.00, 'Uncle', 'Boy'))