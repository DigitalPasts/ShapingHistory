"""Map figures (ShG, 10 Nov 2026: 'the argument should be visualized geographically as well as shape based').
Site coordinates: Pleiades (dump of 10 Nov 2026) where the site is located there, otherwise standard published coordinates
of the tell (flagged 'approx.'); unlocated or unprovenanced sites (Garsana, Irisagrig, Mugdan, Pi-Kasi, 'unknown') are left off.
Basemap: Natural Earth 1:50m land, coastline and rivers.
Panels, one per millennium: circles = sites, area ~ photographed tablets of that millennium; colour = share of the site's
test-set tablets whose period the masked ResNet50 recognises (resnet_masked_test_predictions.csv); grey lines join every site
outside the Babylonian-Assyrian heartland to the heartland site whose archival tablets of the same millennium are closest in
shape (median of the 12 VAE dimensions, robust-scaled; L1 distance).
Outputs: FIGS/FigMap_millennia.(png|pdf), WORK/geo/site_coordinates.csv, WORK/geo/map_links.csv."""
from _paths import WORK, FIGS, SHARED
import json, os, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
G = f'{WORK}/geo'; os.makedirs(FIGS, exist_ok=True)
C = [  # site, lat, lon, source
 ('Nineveh', 36.3595, 43.1521, 'Pleiades'), ('Nippur', 32.1268, 45.2306, 'Pleiades'), ('Umma', 31.6370, 45.8910, 'approx. (Tell Jokha)'),
 ('Puzriš-Dagan', 32.0800, 45.2700, 'approx. (Drehem)'), ('Girsu', 31.5604, 46.1776, 'Pleiades'), ('Ur', 30.9622, 46.1030, 'approx. (Tell al-Muqayyar)'),
 ('Kanesh', 38.8500, 35.6360, 'approx. (Kültepe)'), ('Uruk', 31.3234, 45.6391, 'Pleiades'), ('Assur', 35.4590, 43.2620, 'Pleiades'),
 ('Adab', 31.9400, 45.6200, 'approx. (Bismaya)'), ('Gasur/Nuzi', 35.3708, 44.2548, 'Pleiades'), ('Larsa', 31.2832, 45.8525, 'Pleiades'),
 ('Nerebtum', 33.3300, 44.6200, 'approx. (Ishchali)'), ('Sippar-Yahrurum', 33.0570, 44.2520, 'approx. (Abu Habbah)'), ('Kish', 32.5461, 44.5932, 'Pleiades'),
 ('Kalhu', 36.0980, 43.3290, 'approx. (Nimrud)'), ('Tuttul', 35.9581, 39.0472, 'Pleiades'), ('Babylon', 32.5360, 44.4210, 'approx.'),
 ('Pārśa', 29.9352, 52.8904, 'Pleiades'), ('Ebla', 35.7980, 36.7980, 'approx. (Tell Mardikh)'), ('Akhetaten', 27.6441, 30.8982, 'Pleiades'),
 ('Borsippa', 32.3924, 44.3434, 'Pleiades'), ('Kar-Tukulti-Ninurta', 35.4850, 43.2560, 'approx. (Tulul al-Aqar)'), ('Ešnunna', 33.4845, 44.7281, 'Pleiades'),
 ('Alalakh', 36.2380, 36.3830, 'approx. (Tell Atchana)'), ('Ḫattusa', 40.0190, 34.6150, 'Pleiades'), ('Shuruppak', 31.7760, 45.5090, 'approx. (Fara)'),
 ('Isin', 31.8853, 45.2693, 'Pleiades'), ('Šibaniba', 36.4200, 43.3300, 'approx. (Tell Billa)'), ('Tutub', 33.3540, 44.5560, 'approx. (Khafajah)'),
 ('Dilbat', 32.2958, 44.4669, 'Pleiades'), ('Zabalam', 31.7400, 45.8700, 'approx. (Tell Ibzeikh)'), ('Susa', 32.1899, 48.2535, 'Pleiades'),
 ('Anšan', 30.0032, 52.4104, 'Pleiades')]
S = pd.DataFrame(C, columns=['site', 'lat', 'lon', 'source']); S.to_csv(f'{G}/site_coordinates.csv', index=False)
S.loc[S.site == 'Akhetaten', ['lat', 'lon']] = [29.0, 34.1]   # drawn at the map edge, labelled 'Akhetaten (Egypt)'
HEART = {'Nineveh', 'Nippur', 'Umma', 'Puzriš-Dagan', 'Girsu', 'Ur', 'Uruk', 'Assur', 'Adab', 'Larsa', 'Nerebtum', 'Sippar-Yahrurum', 'Kish', 'Kalhu',
         'Babylon', 'Borsippa', 'Kar-Tukulti-Ninurta', 'Ešnunna', 'Shuruppak', 'Isin', 'Šibaniba', 'Tutub', 'Dilbat', 'Zabalam'}
MIL = {'Uruk IV': 4, 'Uruk III': 4, 'Proto-Elamite': 4, 'ED I-II': 3, 'ED IIIa': 3, 'ED IIIb': 3, 'Ebla': 3, 'Old Akkadian': 3, 'Lagash II': 3, 'Ur III': 3,
       'Early Old Babylonian': 2, 'Old Babylonian': 2, 'Old Assyrian': 2, 'Middle Babylonian': 2, 'Middle Assyrian': 2, 'Middle Hittite': 2, 'Hittite': 2,
       'Middle Elamite': 2, 'Neo-Assyrian': 1, 'Neo-Babylonian': 1, 'Achaemenid': 1, 'Hellenistic': 1}
d = pd.read_parquet(f'{WORK}/master_tablets.parquet'); d['mil'] = d.period.map(MIL)
P = pd.read_csv(f'{SHARED}/resnet_masked_test_predictions.csv') if os.path.exists(f'{SHARED}/resnet_masked_test_predictions.csv') else \
    pd.read_csv('/mnt/project-files/ShapingHistory/repro/resnet_masked_test_predictions.csv')
P = P.rename(columns={'CDLI_id': 'id'})[['id', 'y', 'pred']].merge(d[['id', 'site', 'mil']], on='id')
acc = P.assign(ok=P.y == P.pred).groupby(['site', 'mil']).agg(acc=('ok', 'mean'), ntest=('ok', 'size')).reset_index()
cnt = d.groupby(['site', 'mil']).size().rename('n').reset_index().merge(acc, on=['site', 'mil'], how='left').merge(S, on='site')
VAE = [f'X{i}' for i in range(1, 13)]
a = d[d.genre.isin(['Administrative', 'Letter', 'Legal', 'Business / Contracts'])].dropna(subset=VAE)
Z = (a[VAE] - a[VAE].median()) / (1.4826 * (a[VAE] - a[VAE].median()).abs().median())
a = a[['site', 'mil']].join(Z)
med = a.groupby(['site', 'mil']).filter(lambda g: len(g) >= 20).groupby(['site', 'mil'])[VAE].median()
links = []
for (site, mil), v in med.iterrows():
    if site in HEART or site not in set(S.site): continue
    cand = med.loc[[i for i in med.index if i[1] == mil and i[0] in HEART and i[0] in set(S.site)]]
    if cand.empty: continue
    dist = (cand - v).abs().sum(axis=1); best = dist.idxmin()
    links.append(dict(site=site, mil=mil, nearest=best[0], distance=round(dist.min(), 2), second=dist.drop(best).idxmin()[0] if len(dist) > 1 else ''))
L = pd.DataFrame(links); L.to_csv(f'{G}/map_links.csv', index=False); print(L.to_string())
land = json.load(open(f'{G}/ne_50m_land.geojson')); riv = json.load(open(f'{G}/ne_50m_rivers.geojson'))
def draw_geo(ax, gj, **kw):
    for f in gj['features']:
        g = f['geometry']; polys = g['coordinates'] if g['type'] in ('Polygon', 'MultiLineString') else ([g['coordinates']] if g['type'] == 'LineString' else [p for mp in g['coordinates'] for p in mp])
        for ring in polys:
            r = np.array(ring if g['type'] != 'Polygon' else ring)
            if r.ndim == 2 and len(r) > 1: ax.fill(r[:, 0], r[:, 1], **kw) if kw.get('fill_') else ax.plot(r[:, 0], r[:, 1], **{k: v for k, v in kw.items() if k != 'fill_'})
def base(ax):
    for f in land['features']:
        g = f['geometry']; parts = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        for poly in parts:
            r = np.array(poly[0]); ax.fill(r[:, 0], r[:, 1], color='#f3efe6', lw=0, zorder=0)
            ax.plot(r[:, 0], r[:, 1], color='#c9c2b3', lw=0.4, zorder=1)
    for f in riv['features']:
        nm = (f['properties'].get('name') or '')
        if nm not in ('Tigris', 'Euphrates', 'Nile', 'Karun', 'Diyala', 'Khabur', 'Kızılırmak', 'Zab', 'Shatt al Arab', 'Halys'): continue
        g = f['geometry']; parts = [g['coordinates']] if g['type'] == 'LineString' else g['coordinates']
        for r in parts: r = np.array(r); ax.plot(r[:, 0], r[:, 1], color='#8fb3c9', lw=0.8, zorder=1)
    ax.set_xlim(33.5, 54); ax.set_ylim(28.3, 41.5); ax.set_aspect(1 / np.cos(np.radians(34))); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color('#bbb')
cm = LinearSegmentedColormap.from_list('acc', ['#e9e4f0', '#7b5ea7', '#2d1b4e'])
SZ = lambda n: np.sqrt(n) * 3.2
LAB = {'Nineveh': (6, 4), 'Assur': (6, -9), 'Nippur': (7, 2), 'Umma': (7, -6), 'Girsu': (7, -8), 'Ur': (6, -10), 'Sippar-Yahrurum': (-8, 6), 'Uruk': (-26, -12),
       'Babylon': (-34, 4), 'Kish': (-6, 8), 'Larsa': (7, 2), 'Puzriš-Dagan': (7, 6), 'Kalhu': (7, 0), 'Nerebtum': (-48, 4), 'Kar-Tukulti-Ninurta': (6, 6)}
fig, axs = plt.subplots(1, 3, figsize=(15.5, 5.6)); plt.subplots_adjust(wspace=0.04, left=0.01, right=0.9, bottom=0.12, top=0.92)
for ax, mil, title in zip(axs, [3, 2, 1], ['Third millennium BCE', 'Second millennium BCE', 'First millennium BCE']):
    base(ax); c = cnt[cnt.mil == mil].sort_values('n', ascending=False)
    for _, l in L[L.mil == mil].iterrows():
        p1 = S.set_index('site').loc[l.site]; p2 = S.set_index('site').loc[l.nearest]
        ax.plot([p1.lon, p2.lon], [p1.lat, p2.lat], color='#555', lw=0.9, ls=(0, (3, 2)), zorder=2)
    sc = ax.scatter(c.lon, c.lat, s=SZ(c.n), c=c.acc.fillna(-1), cmap=cm, vmin=0, vmax=1, edgecolor='#333', linewidth=0.5, zorder=3)
    na = c[c.acc.isna()]; ax.scatter(na.lon, na.lat, s=SZ(na.n), color='white', edgecolor='#333', linewidth=0.5, zorder=3)
    top = set(c.head(5).site)
    for _, r in c.iterrows():
        if r.site in HEART and r.site not in top: continue
        nm = 'Akhetaten (Egypt)' if r.site == 'Akhetaten' else r.site
        ax.annotate(nm, (r.lon, r.lat), xytext=LAB.get(r.site, (6, 3)), textcoords='offset points', fontsize=7.5, zorder=4)
    ax.set_title(f'{title}: {int(c.n.sum()):,} tablets, {len(c)} sites', fontsize=10)
cax = fig.add_axes([0.915, 0.3, 0.012, 0.5]); cb = fig.colorbar(sc, cax=cax); cb.set_label('period recognised by the model (share of test tablets)', fontsize=8)
hs = [axs[0].scatter([], [], s=SZ(n_), color='white', edgecolor='#333') for n_ in [100, 1000, 10000]]
fig.legend(hs, ['100 tablets', '1,000', '10,000'], loc='lower left', bbox_to_anchor=(0.01, 0.0), ncol=3, fontsize=8, frameon=False, columnspacing=2)
fig.text(0.3, 0.035, 'Dashed line: heartland site whose archival tablets of the same millennium are nearest in shape (12 VAE dimensions). White: no test tablets.\n'
         'Coordinates from Pleiades or published tell positions; unlocated sites (Garšana, Irisagrig, Pī-Kasî) omitted. Labels: the five largest sites and all sites outside the heartland.', fontsize=7.5, color='#444')
plt.savefig(f'{FIGS}/FigMap_millennia.png', dpi=220); plt.savefig(f'{FIGS}/FigMap_millennia.pdf'); plt.close()
print('map written')
