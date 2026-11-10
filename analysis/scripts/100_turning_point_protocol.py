"""One protocol for the ten testable political turning points (plan of 9 Nov 2026, step 2).

Events were fixed from the literature before the test (middle chronology; testability rule of 98c/98k: >=30 dated
archival tablets on each side within 20 years at the same sites). Each event is typed by what it did to the
institutions that wrote the tablets (see the Introduction's model):
  reform      the ruler changes how the existing institutions keep records (Urukagina, Sulgi 21)
  foundation  a new central institution is created (Puzris-Dagan, Sulgi 39)
  conquest    a state takes over another state's institutions (Hammurabi 1763, Cyrus 539)
  collapse    the centre loses its provinces (Ibbi-Suen 3, Samsu-iluna 1739)
  succession  a new king or a reorganisation inside the same state (Sargon II > Sennacherib, Esarhaddon 681, Darius I 521)

Test, the same for every event:
  * archival documents only (administrative, letters, legal, contracts), photo h/w between 1/3 and 3;
  * before = the 20 years up to the event, after = the 20 years from it (by reign for Urukagina and Sargon II > Sennacherib);
  * comparisons only inside strata of the same site and the same document type present on both sides, so a change in the
    mix of sites or genres cannot pass for a change in form;
  * features: the 12 VAE dimensions, proportion (log h/w), corner fill, rectangularity, taper, side and end thickness;
  * damage control: each feature is first residualised on the damage index (linear + quadratic) in the event sample;
  * museum control: the same test with strata of site x document type x holding museum;
  * effect = weighted mean over strata of (median after - median before), in units of the pooled robust SD (1.4826 MAD),
    weights = n_before*n_after/(n_before+n_after); multivariate effect = Euclidean norm of the 12 VAE effects;
  * dispersion = weighted mean of log(MAD after / MAD before) over strata (negative = more uniform after);
  * p-values from 2,000 permutations of before/after labels inside strata; Benjamini-Hochberg q over all tests of a family.
Outputs (WORK/turning): tp_protocol_events.csv (one row per event), tp_protocol_features.csv (event x feature),
tp_protocol_counts.csv (strata counts)."""
from _paths import WORK
import os, numpy as np, pandas as pd, warnings; warnings.filterwarnings('ignore')
R = WORK; O = f'{R}/turning'; rng = np.random.default_rng(10)
NPERM = int(os.environ.get('SH_NPERM', 2000))
REP = os.environ.get('SH_REP', 'vae')   # 'vae' (main) or 'dinov2' (confirmation: first 12 DINOv2 principal components, script 103)
SUF = '' if REP == 'vae' else '_dinov2'
d = pd.read_parquet(f'{R}/master_tablets.parquet')
D = pd.read_csv(f'{O}/tablet_dates_consolidated.csv')[['id', 'king_final', 'bce', 'year_known']]
d = d.merge(D, on='id', how='left')
if REP == 'dinov2':
    P = pd.read_parquet(f'{R}/dinov2_pca.parquet')[['id'] + [f'D{i}' for i in range(1, 13)]]
    d = d.drop(columns=[f'X{i}' for i in range(1, 13)]).merge(P.rename(columns={f'D{i}': f'X{i}' for i in range(1, 13)}), on='id', how='inner')
ARCH = ['Administrative', 'Letter', 'Legal', 'Business / Contracts']
d = d[d.genre.isin(ARCH) & d.photo_hw.between(1/3, 3)].copy()
d['loghw'] = np.log(d.photo_hw)
VAE = [f'X{i}' for i in range(1, 13)]
HAND = ['loghw', 'corner_fill', 'rect', 'taper', 'thick_side', 'thick_end']
FE = VAE + HAND

from _reigns import in_window
def win(yr):
    """before = the 20 years up to the event (a reign that ends in the event year counts as before), after = the event
    year and the 19 after it; a tablet dated only by reign enters a side only if its whole reign lies in it (_reigns.py)"""
    yk = lambda g: g.year_known.fillna(False).astype(bool)
    return (lambda g: in_window(g, yr, yr + 20) & ~(yk(g) & g.bce.eq(yr))), (lambda g: in_window(g, yr - 19, yr))

EV = [  # name, short, type, periods, before, after, year
    ('Urukagina takes power in Lagas, "reforms"', 'Urukagina', 'reform', ['ED IIIb'],
     lambda g: g.king_final.isin(['Lugalanda', 'Enentarzi']), lambda g: g.king_final.isin(['Urukagina_e', 'Urukagina_l', 'Urukagina']), 2351),
    ('Sulgi 21: army, calendar and accounting reforms', 'Sulgi 21', 'reform', ['Ur III'], *win(2072), 2072),
    ('Sulgi 39: Puzris-Dagan founded', 'Sulgi 39', 'foundation', ['Ur III'], *win(2054), 2054),
    ('Ibbi-Suen 3: the provinces break away', 'Ibbi-Suen 3', 'collapse', ['Ur III'], *win(2024), 2024),
    ('Hammurabi conquers Larsa', 'Hammurabi 1763', 'conquest', ['Old Babylonian'], *win(1763), 1763),
    ('Samsu-iluna loses the south', 'Samsu-iluna 1739', 'collapse', ['Old Babylonian'], *win(1739), 1739),
    ('Sargon II to Sennacherib (by reign)', 'Sargon II > Sennacherib', 'succession', ['Neo-Assyrian'],
     lambda g: g.king_final.eq('Sargon2'), lambda g: g.king_final.eq('Sennacherib'), 705),
    ('Esarhaddon accedes after the murder of Sennacherib', 'Esarhaddon 681', 'succession', ['Neo-Assyrian'], *win(681), 681),
    ('Cyrus takes Babylon', 'Cyrus 539', 'conquest', ['Neo-Babylonian', 'Achaemenid'], *win(539), 539),
    ('Darius I reorganises the empire', 'Darius I 521', 'succession', ['Neo-Babylonian', 'Achaemenid'], *win(521), 521),
]

def mad(x, axis=0):
    m = np.nanmedian(x, axis=axis, keepdims=True)
    return np.nanmedian(np.abs(x - m), axis=axis)

def resid_damage(X, dam):
    """residualise every column on damage (1, dam, dam^2); rows with missing damage keep their value."""
    X = X.copy(); ok = ~np.isnan(dam)
    A = np.c_[np.ones(ok.sum()), dam[ok], dam[ok] ** 2]
    for j in range(X.shape[1]):
        y = X[ok, j]; k = ~np.isnan(y)
        if k.sum() < 10: continue
        b, *_ = np.linalg.lstsq(A[k], y[k], rcond=None)
        X[np.where(ok)[0][k], j] = y[k] - A[k] @ b + np.nanmedian(y)
    return X

def stats(X, post, idx):
    """weighted stratum shift and log-dispersion ratio for every column; a stratum counts for a column only where both
    sides have >= 3 measured tablets (the hand measures exist for about a quarter of the tablets)"""
    F_ = X.shape[1]; num = np.zeros(F_); dnum = np.zeros(F_); den = np.zeros(F_)
    for ix in idx:
        p = post[ix]; xb = X[ix][p == 0]; xa = X[ix][p == 1]
        nb = np.sum(~np.isnan(xb), 0); na = np.sum(~np.isnan(xa), 0); ok = (nb >= 3) & (na >= 3)
        if not ok.any(): continue
        w = np.where(ok, nb * na / np.maximum(nb + na, 1), 0.0)
        with np.errstate(all='ignore'), warnings.catch_warnings():
            warnings.simplefilter('ignore')
            diff = np.nanmedian(xa, 0) - np.nanmedian(xb, 0)
            ld = np.log(np.maximum(mad(xa), 1e-9) / np.maximum(mad(xb), 1e-9))
        num += w * np.where(ok, diff, 0); dnum += w * np.where(ok, ld, 0); den += w
    with np.errstate(all='ignore'):
        return np.where(den > 0, num / den, np.nan), np.where(den > 0, dnum / den, np.nan)

def run(h, keys, label):
    h = h.copy(); h['stratum'] = h[keys].astype(str).agg(' | '.join, axis=1)
    ok = h.groupby('stratum').post.agg(lambda v: (v.sum() >= 3) and ((1 - v).sum() >= 3))
    h = h[h.stratum.isin(ok[ok].index)]
    if h.post.sum() < 15 or (1 - h.post).sum() < 15: return None, None
    X = h[FE].to_numpy(float); X = resid_damage(X, h.damage.to_numpy(float))
    s = 1.4826 * mad(X); s[s == 0] = np.nanstd(X, 0)[s == 0]; X = X / s
    post = h.post.to_numpy(); idx = [np.where(h.stratum.to_numpy() == k)[0] for k in h.stratum.unique()]
    sh, dp = stats(X, post, idx)
    mv = np.sqrt(np.sum(sh[:12] ** 2)); mdp = dp[:12].mean()
    nsh = np.zeros((NPERM, len(FE))); ndp = np.zeros((NPERM, len(FE)))
    for b in range(NPERM):
        pp = post.copy()
        for ix in idx: pp[ix] = rng.permutation(pp[ix])
        nsh[b], ndp[b] = stats(X, pp, idx)
    nmv = np.sqrt(np.sum(nsh[:, :12] ** 2, 1)); nmdp = ndp[:, :12].mean(1)
    pf = np.where(np.isnan(sh), np.nan, (np.sum(np.abs(nsh) >= np.abs(sh), 0) + 1) / (NPERM + 1))
    pd_ = np.where(np.isnan(dp), np.nan, (np.sum(np.abs(ndp) >= np.abs(dp), 0) + 1) / (NPERM + 1))
    nmeas = [int(np.sum(~np.isnan(X[:, j]))) for j in range(X.shape[1])]
    ev = dict(control=label, n_before=int((1 - post).sum()), n_after=int(post.sum()), strata=len(idx),
              sites=h.site.nunique(), vae_shift=round(mv, 3), vae_shift_null_median=round(float(np.median(nmv)), 3),
              vae_shift_excess=round(mv - float(np.median(nmv)), 3),
              p_vae_shift=(np.sum(nmv >= mv) + 1) / (NPERM + 1), vae_disp=round(mdp, 3),
              p_vae_disp=(np.sum(np.abs(nmdp) >= abs(mdp)) + 1) / (NPERM + 1))
    ft = pd.DataFrame(dict(control=label, feature=FE, n_measured=nmeas, shift=sh.round(3), p_shift=pf, log_disp=dp.round(3), p_disp=pd_))
    return ev, ft

def bh(p):
    p = np.asarray(p, float); o = np.argsort(p); m = len(p); q = np.empty(m)
    q[o] = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
    return np.minimum(q, 1)

E, F, C = [], [], []
for name, short, typ, pers, fb, fa, yr in EV:
    g = d[d.period.isin(pers)]
    b = g[fb(g)].assign(post=0); a = g[fa(g)].assign(post=1)
    h = pd.concat([b, a])
    C.append(h.groupby(['site', 'genre', 'post']).size().rename('n').reset_index().assign(event=short))
    for keys, label in [(['site', 'genre'], 'site x type, damage'), (['site', 'genre', 'museum'], 'site x type x museum, damage')]:
        ev, ft = run(h, keys, label)
        if ev is None:
            E.append(dict(event=short, name=name, type=typ, year=yr, control=label, note='too few in shared strata')); continue
        E.append(dict(event=short, name=name, type=typ, year=yr, **ev)); F.append(ft.assign(event=short, type=typ, year=yr))
    print(short, E[-2].get('vae_shift'), E[-2].get('p_vae_shift'), '| museum:', E[-1].get('vae_shift'), E[-1].get('p_vae_shift'))
E = pd.DataFrame(E); F = pd.concat(F)
for lab in E.control.unique():
    k = E.control.eq(lab) & E.p_vae_shift.notna()
    E.loc[k, 'q_vae_shift'] = bh(E.loc[k, 'p_vae_shift']); E.loc[k, 'q_vae_disp'] = bh(E.loc[k, 'p_vae_disp'])
    k = F.control.eq(lab) & F.p_shift.notna()
    F.loc[k, 'q_shift'] = bh(F.loc[k, 'p_shift']); F.loc[k, 'q_disp'] = bh(F.loc[k, 'p_disp'])
E.to_csv(f'{O}/tp_protocol_events{SUF}.csv', index=False); F.to_csv(f'{O}/tp_protocol_features{SUF}.csv', index=False)
pd.concat(C).to_csv(f'{O}/tp_protocol_counts{SUF}.csv', index=False)
print(E[['event', 'type', 'control', 'n_before', 'n_after', 'strata', 'vae_shift', 'vae_shift_excess', 'q_vae_shift', 'vae_disp', 'q_vae_disp']].to_string())
print(F[(F.q_shift < 0.05) & F.control.str.contains('museum')].groupby('event').feature.apply(list).to_string())
