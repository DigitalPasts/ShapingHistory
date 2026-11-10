"""Blind change-point scan (plan of 9 Nov 2026, step 3): where does tablet form change when the test is not told the dates
of political events? Guards against choosing the events that work.

For every year y in the densely dated stretches (Ur III 2105-2010, Old Babylonian 1825-1705, Neo-Assyrian 720-625,
Neo-Babylonian and Achaemenid 620-485 BCE) the archival tablets of the 10 years before y are compared with those of the 10
years from y, inside strata of the same site and document type present on both sides (>= 3 tablets each), after
removing the damage trend; statistic = Euclidean norm of the stratum-weighted median shifts of the 12 VAE dimensions in
robust SD units (as in script 100), against 300 permutations of the before/after labels inside strata. A year is a
change point when its permutation p survives Benjamini-Hochberg (q < 0.05) within its stretch and it is a local maximum of
the excess shift within +/- 5 years. The same scan runs inside every site x document-type group with >= 200 dated
tablets. Change points are then compared with the event list fixed before the test (script 100 plus the other candidate
events of 98k), counting a match within +/- 3 years.
Outputs: WORK/turning/cp_scan_years.csv, cp_scan_points.csv, cp_scan_groups.csv."""
from _paths import WORK
from _reigns import in_window   # a tablet dated only by reign enters a window only if its whole reign fits
import os, numpy as np, pandas as pd, warnings; warnings.filterwarnings('ignore')
R = WORK; O = f'{R}/turning'; rng = np.random.default_rng(101)
NPERM = int(os.environ.get('SH_NPERM', 300)); W = 10
d = pd.read_parquet(f'{R}/master_tablets.parquet').merge(
    pd.read_csv(f'{O}/tablet_dates_consolidated.csv')[['id', 'bce', 'king_final', 'year_known']], on='id', how='left')
ARCH = ['Administrative', 'Letter', 'Legal', 'Business / Contracts']
d = d[d.genre.isin(ARCH) & d.photo_hw.between(1/3, 3) & d.bce.notna()].copy()
d = d[d.year_known.fillna(False).astype(bool) | d.king_final.isin(__import__('_reigns').REIGN)]
VAE = [f'X{i}' for i in range(1, 13)]
STRETCH = {'Ur III': (['Ur III'], 2105, 2010), 'Old Babylonian': (['Old Babylonian', 'Early Old Babylonian'], 1825, 1705),
           'Neo-Assyrian': (['Neo-Assyrian'], 720, 625), 'Neo-Babylonian and Achaemenid': (['Neo-Babylonian', 'Achaemenid'], 620, 485)}
EVENTS = {2072: 'Sulgi 21 reforms', 2054: 'Sulgi 39, Puzris-Dagan', 2024: 'Ibbi-Suen 3, provinces lost', 2044: 'Amar-Suen accession',
          2035: 'Su-Suen accession', 1763: 'Hammurabi takes Larsa', 1739: 'Samsu-iluna loses the south', 1792: 'Hammurabi accession',
          1749: 'Samsu-iluna accession', 1822: 'Rim-Sin accession', 745: 'Tiglath-pileser III reform', 722: 'Sargon II accession',
          705: 'Sennacherib accession', 681: 'Esarhaddon accession', 669: 'Assurbanipal accession', 652: 'Samas-suma-ukin revolt',
          626: 'Nabopolassar independence', 605: 'Nebuchadnezzar II accession', 556: 'Nabonidus accession', 539: 'Cyrus takes Babylon',
          530: 'Cambyses accession', 521: 'Darius I reorganisation', 484: 'Xerxes, Babylonian revolts'}

def mad(x): m = np.nanmedian(x, 0); return np.nanmedian(np.abs(x - m), 0)

def prep(g):
    X = g[VAE].to_numpy(float).copy(); dam = g.damage.fillna(g.damage.median()).to_numpy(float)
    A = np.c_[np.ones(len(dam)), dam, dam ** 2]
    for j in range(X.shape[1]):
        b, *_ = np.linalg.lstsq(A, X[:, j], rcond=None); X[:, j] -= A @ b
    s = 1.4826 * mad(X); return X / np.where(s > 0, s, 1)

def shift(X, post, idx):
    num = np.zeros(X.shape[1]); den = 0.0
    for ix in idx:
        p = post[ix]; nb, na = (p == 0).sum(), (p == 1).sum(); w = nb * na / (nb + na); den += w
        num += w * (np.median(X[ix][p == 1], 0) - np.median(X[ix][p == 0], 0))
    return np.sqrt(np.sum((num / den) ** 2))

def scan(g, y0, y1, keys):
    Xall = prep(g); g = g.assign(_r=np.arange(len(g))); rows = []
    for y in range(y0, y1 - 1, -1):
        b = g[in_window(g, y, y + W) & ~(g.year_known.fillna(False).astype(bool) & g.bce.eq(y))].assign(post=0); a = g[in_window(g, y - W + 1, y)].assign(post=1)
        h = pd.concat([b, a])
        if len(b) < 30 or len(a) < 30: continue
        h['st'] = h[keys].astype(str).agg('|'.join, axis=1)
        ok = h.groupby('st').post.agg(lambda v: v.sum() >= 3 and (1 - v).sum() >= 3); h = h[h.st.isin(ok[ok].index)]
        if h.post.sum() < 30 or (1 - h.post).sum() < 30: continue
        X = Xall[h._r.values]; post = h.post.values; idx = [np.where(h.st.values == k)[0] for k in h.st.unique()]
        obs = shift(X, post, idx); null = []
        for _ in range(NPERM):
            pp = post.copy()
            for ix in idx: pp[ix] = rng.permutation(pp[ix])
            null.append(shift(X, pp, idx))
        null = np.array(null)
        rows.append(dict(year=y, n_before=int((1 - post).sum()), n_after=int(post.sum()), strata=len(idx), shift=obs,
                         excess=obs - np.median(null), z=(obs - null.mean()) / null.std(), p=(np.sum(null >= obs) + 1) / (NPERM + 1)))
    return pd.DataFrame(rows)

def bh(p):
    p = np.asarray(p, float); o = np.argsort(p); m = len(p); q = np.empty(m)
    q[o] = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]; return np.minimum(q, 1)

def points(S):
    if S.empty: return S
    S = S.sort_values('year', ascending=False).reset_index(drop=True); S['q'] = bh(S.p)
    loc = [S.excess.iloc[i] == S.excess[(S.year >= S.year.iloc[i] - 5) & (S.year <= S.year.iloc[i] + 5)].max() for i in range(len(S))]
    S['change_point'] = (S.q < 0.05) & np.array(loc)
    S['near_event'] = S.year.map(lambda y: '; '.join(f'{e} ({k})' for k, e in EVENTS.items() if abs(k - y) <= 3))
    return S

Y, G = [], []
for name, (pers, y0, y1) in STRETCH.items():
    g = d[d.period.isin(pers)]
    S = points(scan(g, y0, y1, ['site', 'genre'])); S.insert(0, 'stretch', name); Y.append(S)
    cp = S[S.change_point]; print(name, 'years scanned', len(S), '| change points', cp.year.tolist(), '| near events', cp.near_event.tolist())
    for (site, gen), gg in g.groupby(['site', 'genre']):
        if len(gg) < 200: continue
        S2 = points(scan(gg, y0, y1, ['site']));
        if S2.empty: continue
        S2.insert(0, 'group', f'{site} {gen}'); S2.insert(0, 'stretch', name); G.append(S2)
        print('   ', site, gen, 'change points', S2[S2.change_point].year.tolist())
Y = pd.concat(Y); Y.to_csv(f'{O}/cp_scan_years.csv', index=False)
G = pd.concat(G) if G else pd.DataFrame(); G.to_csv(f'{O}/cp_scan_groups.csv', index=False)
P = pd.concat([Y[Y.change_point].assign(group='all sites and types'), G[G.change_point]] if len(G) else [Y[Y.change_point]])
P.to_csv(f'{O}/cp_scan_points.csv', index=False)
# how often would a change point fall within 3 years of a listed event by chance? share of scanned years near an event
for name in STRETCH:
    yrs = Y[Y.stretch == name].year; near = yrs.map(lambda y: any(abs(k - y) <= 3 for k in EVENTS)).mean()
    cp = P[P.stretch == name]; hit = (cp.near_event != '').mean() if len(cp) else np.nan
    print(f'{name}: {len(cp)} change points, {hit:.0%} near an event; chance {near:.0%}' if len(cp) else f'{name}: no change points; chance {near:.0%}')
