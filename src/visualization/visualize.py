import pandas as pd
import json
from numpyencoder import NumpyEncoder
from pathlib import Path

# This script takes the final data in processed and formats it to a JSON file to use for D3 visualization

df = pd.read_csv(r"data/csv_to_json.csv")
print(df)
def get_nested_rec(key, grp):
    rec = {}
    rec['leaid'] = key[0]
    rec['lat'] = key[1]
    rec['long'] = key[2]
    rec['name'] = key[3]
    rec['city'] = key[4]
    rec['state'] = key[5]
    #print(grp)
    years = list(grp['year'].unique())
    d = []
    for i in years:
        more = grp.loc[(grp['leaid'] == key[0]) & (grp['year'] == i)]
        more = more.drop(['leaid', 'lat', 'long', 'name', 'city', 'state', 'year'], axis=1)
        more = more.to_dict(orient='records')
        d.append(more)

    #years = [str(i) for i in years]
    rec['by_year'] = dict(zip(years, d))
    print(rec)
    return rec

records = []
for key, grp in df.groupby(['leaid','lat','long','name','city','state']):
    rec = get_nested_rec(key, grp)
    records.append(rec)
print(records)


records = dict(data = records)
with open('json_file', 'w', encoding="utf-8") as file:
    json.dump(records, file, indent=4, sort_keys=True,
              separators=(', ', ': '), ensure_ascii=False,
              cls=NumpyEncoder)
#print(records)
#print(json.dumps(records, indent=4))