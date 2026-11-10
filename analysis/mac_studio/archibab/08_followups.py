"""Follow-ups to 04 and 05 (new outputs only).
1. The Middle Babylonian (period, museum) cell behind 04's Letter->letter result: museum, letters' proveniences, publications.
2. 05 rerun with Achaemenid split into Achaemenid-Persepolis (Pārśa) and Achaemenid-Babylonia; Anšan, Susa OB, Nuzi, Hattusa.
3. Examples: for Susa OB (MB/NB), Anšan (Achaemenid), Kanesh letters (Middle Assyrian, letters only) the 3 tablets with most
   cross-museum CSLS neighbours from the driving period(s), each with its 5 nearest cross-museum neighbours.
4. Compact table from 05 (all genres): group x period with share >= 0.01."""
import os, numpy as np, pandas as pd, torch

ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/archibab'
K, K_HUB, NBOOT, MAX_BASE, SEED = 20, 10, 1000, 3000, 0
rng = np.random.default_rng(SEED); dev = 'mps'
ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv').CDLI_id.values
emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy').astype(np.float32)
pos = pd.Series(np.arange(len(ids)), index=ids)
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), low_memory=False,
                  usecols=['artifact_id', 'designation', 'publications_key', 'publications_exact_ref', 'period', 'provenience',
                           'collections', 'genres', 'artifact_type'])
T = art[art.artifact_id.isin(ids) & art.artifact_type.isin(['tablet', 'tablet & envelope'])].copy()
T['per'] = T.period.fillna('').str.split(' (', regex=False).str[0].str.strip()
T['city'] = T.provenience.fillna('uncertain').str.split(' (', regex=False).str[0].str.strip()
T['museum'] = T.collections.fillna('unknown').str.split(';').str[0].str.strip()
T['genre'] = T.genres.fillna('').str.strip()
T['P'] = T.artifact_id.map(lambda x: f'P{int(x):06d}')
T = T.reset_index(drop=True)
pd.set_option('display.width', 250); pd.set_option('display.precision', 3); pd.set_option('display.max_colwidth', 80); pd.set_option('display.max_rows', 500)

# ---------- 1. MB letter cell of 04 ----------
mb = T[(T.per == 'Middle Babylonian') & T.genre.isin(['Letter', 'Legal', 'Administrative'])]
cells = mb.groupby('museum').genre.agg(n_letter=lambda g: (g == 'Letter').sum(), n_other=lambda g: (g != 'Letter').sum())
cells = cells[(cells.n_letter >= 20) & (cells.n_other >= 20)]
print('== 1. MB museums qualifying for Letter (>=20 letters and >=20 other):'); print(cells.to_string())
let = mb[mb.museum.isin(cells.index) & (mb.genre == 'Letter')]
f1a = let.groupby(['museum', 'provenience']).size().rename('n_letters').reset_index()
let = let.assign(pub_main=let.publications_key.fillna('').str.split(';').str[0].str.strip())
f1b = let.groupby(['museum', 'pub_main']).size().rename('n_letters').sort_values(ascending=False).reset_index()
let[['P', 'designation', 'museum', 'provenience', 'publications_key', 'publications_exact_ref']].to_csv(f'{OUT}/08_1_mb_letter_cell_tablets.csv', index=False)
f1a.to_csv(f'{OUT}/08_1_mb_letter_cell_proveniences.csv', index=False); f1b.to_csv(f'{OUT}/08_1_mb_letter_cell_publications.csv', index=False)
print(f1a.to_string(index=False)); print(f1b.head(15).to_string(index=False))
print('designation series:', let.designation.fillna('').str.extract(r'^([^\d,]+)')[0].str.strip().value_counts().head(10).to_dict())

# ---------- shared neighbour machinery (as 05) ----------
E = torch.nn.functional.normalize(torch.from_numpy(emb[pos.loc[T.artifact_id].values]), dim=1).to(dev)
GROUPS = {'Amarna': (T.city == 'Akhetaten'), 'Nuzi': (T.city == 'Gasur/Nuzi') & (T.per == 'Middle Babylonian'),
          'Alalakh VII': (T.city == 'Alalakh') & (T.per == 'Old Babylonian'), 'Alalakh IV': (T.city == 'Alalakh') & (T.per == 'Middle Babylonian'),
          'Hattusa': (T.city == 'Ḫattusa'), 'Anshan': (T.city == 'Anšan') & (T.per == 'Middle Elamite'),
          'Susa OB': (T.city == 'Susa') & (T.per == 'Old Babylonian'), 'Kanesh': (T.city == 'Kanesh') & (T.per == 'Old Assyrian'),
          'Tuttul OB': (T.city == 'Tuttul') & T.per.isin(['Old Babylonian', 'Early Old Babylonian'])}
periph = np.zeros(len(T), bool)
for m in GROUPS.values(): periph |= m.values
core = (~periph) & ~T.city.isin(['uncertain', 'unclear', '']).values & ~T.per.isin(['', 'modern', 'other', 'uncertain']).values
ci = np.where(core)[0]; C = T.iloc[ci].reset_index(drop=True)
Ec = E[ci]
hub = torch.cat([(Ec[i:i + 2048] @ Ec.T).topk(K_HUB + 1, dim=1).values[:, 1:].mean(1) for i in range(0, len(Ec), 2048)])
mus_codes = pd.factorize(T.museum)[0]; cmus = torch.tensor(mus_codes[ci], device=dev)
grp_codes = pd.factorize(T.per + '|' + T.city)[0]; cgrp = torch.tensor(grp_codes[ci], device=dev)
gen_codes = pd.factorize(T.genre)[0]; cgen = torch.tensor(gen_codes[ci], device=dev)

def neighbours(qi, exclude_own_group, genre=None, k=K):
    idx, cos = [], []
    for s in range(0, len(qi), 1024):
        b = qi[s:s + 1024]; bt = torch.tensor(b, device=dev)
        Sc = E[bt] @ Ec.T; S = 2 * Sc - hub[None]
        bad = cmus[None] == torch.tensor(mus_codes[b], device=dev)[:, None]
        if exclude_own_group: bad |= cgrp[None] == torch.tensor(grp_codes[b], device=dev)[:, None]
        if genre is not None: bad |= (cgen != genre)[None]
        nb = S.masked_fill(bad, -1e9).topk(k, dim=1).indices
        idx.append(nb.cpu().numpy()); cos.append(torch.gather(Sc, 1, nb).cpu().numpy())
    return np.concatenate(idx), np.concatenate(cos)

def lift_table(perlabel, groups, modes=('all_genres', 'same_genre')):
    cper_lab = perlabel[ci]; periods = sorted(set(cper_lab)); cper = np.array([periods.index(p) for p in cper_lab])
    rows = []
    for name in groups:
        gi = np.where(GROUPS[name].values)[0]; G = T.iloc[gi]
        tg, ts = G.genre.value_counts().index[0], G.genre.value_counts(normalize=True).iat[0]
        for mode in modes:
            if mode == 'same_genre' and (ts < 0.4 or tg == ''): continue
            gsel = gi if mode == 'all_genres' else gi[(G.genre == tg).values]; gcode = None if mode == 'all_genres' else gen_codes[gsel[0]]
            gm = T.museum.iloc[gsel].value_counts(); bi, bw, kind = [], [], 'museum-matched'
            for mu, cnt in gm.items():
                pool = ci[(C.museum == mu).values & ((C.genre == tg).values if mode == 'same_genre' else True)]
                if len(pool) == 0: continue
                pick = pool if len(pool) <= MAX_BASE else rng.choice(pool, MAX_BASE, replace=False)
                bi.append(pick); bw.append(np.full(len(pick), cnt / len(pick)))
            if not bi:
                pool = ci[(C.genre == tg).values] if mode == 'same_genre' else ci
                bi, bw, kind = [rng.choice(pool, min(len(pool), 5000), replace=False)], [np.ones(min(len(pool), 5000))], 'FALLBACK all-core sample'
            bi, bw = np.concatenate(bi), np.concatenate(bw)
            share_of = lambda nb: np.stack([np.bincount(cper[r], minlength=len(periods)) for r in nb]) / K
            gs = share_of(neighbours(gsel, False, gcode)[0]); bs = share_of(neighbours(bi, True, gcode)[0])
            base = (bs * bw[:, None]).sum(0) / bw.sum(); share = gs.mean(0)
            boot = np.stack([gs[rng.integers(0, len(gs), len(gs))].mean(0) for _ in range(NBOOT)]) / np.maximum(base, 1e-12)
            lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
            for k, p in enumerate(periods):
                rows.append(dict(group=name, mode=mode, genre=tg if mode == 'same_genre' else 'all', n=len(gsel), baseline=kind,
                                 period=p, share=share[k], base=base[k], lift=share[k] / base[k] if base[k] > 0 else np.nan, lo=lo[k], hi=hi[k]))
    return pd.DataFrame(rows)

# ---------- 2. Achaemenid split ----------
per2 = np.where(T.per == 'Achaemenid', np.where(T.city == 'Pārśa', 'Achaemenid-Persepolis', 'Achaemenid-Babylonia'), T.per).astype(object)
R2 = lift_table(per2, ['Anshan', 'Susa OB', 'Nuzi', 'Hattusa'])
R2.to_csv(f'{OUT}/08_2_periphery_achaemenid_split_full.csv', index=False)
f2 = R2[R2.period.str.startswith('Achaemenid')]
f2.to_csv(f'{OUT}/08_2_periphery_achaemenid_split.csv', index=False)
print('\n== 2. Achaemenid split'); print(f2[['group', 'mode', 'genre', 'n', 'period', 'share', 'base', 'lift', 'lo', 'hi']].to_string(index=False))

# ---------- 3. examples ----------
EX = [('Susa OB', ['Middle Babylonian', 'Neo-Babylonian'], None), ('Anshan', ['Achaemenid'], None), ('Kanesh', ['Middle Assyrian'], 'Letter')]
cols = ['P', 'designation', 'per', 'provenience', 'genre', 'museum']
rows = []
for name, drive, gsel in EX:
    gi = np.where(GROUPS[name].values)[0]
    if gsel: gi = gi[(T.genre.iloc[gi] == gsel).values]
    gcode = gen_codes[gi[0]] if gsel else None
    nb, cs = neighbours(gi, False, gcode)
    hits = np.isin(C.per.values[nb], drive).sum(1)
    for r in np.argsort(-hits, kind='stable')[:3]:
        q = T.iloc[gi[r]]
        for j in range(5):
            nn = C.iloc[nb[r, j]]
            rows.append(dict(group=name, driving_period='/'.join(drive), restricted_genre=gsel or 'all',
                             query_P=q.P, query_designation=q.designation, query_genre=q.genre, query_museum=q.museum,
                             query_hits_of_20=int(hits[r]), rank=j + 1, nn_P=nn.P, nn_designation=nn.designation, nn_period=nn.per,
                             nn_provenience=nn.provenience, nn_genre=nn.genre, nn_museum=nn.museum, cosine=cs[r, j]))
f3 = pd.DataFrame(rows); f3.to_csv(f'{OUT}/08_3_examples.csv', index=False)
print('\n== 3. examples'); print(f3.to_string(index=False))

# ---------- 4. compact table from 05 ----------
f4 = pd.read_csv(f'{OUT}/05_periphery_sources.csv')
f4 = f4[(f4['mode'] == 'all_genres') & (f4.share >= 0.01)][['group', 'period', 'share', 'lift', 'lo', 'hi']].round(3)
f4.to_csv(f'{OUT}/08_4_periphery_compact.csv', index=False)
print('\n== 4. compact'); print(f4.to_string(index=False))
