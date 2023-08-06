import csv
import pathlib

import np_logging

import np_session

logger = np_logging.getLogger()

project = 'DR'

missing = {}
for session in np_session.sessions(project=project):
    D1 = session.D1
    D2 = session.D2
    
    missing_globs = [D1.globs[D1.names.index(_)] for _ in D1.missing]
    missing_globs.extend(D2.globs[D2.names.index(_)] for _ in D2.missing)
    missing_globs.extend(D2.globs_sorted_data[D2.names_sorted_data.index(_)] for _ in D2.missing_sorted_data)
    
    missing[session.id] = set(missing_globs)
    
for_csv = []
for _ in missing:
    for_csv.append(tuple([_, *missing[_]]))
        
with open(f'{project}_missing.csv', 'w') as f:
    csv.writer(f).writerows(for_csv)