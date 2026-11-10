"""Flatten the Nabucco Omeka XML export (github.com/DigitalPasts/nabucco, nabucco-xml/, accessed 2021-03-22) to one CSV row per item."""
import os, glob, xml.etree.ElementTree as ET, pandas as pd
D = os.path.expanduser('~/deeplomatics-repro/nabucco')
ns = {'o': 'http://omeka.org/schemas/omeka-xml/v5'}
rows = []
for fn in sorted(glob.glob(f'{D}/repo/nabucco-xml/items_*.xml')):
    for it in ET.parse(fn).getroot().findall('o:item', ns):
        r = {'itemId': it.get('itemId'), 'itemType': (it.findtext('o:itemType/o:name', namespaces=ns) or '')}
        for el in it.iter('{%s}element' % ns['o']):
            name = el.findtext('o:name', namespaces=ns)
            vals = [t.text or '' for t in el.findall('o:elementTextContainer/o:elementText/o:text', ns)]
            if name: r[name] = ' || '.join(v.strip() for v in vals) if name not in r else r[name] + ' || ' + ' || '.join(vals)
        rows.append(r)
df = pd.DataFrame(rows); df.to_csv(f'{D}/nabucco_items.csv', index=False)
print(df.shape); print(df.itemType.value_counts().to_string())
print(df.notna().mean().sort_values(ascending=False).round(2).to_string())
