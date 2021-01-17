import sqlite3
import pandas as pd

pd.set_option('precision', 3)

cursor = sqlite3.connect('../database/sstubs.db').cursor()
data = list(cursor.execute('SELECT * FROM sstubs_large'))
columns = cursor.execute(
    "SELECT name FROM PRAGMA_TABLE_INFO('sstubs_large')"
)
sstubs_df = pd.DataFrame(data=data, columns=[col for col, in columns])

bugTypeMap = {
    'CHANGE_MODIFIER': 'Change Modifier',
    'CHANGE_NUMERAL': 'Change Numeric Literal',
    'DIFFERENT_METHOD_SAME_ARGS': 'Wrong Function Name',
    'CHANGE_IDENTIFIER': 'Change Identifier Used',

    'CHANGE_CALLER_IN_FUNCTION_CALL': 'Same Function Change Caller',
    'LESS_SPECIFIC_IF': 'Less Specific If',
    'MORE_SPECIFIC_IF': 'More Specific If',
    'CHANGE_OPERAND': 'Change Operand',

    'SWAP_ARGUMENTS': 'Same Function Swap Args',
    'OVERLOAD_METHOD_MORE_ARGS': 'Same Function More Args',
    'OVERLOAD_METHOD_DELETED_ARGS': 'Same Function Less Args',
    'CHANGE_OPERATOR': 'Change Binary Operator',

    'CHANGE_UNARY_OPERATOR': 'Change Unary Operator',
    'SWAP_BOOLEAN_LITERAL': 'Change Boolean Literal',
    'ADD_THROWS_EXCEPTION': 'Missing Throws Exception',
    'DELETE_THROWS_EXCEPTION': 'Delete Throws Exception',
}

sstubs_df['type'] = sstubs_df['type'].map(bugTypeMap)

col_names = {
    'parent': 'Parent',
    'child': 'Child',
    'type': 'Bug Type',
    'distance': 'Depth',
    'refix': 'Refix',
}

sstubs_df = sstubs_df.merge(
    right=pd.read_csv('../database/sstubs_large_distances.csv'),
    left_on='child',
    right_on='commit'
).rename(columns=col_names)

stat_df = sstubs_df[col_names.values()]
fix_df = stat_df[stat_df.Refix == True]
