import pandas as pd
import re
import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()

def get(i):
    soup = BeautifulSoup(http.urlopen('POST', 'http://www.nysed.gov/COMS/OP001/OPSCR2',
        headers={'Content-Type':'text/html'},
        body='profcd=60&plicno=%d' % (i)).data, 'html')
    content = list(filter(None,
                          map(str.strip,
                              re.split(r'(\n|\r|\xa0)',
                                       soup.select('#content_column')[0].text))))
    for l in content:
        ll = list(map(str.strip, l.split(':')))
        if len(ll) == 2 and ll[1] and not ll[0].startswith('-'):
            yield(ll)
    yield(['NYS Physician License Number', i])

df = pd.read_csv('Cardiac_Surgery_by_Surgeon__Beginning_2008.csv')
L = []
for i in set(df['NYS Physician License Number']):
    d=dict(get(i))
    if not d:
        print(i)
    L.append(d)
df2 = pd.DataFrame().from_records(L)#.dropna(subset=['License No'])
df2['City'] = df2['Address'].apply(lambda s: s.split('  ')[0].strip() if type(s)==str else '')
df2['State'] = df2['Address'].apply(lambda s: s.split('  ')[-1].strip() if type(s)==str else '')
df2 = df2.drop(['Address', 'Additional Qualification'], axis=1)
df2.to_csv('results.csv', index=False)
