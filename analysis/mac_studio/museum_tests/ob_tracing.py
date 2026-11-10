"""Which Old Babylonian city groups do later (non-OB) tablets resemble, with and without same-museum OB neighbours?
DINOv2 ViT-B/14 mask embeddings, tablets only, L2-normalised, cosine and CSLS (k=10) neighbour retrieval (25 NN)."""
import os, time, numpy as np, pandas as pd, torch

t0 = time.time()
ROOT = os.path.expanduser('~/deeplomatics-repro')
OUT = f'{ROOT}/museum_tests'
K_NN, K_CSLS, NBOOT, SEED = 25, 10, 300, 0
dev = 'mps'

emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy')
ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv'); ids['row'] = np.arange(len(ids))
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'),
                  usecols=['artifact_id', 'period', 'provenience', 'collections', 'genres', 'is_school_text', 'artifact_type'], low_memory=False)
df = ids.merge(art, left_on='CDLI_id', right_on='artifact_id')
df = df[df.artifact_type.isin(['tablet', 'tablet & envelope'])].reset_index(drop=True)
df['per'] = df.period.fillna('').str.split(' (', regex=False).str[0].str.strip()
df['city'] = df.provenience.fillna('uncertain').str.split(' (', regex=False).str[0].str.strip()
df['museum'] = df.collections.fillna('unknown').str.split(';').str[0].str.strip()
g = df.genres.fillna('')
schol = g.str.contains('Literary|Lexical|Mathematical|Divination|Scientific|Liturg|Ritual|Incantation', case=False) | (df.is_school_text == 1)
arch = g.str.contains('Administrative|Legal|Letter|Business', case=False) & ~schol  # scholarly wins (e.g. 'Literary letter')
E = emb[df.row.values].astype(np.float32); E /= np.linalg.norm(E, axis=1, keepdims=True)
UNKNOWN = {'uncertain', 'unknown', ''}

rows, hub_rows = [], []
rng = np.random.default_rng(SEED)
for pool, pm in [('archival', arch), ('scholarly', schol)]:
    P = df[pm]
    ob = P[(P.per == 'Old Babylonian') & ~P.city.isin(UNKNOWN)]
    vc = ob.city.value_counts(); ob = ob[ob.city.isin(vc[vc >= 60].index)]
    cities = sorted(ob.city.unique()); C = len(cities)
    q = P[(P.per != 'Old Babylonian') & (P.per != '')]
    qn = q.groupby(['per', 'city']).size(); q = q[q.set_index(['per', 'city']).index.isin(qn[qn >= 30].index)]
    R = torch.from_numpy(E[ob.index]).to(dev); Q = torch.from_numpy(E[q.index]).to(dev)
    r_city = np.array([cities.index(c) for c in ob.city]); r_mus = pd.factorize(pd.concat([ob.museum, q.museum]))[0]
    r_mus, q_mus = torch.tensor(r_mus[:len(ob)], device=dev), torch.tensor(r_mus[len(ob):], device=dev)
    # CSLS penalty: each OB tablet's mean cosine to its K_CSLS nearest query tablets
    rS = torch.cat([(R[i:i + 2048] @ Q.T).topk(K_CSLS, dim=1).values.mean(1) for i in range(0, len(R), 2048)])
    onehot = np.eye(C)[r_city]
    city_size = onehot.sum(0)
    # per-museum city counts for mode-b base
    mus_city = np.zeros((int(max(r_mus.max(), q_mus.max())) + 1, C)); np.add.at(mus_city, r_mus.cpu().numpy(), onehot)
    print(pool, 'OB refs', len(ob), 'cities', C, 'queries', len(q), 'groups', q.groupby(['per', 'city']).ngroups, flush=True)
    for mode in ['a_all', 'b_other_museum']:
        for metric in ['cosine', 'csls']:
            nbr = []
            for i in range(0, len(Q), 2048):
                S = Q[i:i + 2048] @ R.T
                if metric == 'csls': S = 2 * S - rS[None]
                if mode == 'b_other_museum': S = S.masked_fill(q_mus[i:i + 2048, None] == r_mus[None], -1e9)
                nbr.append(S.topk(K_NN, dim=1).indices.cpu().numpy())
            nbr = np.concatenate(nbr)
            share = np.stack([np.bincount(r, minlength=C) for r in r_city[nbr]]) / K_NN       # (nq, C)
            if mode == 'a_all':
                base = np.tile(city_size / city_size.sum(), (len(q), 1))
            else:
                rem = city_size[None] - mus_city[q_mus.cpu().numpy()]
                base = rem / rem.sum(1, keepdims=True)
            occ = np.bincount(nbr.ravel(), minlength=len(ob))
            for ci, c in enumerate(cities):
                hub_rows.append(dict(mode=mode, metric=metric, pool=pool, ob_city=c, n_ob=int(city_size[ci]),
                                     share_of_neighbours=occ[r_city == ci].sum() / occ.sum(), base=base[:, ci].mean(),
                                     hub_ratio=(occ[r_city == ci].sum() / occ.sum()) / base[:, ci].mean(),
                                     max_k_occurrence=int(occ[r_city == ci].max())))
            qi = q.reset_index(drop=True)
            for (per, city), gi in qi.groupby(['per', 'city']).indices.items():
                sh, bs = share[gi], base[gi]
                b = rng.integers(0, len(gi), (NBOOT, len(gi)))
                boot = sh[b].mean(1) / np.maximum(bs[b].mean(1), 1e-12)
                lift = sh.mean(0) / np.maximum(bs.mean(0), 1e-12)
                lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
                for ci, c in enumerate(cities):
                    rows.append(dict(mode=mode, metric=metric, pool=pool, period=per, city=city, n=len(gi), ob_city=c,
                                     share=sh[:, ci].mean(), base=bs[:, ci].mean(), lift=lift[ci], lo=lo[ci], hi=hi[ci]))
res = pd.DataFrame(rows); res.to_csv(f'{OUT}/ob_tracing.csv', index=False)
hub = pd.DataFrame(hub_rows); hub.to_csv(f'{OUT}/ob_tracing_hubness.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.precision', 3); pd.set_option('display.max_rows', 500)
sel = res[(res['mode'] == 'b_other_museum') & (res.metric == 'csls') & (res.lo > 1) & (res.share >= 0.05)].sort_values(['pool', 'period', 'city', 'lift'], ascending=[True, True, True, False])
sel.to_csv(f'{OUT}/ob_tracing_b_csls_significant.csv', index=False)
print(sel.to_string(index=False))
print(hub.pivot_table(index=['pool', 'ob_city', 'n_ob'], columns=['mode', 'metric'], values='hub_ratio').to_string())
cnt = sel.groupby(['pool', 'ob_city']).size().rename('n_groups_lo>1'); print(cnt.to_string())
print(f'runtime {time.time() - t0:.0f}s')
