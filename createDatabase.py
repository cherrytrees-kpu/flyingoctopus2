import sqlite3
import anno

connection = sqlite3.connect('family_M.db')
cursor = connection.cursor()

#Create tables
cursor.execute('DROP TABLE IF EXISTS GeneralInformation')
cursor.execute('CREATE TABLE GeneralInformation (HGVS TEXT, RSID TEXT, VarType TEXT, MostSevereConsequence TEXT, gnomADE FLOAT, gnomADG FLOAT, Gene TEXT, EnsemblGene TEXT, CADDRaw FLOAT, CADDPhred FLOAT)')
#cursor.execute('CREATE TABLE InSilicoModel (HGVS TEXT, Gene TEXT, UniprotACC TEXT, UniprotEntry TEXT, ProveanPred TEXT, ProveanScore FLOAT, ProveanRank FLOAT, Polyphen2Pred TEXT, Polyphen2Score FLOAT, Polyphen2Rank FLOAT, SIFTPred TEXT, SiftScore FLOAT, SiftRank FLOAT, CADDRaw FLOAT, CADDPhred FLOAT)')

#Write to table
#cursor.execute('INSERT INTO GeneralInformation(HGVS, RSID, VarType, gnomADE, gnomADG, Gene, EnsemblGene) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Bob', 'is', 'your', 0.00, 0.00, 'Uncle', 'Boy'))

connection.commit()

connection.close()
