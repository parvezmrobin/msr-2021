import pandas as pd
import sqlite3

DB_PATH = '../database/sstubs.db'

connection = sqlite3.connect(DB_PATH)
c = connection.cursor()

# Create table
c.execute('DROP TABLE IF EXISTS sstubs')
c.execute('''CREATE TABLE sstubs (
    parent char(40),
    child char(40), 
    type varchar(64), 
    project varchar, 
    file varchar, 
    line unsigned int,
    before varchar,
    after varchar
)''')
c.execute('DROP TABLE IF EXISTS sstubs_large')
c.execute('''CREATE TABLE sstubs_large (
    parent char(40),
    child char(40), 
    type varchar(64), 
    project varchar, 
    file varchar, 
    line unsigned int,
    before varchar,
    after varchar
)''')
c.execute('DROP TABLE IF EXISTS bugs')
c.execute('''CREATE TABLE bugs (
    parent char(40), 
    child char(40), 
    project varchar, 
    file varchar, 
    line unsigned int,
    before varchar,
    after varchar
)''')
c.execute('DROP TABLE IF EXISTS bugs_large')
c.execute('''CREATE TABLE bugs_large (
    parent char(40), 
    child char(40), 
    project varchar, 
    file varchar, 
    line unsigned int,
    before varchar,
    after varchar
)''')

# Insert into sstubs
df = pd.read_json('../dataset/sstubs')
values = []
for _, row in df.iterrows():
    value = (
        row.fixCommitParentSHA1,
        row.fixCommitSHA1,
        row.bugType,
        row.projectName,
        row.bugFilePath,
        row.bugLineNum,
        row.sourceBeforeFix,
        row.sourceAfterFix,
    )
    values.append(value)

c.executemany('INSERT INTO sstubs VALUES (?,?,?,?,?,?,?,?)', values)
connection.commit()
print(f'{len(values)} entries added to table SStuBs')

# Insert into sstubs_large
df = pd.read_json('../dataset/sstubsLarge')
values = []
for _, row in df.iterrows():
    value = (
        row.fixCommitParentSHA1,
        row.fixCommitSHA1,
        row.bugType,
        row.projectName,
        row.bugFilePath,
        row.bugLineNum,
        row.sourceBeforeFix,
        row.sourceAfterFix,
    )
    values.append(value)

c.executemany('INSERT INTO sstubs_large VALUES (?,?,?,?,?,?,?,?)', values)
connection.commit()
print(f'{len(values)} entries added to table SStuBs Large')

# Insert into bugs
df = pd.read_json('../dataset/bugs')
values = []
for _, row in df.iterrows():
    value = (
        row.fixCommitParentSHA1,
        row.fixCommitSHA1,
        row.projectName,
        row.bugFilePath,
        row.bugLineNum,
        row.sourceBeforeFix,
        row.sourceAfterFix,
    )
    values.append(value)

c.executemany('INSERT INTO bugs VALUES (?,?,?,?,?,?,?)', values)
connection.commit()
print(f'{len(values)} entries added to table Bugs')

# Insert into bugs_large
df = pd.read_json('../dataset/bugsLarge')
values = []
for _, row in df.iterrows():
    value = (
        row.fixCommitParentSHA1,
        row.fixCommitSHA1,
        row.projectName,
        row.bugFilePath,
        row.bugLineNum,
        row.sourceBeforeFix,
        row.sourceAfterFix,
    )
    values.append(value)

c.executemany('INSERT INTO bugs_large VALUES (?,?,?,?,?,?,?)', values)
connection.commit()
print(f'{len(values)} entries added to table Bugs Large')

# Create indices
for table in ['bugs', 'bugs_large', 'sstubs', 'sstubs_large']:
    c.execute(f'CREATE INDEX parent_{table} ON {table}(parent)')
    c.execute(f'CREATE INDEX child_{table} ON {table}(child)')
    c.execute(f'CREATE INDEX project_{table} ON {table}(project)')
    c.execute(f'CREATE INDEX before_{table} ON {table}(before)')
    c.execute(f'CREATE INDEX after_{table} ON {table}(after)')
for table in ['sstubs', 'sstubs_large']:
    c.execute(f'CREATE INDEX type_{table} ON {table}(type)')

print('Created indices')

connection.close()
