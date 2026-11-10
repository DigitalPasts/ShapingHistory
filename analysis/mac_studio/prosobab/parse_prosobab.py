"""Parse the needed tables from the Prosobab MySQL dump (DANS doi:10.17026/DANS-ZVN-EECE, CC BY-NC) into CSVs."""
import os, re, sys, pandas as pd
D = os.path.expanduser('~/deeplomatics-repro/prosobab/data')
TABLES = ['e_tablets', 's_types', 's_subtypes', 's_localities', 'c_archives', 'x_mentionedsubtypesobjects']
sql = open(f'{D}/prosobab.sql', encoding='utf-8').read()

def parse_values(s, i):
    """parse '(..),(..);' starting at s[i]; returns rows, end index"""
    rows, row, cur, inq, n = [], [], [], False, len(s)
    while i < n:
        c = s[i]
        if inq:
            if c == '\\': cur.append({'n': '\n', 'r': '\r', 't': '\t', '0': '\0'}.get(s[i + 1], s[i + 1])); i += 2; continue
            if c == "'":
                if i + 1 < n and s[i + 1] == "'": cur.append("'"); i += 2; continue
                inq = False; i += 1; continue
            cur.append(c); i += 1; continue
        if c == "'": inq = True; quoted = True
        elif c == '(': row, cur, quoted = [], [], False
        elif c in ',)':
            if row is not None and (cur or c == ')' or True):
                v = ''.join(cur); row.append(v if quoted else (None if v.strip() == 'NULL' else v.strip()))
                cur, quoted = [], False
                if c == ')': rows.append(row); row = None
        elif c == ';': return rows, i
        elif not c.isspace() or cur: 
            if row is not None: cur.append(c)
        i += 1
        if c == ',' and row is None: row = None
    return rows, i

for t in TABLES:
    out = []
    for m in re.finditer(r'INSERT INTO `%s` \(([^)]*)\) VALUES\s*' % t, sql):
        cols = [c.strip(' `') for c in m.group(1).split(',')]
        rows, _ = parse_values(sql, m.end())
        out += rows
    df = pd.DataFrame(out, columns=cols)
    df.to_csv(f'{D}/{t}.csv', index=False)
    print(t, df.shape)
