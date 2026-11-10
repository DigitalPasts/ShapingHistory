"""Which Mesopotamian period do peripheral tablets resemble, controlling for museum? DINOv2 768-d L2-normalised, cosine/CSLS.
Each peripheral tablet: k=20 nearest core tablets by CSLS, only neighbours held in a different museum. Baseline: the same search
for core tablets held in the group's museums, re-weighted to the group's museum mix, excluding same-museum neighbours and
neighbours from the query's own (period, city). Lift(X) = group share of neighbours in period X / baseline share.
CSLS hub term: each core tablet's mean cosine to its 10 nearest core tablets (query-side term is constant per query)."""
import os, time, numpy as np, pandas as pd, torch

t0 = time.time()
ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/archibab'
K, K_HUB, NBOOT, MAX_BASE, MIN_SHARE, SEED = 20, 10, 1000, 3000, 0.02, 0
rng = np.random.default_rng(SEED); dev = 'mps'
ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv').CDLI_id.values
emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy').astype(np.float32)
pos = pd.Series(np.arange(len(ids)), index=ids)
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), low_memory=False,
                  usecols=['artifact_id', 'period', 'provenience', 'collections', 'genres', 'artifact_type'])
T = art[art.artifact_id.isin(ids) & art.artifact_type.isin(['tablet', 'tablet & envelope'])].copy()
T['per'] = T.period.fillna('').str.split(' (', regex=False).str[0].str.strip()
T['city'] = T.provenience.fillna('uncertain').str.split(' (', regex=False).str[0].str.strip()
T['museum'] = T.collections.fillna('unknown').str.split(';').str[0].str.strip()
T['genre'] = T.genres.fillna('').str.strip()
T = T.reset_index(drop=True)
E = torch.from_numpy(emb[pos.loc[T.artifact_id].values]); E = torch.nn.functional.normalize(E, dim=1).to(dev)

GROUPS = {
    'Amarna': (T.city == 'Akhetaten'),
    'Nuzi': (T.city == 'Gasur/Nuzi') & (T.per == 'Middle Babylonian'),
    'Alalakh VII': (T.city == 'Alalakh') & (T.per == 'Old Babylonian'),
    'Alalakh IV': (T.city == 'Alalakh') & (T.per == 'Middle Babylonian'),
    'Hattusa': (T.city == 'Ḫattusa'),
    'Anshan': (T.city == 'Anšan') & (T.per == 'Middle Elamite'),
    'Susa OB': (T.city == 'Susa') & (T.per == 'Old Babylonian'),
    'Kanesh': (T.city == 'Kanesh') & (T.per == 'Old Assyrian'),
    'Tuttul OB': (T.city == 'Tuttul') & T.per.isin(['Old Babylonian', 'Early Old Babylonian']),
}
CONTEMP = {'Amarna': ['Middle Babylonian'], 'Nuzi': ['Middle Babylonian', 'Middle Assyrian'], 'Alalakh VII': ['Old Babylonian'],
           'Alalakh IV': ['Middle Babylonian'], 'Hattusa': ['Middle Babylonian'], 'Anshan': ['Middle Babylonian', 'Middle Assyrian'],
           'Susa OB': ['Old Babylonian'], 'Kanesh': ['Ur III', 'Old Babylonian'], 'Tuttul OB': ['Old Babylonian']}
periph = np.zeros(len(T), bool)
for m in GROUPS.values(): periph |= m.values
core = (~periph) & ~T.city.isin(['uncertain', 'unclear', '']).values & ~T.per.isin(['', 'modern', 'other', 'uncertain']).values
ci = np.where(core)[0]; C = T.iloc[ci].reset_index(drop=True)
periods = sorted(C.per.unique()); cper = np.array([periods.index(p) for p in C.per])
mus_codes = pd.factorize(T.museum)[0]; cmus = torch.tensor(mus_codes[ci], device=dev)
grp_codes = pd.factorize(T.per + '|' + T.city)[0]; cgrp = torch.tensor(grp_codes[ci], device=dev)
gen_codes = pd.factorize(T.genre)[0]; cgen = torch.tensor(gen_codes[ci], device=dev)
Ec = E[ci]
hub = torch.cat([(Ec[i:i + 2048] @ Ec.T).topk(K_HUB + 1, dim=1).values[:, 1:].mean(1) for i in range(0, len(Ec), 2048)])
print('core tablets', len(C), '| periods', len(periods), flush=True)

def neighbour_shares(qi, exclude_own_group, genre=None):
    """qi = row indices into T. Returns (len(qi), n_periods) neighbour-period shares."""
    out = []
    for s in range(0, len(qi), 1024):
        b = qi[s:s + 1024]; bt = torch.tensor(b, device=dev)
        S = 2 * (E[bt] @ Ec.T) - hub[None]
        bad = cmus[None] == torch.tensor(mus_codes[b], device=dev)[:, None]
        if exclude_own_group: bad |= cgrp[None] == torch.tensor(grp_codes[b], device=dev)[:, None]
        if genre is not None: bad |= (cgen != genre)[None]
        nb = S.masked_fill(bad, -1e9).topk(K, dim=1).indices.cpu().numpy()
        sh = np.zeros((len(b), len(periods))); np.add.at(sh, (np.repeat(np.arange(len(b)), K), cper[nb.ravel()]), 1)
        out.append(sh / K)
    return np.concatenate(out)

rows = []
for name, m in GROUPS.items():
    gi = np.where(m.values)[0]; G = T.iloc[gi]
    top_genre, top_share = G.genre.value_counts().index[0], G.genre.value_counts(normalize=True).iat[0]
    for mode in ['all_genres', 'same_genre']:
        if mode == 'same_genre' and (top_share < 0.4 or top_genre == ''): continue
        gsel = gi if mode == 'all_genres' else gi[(G.genre == top_genre).values]
        gcode = None if mode == 'all_genres' else gen_codes[gsel[0]]
        gm = T.museum.iloc[gsel].value_counts()
        # baseline: core tablets in the group's museums (same genre in same-genre mode), capped per museum, re-weighted
        bi, bw = [], []
        for mu, cnt in gm.items():
            pool = ci[(C.museum == mu).values & ((C.genre == top_genre).values if mode == 'same_genre' else True)]
            if len(pool) == 0: continue
            pick = pool if len(pool) <= MAX_BASE else rng.choice(pool, MAX_BASE, replace=False)
            bi.append(pick); bw.append(np.full(len(pick), cnt / len(pick)))
        baseline_kind = 'museum-matched'
        if not bi:   # none of the group's museums hold core tablets: fall back to an unweighted core sample (flagged)
            pool = ci[(C.genre == top_genre).values] if mode == 'same_genre' else ci
            bi, bw = [rng.choice(pool, min(len(pool), 5000), replace=False)], [np.ones(min(len(pool), 5000))]
            baseline_kind = 'FALLBACK all-core sample'
        bi, bw = np.concatenate(bi), np.concatenate(bw)
        covered = T.museum.iloc[gsel].isin(T.museum.iloc[bi].unique()).values
        gs = neighbour_shares(gsel, False, gcode); bs = neighbour_shares(bi, True, gcode)
        base = (bs * bw[:, None]).sum(0) / bw.sum(); share = gs.mean(0)
        boot = np.stack([gs[rng.integers(0, len(gs), len(gs))].mean(0) for _ in range(NBOOT)]) / np.maximum(base, 1e-12)
        lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
        for k, p in enumerate(periods):
            rows.append(dict(group=name, mode=mode, genre=top_genre if mode == 'same_genre' else 'all', n=len(gsel),
                             n_museums=int(gm.size), museums=' | '.join(f'{a} ({b})' for a, b in gm.items()),
                             share_museums_with_baseline=covered.mean(), n_baseline=len(bi), baseline=baseline_kind, period=p, share=share[k],
                             base=base[k], lift=share[k] / base[k] if base[k] > 0 else np.nan, lo=lo[k], hi=hi[k],
                             contemporary=p in CONTEMP[name]))
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/05_periphery_sources.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.precision', 3); pd.set_option('display.max_colwidth', 160)
for (g, mode), h in R.groupby(['group', 'mode'], sort=False):
    top = h[h.share >= MIN_SHARE].sort_values('lift', ascending=False).head(4)
    print(f'\n== {g} / {mode} ({h.genre.iat[0]}) n={h.n.iat[0]}  museums: {h.museums.iat[0]}  baseline n={h.n_baseline.iat[0]} ({h.baseline.iat[0]})  group tablets in museums with baseline: {h.share_museums_with_baseline.iat[0]:.2f}')
    print(top[['period', 'share', 'base', 'lift', 'lo', 'hi']].to_string(index=False))
    print('contemporary:', h[h.contemporary][['period', 'share', 'base', 'lift', 'lo', 'hi']].to_string(index=False, header=False))
print(f'runtime {time.time() - t0:.0f}s')
