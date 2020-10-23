import pandas as pd
import sqlite3

DB_PATH = '../database/sstubs.db'

connection = sqlite3.connect(DB_PATH)
c = connection.cursor()

# Create table
c.execute('DROP TABLE IF EXISTS sstubs')
c.execute('CREATE TABLE sstubs (parent char(40), child char(40), type varchar(64), file varchar)')
c.execute('DROP TABLE IF EXISTS sstubs_large')
c.execute('CREATE TABLE sstubs_large (parent char(40), child char(40), type varchar(64), file varchar)')
c.execute('DROP TABLE IF EXISTS bugs')
c.execute('CREATE TABLE bugs (parent char(40), child char(40), file varchar)')
c.execute('DROP TABLE IF EXISTS bugs_large')
c.execute('CREATE TABLE bugs_large (parent char(40), child char(40), file varchar)')

# Insert into sstubs
df = pd.read_json('../dataset/sstubs')
values = []
for _, row in df.iterrows():
    value = (row.fixCommitParentSHA1, row.fixCommitSHA1, row.bugType, row.bugFilePath)
    values.append(value)

c.executemany('INSERT INTO sstubs VALUES (?,?,?,?)', values)
connection.commit()
print(f'{len(values)} entries added to DB SStuBs')

# Insert into sstubs_large
df = pd.read_json('../dataset/sstubsLarge')
values = []
for _, row in df.iterrows():
    value = (row.fixCommitParentSHA1, row.fixCommitSHA1, row.bugType, row.bugFilePath)
    values.append(value)

c.executemany('INSERT INTO sstubs_large VALUES (?,?,?,?)', values)
connection.commit()
print(f'{len(values)} entries added to DB SStuBs Large')

# Insert into bugs
df = pd.read_json('../dataset/bugs')
values = []
for _, row in df.iterrows():
    value = (row.fixCommitParentSHA1, row.fixCommitSHA1, row.bugFilePath)
    values.append(value)

c.executemany('INSERT INTO bugs VALUES (?,?,?)', values)
connection.commit()
print(f'{len(values)} entries added to DB Bugs')

# Insert into bugs_large
df = pd.read_json('../dataset/bugsLarge')
values = []
for _, row in df.iterrows():
    value = (row.fixCommitParentSHA1, row.fixCommitSHA1, row.bugFilePath)
    values.append(value)

c.executemany('INSERT INTO bugs_large VALUES (?,?,?)', values)
connection.commit()
print(f'{len(values)} entries added to DB Bugs Large')

connection.close()
