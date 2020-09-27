import sqlite3
import anno

connection = sqlite3.connect('family_M.db')
cursor = connection.cursor()

#Create tables
cursor.execute('DROP TABLE IF EXISTS GeneralInformation')
cursor.execute('CREATE TABLE GeneralInformation (HGVS TEXT, RSID TEXT, VarType TEXT, MostSevereConsequence TEXT, gnomADE FLOAT, gnomADG FLOAT, Gene TEXT, EnsemblGene TEXT)')

#Write to table
#cursor.execute('INSERT INTO GeneralInformation(HGVS, RSID, VarType, gnomADE, gnomADG, Gene, EnsemblGene) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Bob', 'is', 'your', 0.00, 0.00, 'Uncle', 'Boy'))

connection.commit()

connection.close()
