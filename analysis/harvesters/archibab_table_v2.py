"""Save the full Archibab text table (all 36,060 texts) to archibab_textes_v2.csv, as the website shows it.

Version 2 (9 Nov 2026): the first run saved 199 pages twice, because the page counter changed before the
table itself had redrawn, so the previous page's rows were read again (31,100 of 36,060 texts kept).
This version waits until the table shows new rows (first text id differs from the previous page and the
rows stop changing) before reading, re-reads a page that still overlaps the previous one, and prints a
check at the end (texts saved vs unique ids).

Run on your own computer, where archibab.fr opens normally:
    pip install playwright pandas
    playwright install chromium
    python archibab_table_v2.py
It opens www.archibab.fr/textes in a browser window, reads each results page (25 rows), clicks "next",
waits until the new rows are drawn, and repeats: about 1,443 pages, roughly 40 to 80 minutes. It saves after every page, so if it
stops you can run it again and it continues where it left off. Nothing is sent anywhere.
"""
import csv, os, re, time
from playwright.sync_api import sync_playwright

OUT = 'archibab_textes_v2.csv'
COLS = ['id', 'reference', 'museum_no', 'type', 'from_to', 'from_to_site_links', 'date', 'date_links',
        'archives', 'archives_links', 'n_publications', 'summary', 'page']
PAUSE = 1.0  # seconds between pages; please keep it slow

ROWS_JS = r"""
() => [...document.querySelectorAll('table.table tbody tr')].map(tr => {
  const td = [...tr.querySelectorAll(':scope > td')];
  if (td.length < 6) {                       // the summary line under each text
    const r = tr.querySelector('.texte-resume'); return {summary: r ? r.innerText.trim() : null};
  }
  const links = el => [...el.querySelectorAll('a')].map(a => a.innerText.trim() + ' <' + a.href + '>').join(' | ');
  return {
    id: td[0].innerText.trim().split(/\s+/)[0],
    reference: td[1].innerText.trim().replace(/\s+/g, ' '),
    type: td[2].innerText.trim(),
    from_to: td[3].innerText.trim().replace(/\s+/g, ' '),
    from_to_site_links: links(td[3]),
    date: td[4].innerText.trim().replace(/\s+/g, ' '),
    date_links: links(td[4]),
    archives: td[5].innerText.trim().replace(/\s+/g, ' '),
    archives_links: links(td[5]),
    n_publications: (td[6] ? td[6].innerText.trim() : ''),
  };
})
"""

def current_page(page):
    t = page.locator('.p-paginator-current').first.inner_text()
    m = re.match(r'\s*(\d+)\s+de\s+(\d+)', t)
    return int(m.group(1)), int(m.group(2))

IDS_JS = r"""() => [...document.querySelectorAll('table.table tbody tr')]
  .map(tr => tr.querySelectorAll(':scope > td')).filter(td => td.length >= 6)
  .map(td => td[0].innerText.trim().split(/\s+/)[0])"""

def wait_new_rows(page, prev_ids):
    """Wait until the table holds rows that are not the previous page's, and are stable."""
    last = None
    for _ in range(120):                                   # up to ~60 s
        ids = page.evaluate(IDS_JS)
        if ids and not (set(ids) & prev_ids) and ids == last:
            return ids
        last = ids
        time.sleep(0.5)
    return page.evaluate(IDS_JS)

def main():
    saved = {}                                             # page -> ids already in the file
    if os.path.exists(OUT):
        with open(OUT, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                saved.setdefault(int(r['page']), set()).add(r['id'])
    done = set(saved)
    new = not os.path.exists(OUT)
    with sync_playwright() as p, open(OUT, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new: w.writeheader()
        b = p.chromium.launch(headless=False)
        page = b.new_page()
        page.goto('https://www.archibab.fr/textes', wait_until='networkidle', timeout=120000)
        page.wait_for_selector('.p-paginator-current', timeout=120000)
        n, total = current_page(page)
        print('pages:', total, '| already saved:', len(done))
        while True:
            if n not in done:
                prev_ids = saved.get(n - 1, set())
                ids = wait_new_rows(page, prev_ids)
                if set(ids) & prev_ids:
                    print(f'WARNING page {n}: still overlaps the previous page', flush=True)
                rows, last = [], None
                for r in page.evaluate(ROWS_JS):
                    if 'id' in r:
                        m = re.search(r'\[([^\]]+)\]', r['reference'])
                        r.update(museum_no=m.group(1) if m else '', page=n, summary=''); rows.append(r); last = r
                    elif last is not None:
                        last['summary'] = r['summary'] or ''
                w.writerows(rows); f.flush(); done.add(n)
                saved[n] = {r['id'] for r in rows}
                print(f'page {n}/{total}: {len(rows)} texts', flush=True)
            if n >= total: break
            nxt = page.locator('button.p-paginator-next').first   # the page has two paginators (top and bottom)
            nxt.click(); time.sleep(PAUSE if n + 1 not in done else 0.3)   # move faster over pages already saved
            for _ in range(60):                                  # wait until the page number changes
                m, _t = current_page(page)
                if m != n: break
                time.sleep(0.5)
            n = m
        b.close()
    with open(OUT, encoding='utf-8') as f:
        rr = list(csv.DictReader(f))
    print('done:', OUT, '| rows', len(rr), '| unique texts', len({r["id"] for r in rr}),
          '| pages', len({r["page"] for r in rr}))

if __name__ == '__main__':
    main()
