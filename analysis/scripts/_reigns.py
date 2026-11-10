"""Reign spans (BCE, accession year to last year; middle chronology as in 98j, where a tablet dated only by reign
carries the accession year in `bce`). A tablet dated only to a reign enters a before/after window only when the whole
reign lies inside that window; otherwise its accession year would pass for its date (heaping found 10 Nov 2026)."""
import numpy as np
REIGN = {  # king_final: (first year, last year)
    'Ur-Namma': (2110, 2093), 'Šulgi': (2092, 2045), 'Amar-Suen': (2044, 2036), 'Šū-Suen': (2035, 2027), 'Ibbi-Suen': (2026, 2003),
    'Sargon': (2334, 2279), 'Rimush': (2278, 2270), 'Naramsin': (2254, 2218), 'Shar-kali-sharri': (2217, 2193),
    'Lugalanda': (2358, 2352), 'Urukagina_e': (2351, 2346), 'Urukagina_l': (2350, 2342), 'Urukagina': (2351, 2342),
    'Warad-Sin': (1834, 1823), 'Rim-Sin': (1822, 1763), 'Hammurapi': (1792, 1750), 'Samsu-iluna': (1749, 1712),
    'Abi-ešuh': (1711, 1684), 'Ammi-ditana': (1683, 1647), 'Ammi-saduqa': (1646, 1626),
    'Tiglath-pileser3': (745, 727), 'Shalmaneser5': (726, 722), 'Sargon2': (722, 705), 'Sennacherib': (705, 681),
    'Esarhaddon': (681, 669), 'Assurbanipal': (669, 631), 'Assur-etel-ilani': (631, 627), 'Sin-sharru-ishkun': (627, 612),
    'Šamaš-šuma-ukīn': (668, 648), 'Nabopolassar': (626, 605), 'Nebuchadnezzar': (605, 562), 'Nebuchadnezzar2': (605, 562),
    'Amel-Marduk': (562, 560), 'Neriglissar': (560, 556), 'Nabonidus': (556, 539), 'Cyrus': (539, 530), 'Cambyses': (530, 522),
    'Darius1': (522, 486), 'Xerxes': (486, 465), 'Artaxerxes1': (465, 424), 'Darius2': (424, 405)}

def in_window(g, lo, hi):
    """rows whose date lies in [lo, hi] BCE: year-dated tablets by their year; reign-dated tablets only if the whole
    reign lies in [lo, hi]."""
    yk = g.year_known.fillna(False).astype(bool).to_numpy()
    first = g.king_final.map(lambda k: REIGN.get(k, (np.nan, np.nan))[0]).to_numpy(float)
    last = g.king_final.map(lambda k: REIGN.get(k, (np.nan, np.nan))[1]).to_numpy(float)
    by_year = yk & g.bce.between(lo, hi).to_numpy()
    by_reign = (~yk) & (first <= hi) & (last >= lo)
    return by_year | by_reign
