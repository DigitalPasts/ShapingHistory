"""How large a change could each turning-point test have detected? (power check for script 100)

A test that finds no change after a conquest only means something if it could have found one. For every event, with the
same sample, strata, damage control and scaling as script 100 (site x document type strata), we draw the permutation
null of the 12 stratum-weighted median shifts. Because a median moves exactly with a constant added to every tablet,
adding a true change of size m (robust SD units) in direction u to the tablets after the event moves the observed shift
vector by m*u. Power at size m is then the share of null shift vectors s for which ||s + m*u|| exceeds the 95th
percentile of the null norm. Directions: the observed direction of the Sulgi 39 change (the foundation of Puzris-Dagan)
and 200 random directions (averaged). Reported: power at the size of the observed reform and foundation shifts, and the
smallest change detectable with 80% power (minimum detectable shift, MDS).
Outputs: WORK/turning/tp_power{SUF}.csv"""
from _paths import WORK
import os, numpy as np, pandas as pd, warnings; warnings.filterwarnings('ignore')
R = WORK; O = f'{R}/turning'; rng = np.random.default_rng(105)
NPERM = int(os.environ.get('SH_NPERM', 1000))
REP = os.environ.get('SH_REP', 'vae'); SUF = '' if REP == 'vae' else '_dinov2'
d = pd.read_parquet(f'{R}/master_tablets.parquet').merge(
    pd.read_csv(f'{O}/tablet_dates_consolidated.csv')[['id', 'king_final', 'bce', 'year_known']], on='id', how='left')
if REP == 'dinov2':
    P = pd.read_parquet(f'{R}/dinov2_pca.parquet')[['id'] + [f'D{i}' for i in range(1, 13)]]
    d = d.drop(columns=[f'X{i}' for i in range(1, 13)]).merge(P.rename(columns={f'D{i}': f'X{i}' for i in range(1, 13)}), on='id', how='inner')
ARCH = ['Administrative', 'Letter', 'Legal', 'Business / Contracts']
d = d[d.genre.isin(ARCH) & d.photo_hw.between(1/3, 3)].copy()
VAE = [f'X{i}' for i in range(1, 13)]

from _reigns import in_window
def win(yr):
    """before = the 20 years up to the event (a reign that ends in the event year counts as before), after = the event
    year and the 19 after it; a tablet dated only by reign enters a side only if its whole reign lies in it (_reigns.py)"""
    yk = lambda g: g.year_known.fillna(False).astype(bool)
    return (lambda g: in_window(g, yr, yr + 20) & ~(yk(g) & g.bce.eq(yr))), (lambda g: in_window(g, yr - 19, yr))
EV = [('Urukagina', ['ED IIIb'], lambda g: g.king_final.isin(['Lugalanda', 'Enentarzi']),
       lambda g: g.king_final.isin(['Urukagina_e', 'Urukagina_l', 'Urukagina'])),
      ('Sulgi 21', ['Ur III'], *win(2072)), ('Sulgi 39', ['Ur III'], *win(2054)), ('Ibbi-Suen 3', ['Ur III'], *win(2024)),
      ('Hammurabi 1763', ['Old Babylonian'], *win(1763)), ('Samsu-iluna 1739', ['Old Babylonian'], *win(1739)),
      ('Sargon II > Sennacherib', ['Neo-Assyrian'], lambda g: g.king_final.eq('Sargon2'), lambda g: g.king_final.eq('Sennacherib')),
      ('Esarhaddon 681', ['Neo-Assyrian'], *win(681)), ('Cyrus 539', ['Neo-Babylonian', 'Achaemenid'], *win(539)),
      ('Darius I 521', ['Neo-Babylonian', 'Achaemenid'], *win(521))]

def mad(x): m = np.nanmedian(x, 0, keepdims=True); return np.nanmedian(np.abs(x - m), 0)

def prep(h):
    X = h[VAE].to_numpy(float).copy(); dam = h.damage.to_numpy(float); ok = ~np.isnan(dam)
    A = np.c_[np.ones(ok.sum()), dam[ok], dam[ok] ** 2]
    for j in range(12):
        b, *_ = np.linalg.lstsq(A, X[ok, j], rcond=None); X[ok, j] = X[ok, j] - A @ b + np.median(X[ok, j])
    s = 1.4826 * mad(X); return X / np.where(s > 0, s, 1)

def shift(X, post, idx):
    num = np.zeros(12); den = 0.0
    for ix in idx:
        p = post[ix]; nb, na = (p == 0).sum(), (p == 1).sum(); w = nb * na / (nb + na); den += w
        num += w * (np.median(X[ix][p == 1], 0) - np.median(X[ix][p == 0], 0))
    return num / den

samples = {}
for name, pers, fb, fa in EV:
    g = d[d.period.isin(pers)]; h = pd.concat([g[fb(g)].assign(post=0), g[fa(g)].assign(post=1)])
    h['st'] = h.site.astype(str) + '|' + h.genre.astype(str)
    ok = h.groupby('st').post.agg(lambda v: v.sum() >= 3 and (1 - v).sum() >= 3); h = h[h.st.isin(ok[ok].index)]
    X = prep(h); post = h.post.to_numpy(); idx = [np.where(h.st.to_numpy() == k)[0] for k in h.st.unique()]
    obs = shift(X, post, idx); null = np.zeros((NPERM, 12))
    for b in range(NPERM):
        pp = post.copy()
        for ix in idx: pp[ix] = rng.permutation(pp[ix])
        null[b] = shift(X, pp, idx)
    samples[name] = (obs, null, int((1 - post).sum()), int(post.sum()), len(idx))
    print(name, 'done', flush=True)

u39 = samples['Sulgi 39'][0] / np.linalg.norm(samples['Sulgi 39'][0])
U = rng.normal(size=(200, 12)); U /= np.linalg.norm(U, axis=1, keepdims=True)
ref = {k: float(np.linalg.norm(samples[k][0]) - np.median(np.linalg.norm(samples[k][1], axis=1))) for k in ['Urukagina', 'Sulgi 21', 'Sulgi 39', 'Ibbi-Suen 3']}
M = np.round(np.arange(0.05, 2.01, 0.05), 2); rows = []
for name, (obs, null, nb, na, ns) in samples.items():
    crit = np.quantile(np.linalg.norm(null, axis=1), 0.95)
    def power(m, u): return float(np.mean(np.linalg.norm(null + m * u, axis=1) > crit))
    pw39 = np.array([power(m, u39) for m in M]); pwr = np.array([np.mean([power(m, u) for u in U[:50]]) for m in M])
    mds39 = M[np.argmax(pw39 >= 0.8)] if (pw39 >= 0.8).any() else np.nan
    mdsr = M[np.argmax(pwr >= 0.8)] if (pwr >= 0.8).any() else np.nan
    r = dict(event=name, n_before=nb, n_after=na, strata=ns, null_95=round(crit, 3), observed=round(float(np.linalg.norm(obs)), 3),
             mds_sulgi39_direction=mds39, mds_random_direction=mdsr)
    for k, v in ref.items(): r[f'power_at_{k.replace(" ", "")}_excess'] = round(power(max(v, 0), u39), 2)
    rows.append(r)
T = pd.DataFrame(rows); T.to_csv(f'{O}/tp_power{SUF}.csv', index=False)
print('reference excess shifts:', {k: round(v, 3) for k, v in ref.items()})
print(T.to_string())

# Pooled test by type of event: are conquests and successions together consistent with no change, and could the pooled
# test have seen a change of the reform size at each of them? Statistic = sum over events of the standardised excess
# (observed norm - null median) / null SD; null = sums of independent permutation draws.
GROUPS = {'reform and foundation': ['Urukagina', 'Sulgi 21', 'Sulgi 39'], 'collapse': ['Ibbi-Suen 3', 'Samsu-iluna 1739'],
          'conquest and succession': ['Hammurabi 1763', 'Sargon II > Sennacherib', 'Esarhaddon 681', 'Cyrus 539', 'Darius I 521'],
          'conquest': ['Hammurabi 1763', 'Cyrus 539'], 'succession': ['Sargon II > Sennacherib', 'Esarhaddon 681', 'Darius I 521']}
prow = []
for gname, evs in GROUPS.items():
    nn = {k: np.linalg.norm(samples[k][1], axis=1) for k in evs}
    zs = lambda k, v: (v - np.median(nn[k])) / nn[k].std()
    obs = sum(zs(k, np.linalg.norm(samples[k][0])) for k in evs)
    nullsum = sum(zs(k, nn[k][rng.permutation(NPERM)]) for k in evs); crit = np.quantile(nullsum, 0.95)
    def ppower(m, u=u39):
        tot = sum(zs(k, np.linalg.norm(samples[k][1][rng.permutation(NPERM)] + m * u, axis=1)) for k in evs)
        return float(np.mean(tot > crit))
    pw = {m: ppower(m) for m in M}
    mds = min([m for m, v in pw.items() if v >= 0.8], default=np.nan)
    prow.append(dict(group=gname, events='; '.join(evs), pooled_z=round(obs, 2), p=(np.sum(nullsum >= obs) + 1) / (NPERM + 1),
                     power_at_sulgi39_size=round(ppower(ref['Sulgi 39']), 2), power_at_ibbisuen3_size=round(ppower(ref['Ibbi-Suen 3']), 2),
                     mds_each_event=mds))
PT = pd.DataFrame(prow); PT.to_csv(f'{O}/tp_power_pooled{SUF}.csv', index=False); print(PT.to_string())
