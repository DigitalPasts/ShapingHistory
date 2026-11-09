"""SI text codebook for the centralization parameters: definitions, origin, anchors with operational tests, decision
rules, boundary cases, and for every period the quoted evidence behind its score. The prose is fixed here; the
evidence tables are generated from lit_evidence_long.csv and lit_scores_long.csv, so the codebook always matches the
scores. Output: centralization/si_codebook.md (whole) and centralization/si_codebook_<section>.md (one per section)."""
from _paths import SHARED, WORK
import re, pandas as pd
C=WORK+'/centralization'; PJ=SHARED+'/centralization'
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian',
      'Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
SI=['Hittite','Middle Elamite']
CB=pd.read_csv(f'{PJ}/centralization_codebook.csv').set_index('param')
L=pd.read_csv(f'{C}/lit_scores_long.csv').set_index(['period','param'])
E=pd.read_csv(f'{C}/lit_evidence_long.csv')
FIX={'vandemieroop':'Van De Mieroop','vandenhout':'van den Hout','mofidi':'Mofidi Nasrabadi','mofidinasrabadi':'Mofidi Nasrabadi',
     'degraef':'De Graef','coro':'Corò','malbran':'Malbran-Labat','basello':'Basello and Giovinazzo','westenholz':'Sallaberger and Westenholz',
     'sallaberger':'Sallaberger','wasserman':'Wasserman and Bloch','monerie':'Monerie','gesche':'Gesche'}
def short(k):
    m=re.match(r'([a-z]+?)(?=[A-Z]|$)',str(k)); y=re.search(r'(\d{4})[a-z]?$',str(k)); a=m.group(1) if m else str(k)
    return f"{FIX.get(a,a[:1].upper()+a[1:])} {y.group(1) if y else ''}".strip()
def clip(q,n=260):
    q=' '.join(str(q).split()).replace('|','/')
    return q if len(q)<=n else q[:n].rsplit(' ',1)[0]+' ...'
def where(w): return str(w).replace('|','/')
def cite(k,w):
    w=where(w); a=short(k)
    return w if w.split(' ')[0].rstrip(',')==a.split(' ')[0] else f"{a}, {w}"


# ---------------------------------------------------------------- prose
INTRO="""## 1. Purpose, origin and procedure

This codebook defines the twelve parameters used to describe how centralized each period's polity was, and documents every score with quotations from the historical literature. A reader can check each score against the anchors below and the statements in the evidence tables, and re-score it in the accompanying worksheet.

**Why these parameters.** "Centralization" is not one variable. Historians of the ancient Near East use the word for at least three different things: how far a ruler's reach extended (territory, officials, taxes, messengers), which institutions held the economy and its records (palace, temple, private households), and how far the state shaped the practice of writing itself (procedures, schooling, law, standards). We therefore score twelve parameters in three dimensions:

| Dimension | Parameters | Question it answers |
| --- | --- | --- |
| A. Polity reach | TERR, HIER, FISC, COMM | How far did royal power extend, and through what channels? |
| B. Institutional economy | PAL, TEMP, TCTL, PRIV | Which households held the economy and its archives, and did the crown control them? |
| C. Control of writing and norms | BUR, SCHOOL, LAW, STD | Did the state standardize procedure, training, justice and measures? |

**Where the parameters come from.** Each parameter combines three sources. (1) A comparable Seshat variable where one exists (polity territory, administrative levels, couriers and postal stations, formal legal code, calendar). (2) General theory of state capacity: Mann's extensive and infrastructural power, Weber's bureaucracy, Scott's legibility, and the work of Monson and Scheidel on fiscal regimes. (3) The specific debates of Assyriology: the temple-city model and its critique, Diakonoff's two-sector model, the extent of Ur III bureaucracy, the nature of the law collections, and household versus institutional schooling. Seshat alone proved too coarse for our purpose: most of its variables take the same value in nearly every Mesopotamian period. The grouping into three dimensions is our own and not taken from a published scheme. Section 5 lists the Seshat variable for each parameter.

**What a score means.** Every parameter is scored 0 to 3. The four anchors describe historical states of affairs, from the least to the most centralized. **A score of 0 is not a missing value.** It is the lowest anchor and describes a real, low state, for example "single city-state" (TERR) or "marginal" (PAL, TEMP). Thin evidence is never coded as 0; it shows as low confidence, a wide range and few sources. For three parameters (COMM, BUR, LAW) the 0 anchor reads "none known" or "no evidence", which does not separate absence from silence; no main-period cell scores 0 on these three. Section 5 discusses the eight cells that score 0.

**How a score is derived.** Each piece of evidence is one published statement, quoted verbatim with its page, about one period and one parameter. We record the score the statement implies and its stance: *supports* (the statement describes the state of affairs of that anchor), *qualifies* (it accepts the institution but limits its reach), or *contests* (it argues for a different score against the prevailing view). The point score of a cell is the median of the scores implied by its supporting statements, rounded down at .5 (the conservative choice). The range runs over all statements, whatever their stance. A cell is *contested* when a contesting statement implies a score other than the point score. Confidence is H when at least two statements support the score, none contests it and all agree; M when at least one supports it and the range spans at most one step; L otherwise. For the uncertainty analysis each cell becomes a distribution over 0-3, with weight 1 for each supporting statement and 0.5 for each qualifying or contesting one.

**How to read the evidence tables.** Each parameter has a table with one row per period. "Score" gives the point score, the range and the confidence. "Key statement" quotes a supporting statement that implies the point score (the fullest one, shortened to about 260 characters). "Other statements" lists the remaining sources with the score each implies and its stance (s = supports, q = qualifies, c = contests). Contesting statements are quoted below the table. Hittite and Middle Elamite, which enter only the SI analysis, close each table. All 524 statements, with full quotations, are in the Evidence sheet of the worksheet and in the review page."""

DIMS={
'A':("## 2. Dimension A: polity reach",
 "Dimension A measures how far royal power extended and through which channels it acted. Its four parameters follow the sequence by which a ruler governs territory beyond the capital: the territory itself, the officials who govern it, the revenues taken from it, and the messengers who connect it.",
 ['TERR','HIER','FISC','COMM']),
'B':("## 3. Dimension B: institutional economy",
 "Dimension B asks which households held the economy and produced its records. It reflects the long debate between the temple-city model (Deimel, Falkenstein), its critique (Gelb, Foster), Diakonoff's two-sector model and later views of the patrimonial household (Schloen). PAL, TEMP and PRIV measure weight in the written record, not only in the economy, so they are sensitive to which archives happen to be excavated. PRIV enters index B reversed (3 minus PRIV), because a large private sector means less institutional control of the economy.",
 ['PAL','TEMP','TCTL','PRIV']),
'C':("## 4. Dimension C: control of writing and norms",
 "Dimension C asks how far the state shaped writing practice and the norms written documents follow. These parameters are closest to our outcome, the form of tablets. To keep the outcome out of its own predictor they should rest on statements about procedure, training, law and standards. Some quoted statements also mention tablet shape or format; they are marked [format] in the tables, and Section 5 shows what happens to the scores without them.",
 ['BUR','SCHOOL','LAW','STD']),
}

P={
'TERR':dict(
 what="The extent of the territory ruled by one king at the period's height: one city, several cities, a whole region, or several regions held as provinces or vassals.",
 why="Territorial reach is the classic measure of extensive power (Mann) and of social scale in Seshat. If centralization produces uniform tablets, wider rule should spread one format over more scribes.",
 origin="Seshat *Polity territory*; Mann 1986 (extensive power); the debate on whether the Sargonic and Ur III states were empires or hegemonies of city-states.",
 tests=["Only one city and its hinterland under the ruler; neighbouring cities independent.",
        "Several cities under one ruler or bound in a league, within one region.",
        "One king rules a whole region, for example all of Sumer and Akkad or all of Assyria.",
        "Several regions held as provinces or by vassal treaty, beyond the home region."],
 rules=["Score the polity whose tablets dominate the corpus for that period, at its documented height, not its founding.",
        "A commercial network is not territory. Old Assyrian trade colonies in Anatolia did not belong to the city of Assur, so Old Assyrian scores 0.",
        "A league of cities (ED IIIa Šuruppak) scores 1, not 2: the cities keep their own rulers.",
        "Early Old Babylonian is a period of competing kingdoms (Isin, Larsa, Ešnunna, Babylon); score the typical kingdom, which is 1; Ešnunna's wider influence (De Graef 2022 p. 424) is the upper bound."],
 cross="Ur III (3) and Early Old Babylonian (1) show the scale's span within a few generations: the same cities passed from provinces of one empire to the capitals of rival kingdoms. Hammurabi's conquests return Old Babylonian to 3."),
'HIER':dict(
 what="The number of administrative tiers between the king and the local community that were staffed by royal appointees.",
 why="Tiers of appointed officials are the channel through which a central format could be imposed on provincial scribes.",
 origin="Seshat *Administrative levels*; Weber's bureaucratic hierarchy; debate on the Ur III ensi2 as royal governors versus local dynasts.",
 tests=["A single tier: the city or the great household runs itself.",
        "The capital administers dependent towns directly; no appointed governors.",
        "Provincial governors or equivalents appointed by the king.",
        "Four or more tiers (province, district, town, institution) with royal appointees at each."],
 rules=["Count only offices filled by royal appointment, not hereditary local rulers who acknowledge a king.",
        "Where governors are appointed but come from local families (Ur III ensi2), score 2 or 3 depending on the number of tiers documented, and record the qualification.",
        "Neo-Assyrian is contested (2-3): Baker 2023 points to the era of powerful magnates before Tiglath-pileser III. Neo-Babylonian is contested (2-3): Jursa 2023 p. 113 finds local power more decentralized than in Assyria, although governors and chief priests were royal appointees (p. 118)."],
 cross="Old Akkadian is contested (2-3): Sargon appointed governors (Schrakamp 2020; Yoffee 1995 p. 292), but the lower ranks stayed local and imperial control was loose (Charpin 1995 p. 810). Ur III scores 3."),
'FISC':dict(
 what="Regular extraction of revenue for the crown that is recorded in writing: from ad hoc tribute to an integrated, centrally recorded system across provinces.",
 why="Fiscal extraction is the core of state capacity (Monson and Scheidel 2015). Recorded levies need standardized documents, which could favour uniform tablet formats.",
 origin="No Seshat equivalent; Monson and Scheidel 2015; Hanson and Sigman 2021; Assyriological work on bala, gun2 ma-da, ilkum and satrapal taxation.",
 tests=["No revenue beyond the income of the institutions themselves.",
        "Ad hoc tribute, booty and gifts.",
        "Regular levies on land, produce or service, recorded locally.",
        "An integrated system, recorded centrally, across provinces (for example Ur III bala and gun2 ma-da)."],
 rules=["The levy must be recorded in writing; levies known only from narrative sources score at most 2.",
        "Temple offerings count only when the crown imposes and records them, not when temples receive gifts.",
        "Hellenistic royal taxation recorded on parchment still counts; Messina 2009 p. 179 notes that taxed contracts moved from clay to sealed parchment under Antiochus I."],
 cross="ED IIIa scores 2 on a single statement about corvée levied by labour managers (Bartash 2020); ED IIIb on taxes levied on temple land at Lagaš (Yoffee 1995 p. 289) and silver used for tax payments (Bartash 2020). Ur III, Old Babylonian, Middle Assyrian and the first-millennium empires reach 3."),
'COMM':dict(
 what="The infrastructure by which the crown moved messages and agents: occasional messengers, a regular royal messenger service, or relay stations and roads documented by ration records.",
 why="Infrastructural power (Mann 1984) depends on communication; a fast royal network carries both orders and scribal norms.",
 origin="Seshat *Couriers* and *Postal stations*; Mann 1984; Sallaberger on Ur III messenger texts; Radner on the Neo-Assyrian royal road.",
 tests=["No royal communication known.",
        "Ad hoc messengers, sent case by case.",
        "A regular royal messenger service.",
        "Relay stations or a road network, documented by ration or travel records."],
 rules=["Score the crown's network, not merchants' private correspondence (Old Assyrian letters score 1).",
        "Letters alone show messengers (1); a service needs repeated, administered dispatch (2); stations need ration records at fixed points (3)."],
 cross="ED IIIb scores 1 on one weak statement (Frahm 2015 p. 5: the earliest letters date to the 24th century); it is the thinnest cell in the main analysis. Ur III, Neo-Assyrian and Achaemenid score 3."),
'PAL':dict(
 what="The weight of the palace (crown household) in the economy and in the surviving record.",
 why="If the palace is the dominant producer of documents, a single household's practice sets the norm for a large share of tablets.",
 origin="No Seshat equivalent; Gelb 1979; Diakonoff 1982; Renger 1994; Schloen 2001.",
 tests=["Marginal or absent from the record.",
        "Present but minor in the record.",
        "A major institution.",
        "The dominant institution of the economy and the written record."],
 rules=["Score weight in the record, and note when it may reflect excavation rather than history.",
        "Old Assyrian scores 0 because the texts never mention a palace (Veenhof 2008 p. 39); this is evidence of absence from the record, not silence.",
        "Ebla scores 3: the archive is a palace archive and the palace runs the economy."],
 cross="Ebla (3) and Old Assyrian (0) are the two extremes: the Ebla archive is the palace's own, while the Old Assyrian record never mentions a palace."),
'TEMP':dict(
 what="The weight of temple households in the economy and in the surviving record.",
 why="Temple archives are among the most uniform corpora we measure (Girsu, Eanna, Hellenistic Uruk). TEMP lets us test whether institution type, rather than state power, predicts uniformity.",
 origin="No Seshat equivalent; the temple-city debate (Deimel, Falkenstein, Gelb, Foster); Jursa 2010 and Kleber 2008 for the first millennium.",
 tests=["Marginal.",
        "Present but minor.",
        "A major institution.",
        "The dominant institution of the economy and the record."],
 rules=["ED IIIb is contested (2-3): Steinkeller 1993 p. 122 describes self-sufficient temple households controlling most resources, while Yoffee 1995 pp. 289-290 and Schrakamp (as cited by Bartash 2020) argue that temples were subordinate to the palace.",
        "Ebla scores 0: Steinkeller 1993 p. 124 says the temple household of southern type did not exist there.",
        "Hellenistic scores 3 on Clancier 2011 p. 757 (temple herds and fields) and Monerie and Clancier 2023 p. 73. The surviving cuneiform record of the period comes mainly from the temples of Uruk and Babylon, so this score depends strongly on what was recovered."],
 cross="Neo-Assyrian (1) and Neo-Babylonian (3) mark the north-south contrast of the first millennium."),
'TCTL':dict(
 what="The degree of crown control over temples: from autonomous temples to temples run as units of the state.",
 why="If the crown controls temples, temple archives become channels of state practice; if not, they are independent producers.",
 origin="No Seshat equivalent; Jursa 2010; Kleber 2008; Sallaberger and Westenholz 1999.",
 tests=["Temples autonomous.",
        "Royal patronage only (gifts, building).",
        "Royal appointees in temples, or levies on temples.",
        "Temples run as units of the state, with royal officials auditing their accounts."],
 rules=["Look for royal officials inside temples (šabra appointed by the king, qīpu, ša rēš šarri) and royal audits.",
        "Ur III is contested (2-3): Steinkeller 1987 p. 17 and Garfinkle 2022 pp. 143, 149 describe temples as state property under royal governors, while Sallaberger 1999 pp. 287-288 places control with the provincial governor (ensi2) rather than the crown.",
        "Middle Babylonian is contested (1-3): Sassmannshausen 2001 p. 181 sees royal kin as chancellors of Nippur with levies from much of Babylonia, while Brinkman 2004 p. 287 finds the evidence too scattered for such conclusions."],
 cross="ED IIIb scores 3 on Charpin 1995 p. 809 and Bartash 2020 (rulers of Umma and Lagaš had been temple administrators); Yoffee 1995 p. 289 implies 2. ED IIIa scores 1 on a single qualifying statement (the House of the Lass was close to the ruler)."),
'PRIV':dict(
 what="The weight of private (family) archives in the written record.",
 why="Private archives are produced by many independent writers; a record dominated by them should be less uniform. PRIV enters index B reversed.",
 origin="No Seshat equivalent; Diakonoff's two-sector model; Van De Mieroop 1992; Garfinkle 2012; Schloen 2001.",
 tests=["Negligible.",
        "Some private legal documents (sales, loans).",
        "Substantial private archives.",
        "Private archives dominate the written record."],
 rules=["Score the share of the record, not the size of the private economy.",
        "A 0/1 split between sources is rounded down to 0 (ED IIIa, Ebla); the reader may prefer 1.",
        "A silent record (no private documents survive) is scored 0 by the current rule; Hittite and Middle Elamite are candidates for 'insufficient evidence'."],
 cross="Early and full Old Babylonian (3) and Old Assyrian (3) are the periods of private archives; Ur III is contested (1-2): Garfinkle 2010 p. 186 and 2022 p. 163 stress the autonomy of merchants against the institutional picture."),
'BUR':dict(
 what="Standardized administrative procedure: from no detectable conventions to the same procedures applied across provinces.",
 why="Standard procedure means standard document types, which the bureaucratic hypothesis expects to produce standard tablets.",
 origin="Seshat *Full-time bureaucrats* (partial); Weber 1922; Postgate 2013; Steinkeller 2003; the debate on the Ur III bureaucratic state.",
 tests=["No standard procedure detectable.",
        "Local conventions only.",
        "Standardized accounting within the major institutions.",
        "Standardized procedures across provinces: balanced accounts, instructions to officials, audits."],
 rules=["Score from statements about procedure (account types, audits, instructions), not from tablet form.",
        "Old Akkadian is contested (2-3): Charpin 1995 p. 810 and Yoffee 1995 p. 293 describe standardized accounting under royal control, while Schrakamp 2020 (PDF p. 565) and Foster 1982 p. 22 point to local dating, measures and accounting.",
        "Hellenistic scores 1: royal administration wrote on leather in alphabetic script (Clancier 2011 p. 764; Monerie and Clancier 2023 p. 70), so cuneiform records show no royal procedure."],
 cross="Ur III (3, contested) and Middle Assyrian (3) are the clearest cases; Postgate 2001 p. 193 compares them directly. Old Babylonian scores 2: Postgate 2001 p. 190 calls its practice a 'legal' mode, with parts of the institutional economy handed to private contractors."),
'SCHOOL':dict(
 what="Institutional scribal training: from household apprenticeship to state-controlled training producing scribes for the whole polity.",
 why="Shared training is the obvious mechanism for shared tablet formats.",
 origin="Seshat *Examination system* (poor fit); Veldhuis 2011; Robson 2001; Gesche 2001; Visicato 2000; the edubba debate.",
 tests=["Household apprenticeship without a shared curriculum.",
        "A shared curriculum, taught in households.",
        "Institutional (palace or temple) schooling with a shared curriculum.",
        "State-controlled training producing scribes for the whole polity."],
 rules=["Old Babylonian scores 1: school tablets are usually found in the masters' houses (Charpin 2010 p. 22), and state control was lower than under Ur III (Boivin 2022 p. 612).",
        "Ur III is contested (1-3): Steinkeller 1987 p. 17 and Charpin 1995 p. 812 describe uniform state training, while Sallaberger 1999 p. 130 notes that practically no school tablets were found with the Ur III archives and that sons took up their fathers' profession.",
        "Old Assyrian scores 0: merchants learned to write at home (Larsen 2015 pp. 55-56)."],
 cross="The scale separates curriculum from locus: Kassite exercise tablets are the same type across sites (Veldhuis 2000 p. 67), which supports a shared curriculum but not state control."),
'LAW':dict(
 what="Codified law and royal justice: from no evidence to a law collection together with royal judges and edicts.",
 why="Royal law can standardize legal formulae and thus legal documents, which bears directly on the Hammurabi test.",
 origin="Seshat *Formal legal code*, *Judges*, *Courts*; Westbrook 2003; Charpin 2010; the debate on whether law collections were applied law.",
 tests=["No evidence.",
        "Royal edicts or judgements only.",
        "A law collection, or royal courts.",
        "A law collection together with royal judges and edicts."],
 rules=["A law collection counts whatever its legal status; the debate on its application is noted as a qualification.",
        "Old Babylonian scores 3 (Laws of Hammurabi and mīšarum edicts, Boivin 2022 pp. 603-606), qualified by the reading of the Laws as exemplary royal rulings rather than a legal system (Wasserman and Bloch 2023 pp. 454-455).",
        "Middle Assyrian scores 3: the Middle Assyrian Laws and a compilation of palace decrees (Reculeau 2022 p. 721)."],
 cross="Early Old Babylonian (2: Lipit-Ištar and the Laws of Ešnunna) and Old Babylonian (3) bracket Hammurabi's reign, which is why the break-point test targets it."),
'STD':dict(
 what="State-imposed standards of measure, calendar and dating.",
 why="Imposed standards are a direct form of legibility (Scott 1998); they show the state reaching into documentary practice.",
 origin="Seshat *Calendar* (partial); Scott 1998; Brambor et al. 2020; Bartash 2019 on weight standards.",
 tests=["Local systems only: each city or institution keeps its own measures and dating.",
        "A standard shared within one region or one institution (for example a palace measure beside a temple measure).",
        "One polity-wide standard in ONE domain: metrology OR dating and calendar.",
        "Polity-wide standards in BOTH domains (metrology AND dating or calendar), demonstrably imposed by the crown, so that local variants disappear from the administrative record."],
 rules=["Score imposition by the state, not mere use of common units.",
        "Sharper rule for 2 against 3 (8 Nov 2026, after ShG's note on Old Akkadian STD): a score of 3 needs evidence in both domains and evidence that local variants were displaced. A royal measure beside surviving local calendars is 2. Year names sent out by a chancellery count as dating only when they replace local formulae in the provinces.",
        "Applied: Old Akkadian 2 (measure of Agade, but 'the Akkadian Empire did not have a unified calendar', Foster 2016 ch. 6 §7); Neo-Assyrian 3 (eponym dating, the silver 'mina of Carchemish' after 717 and a court-run calendar: Baker 2023; Weeden 2023 §46.7; Steele 2011 p. 472); Middle Assyrian 2 to 2.5 (one official calendar and eponyms, but Ṭābetu keeps its own calendar, Postgate 2013 pp. 51-52); Hittite 2 at most (weights sealed by the queen, but letters undated, Hoffner 2009 p. 39).",
        "Old Akkadian is contested (1-3): Foster 2016 calls the measure of Agade the first attempt to impose a unified standard, but the governor of Umma kept local dating and the governor of Adab his own date formulae (Schrakamp 2020, PDF p. 549). Bartash 2019 p. 96 shows the reform was a process, not a single act.",
        "Ur III scores 3 (contested, 2-3): royal weights and a state calendar (Steinkeller 1987 p. 17; Bartash 2019 p. 110), while the provinces kept their own calendars (Sallaberger 1999 p. 234)."],
 cross="Neo-Assyrian, Neo-Babylonian and Hellenistic score 3, Achaemenid 2; ED IIIa and IIIb score 1 for local systems."),
}

LIMITS="""## 5. Limits, contested cells and reproduction

**The eight cells that score 0.** A 0 can mean three different things, and the reader should judge each case.

| Cell | Reading | Basis |
| --- | --- | --- |
| Ebla TEMP | Evidence of absence | Steinkeller 1993 p. 124: the southern temple household did not exist at Ebla |
| Old Assyrian TERR | Real low state | Arkhipov 2022: Assur was a city-state |
| Old Assyrian PAL | Evidence of absence from the record | Veenhof 2008 p. 39: OA texts never mention a palace |
| Old Assyrian SCHOOL | Real low state | Larsen 2015 pp. 55-56: household literacy; p. 85 school texts qualify it |
| ED IIIa PRIV | Tie rounded down | Steinkeller 1993 (0) against Bartash 2020 (1, sale contracts) |
| Ebla PRIV | Tie rounded down | Steinkeller 1993 (1) against Bartash 2020 (0) |
| Hittite PRIV | Silent record | van den Hout 2020 p. 16 warns of a "false equilibrium" |
| Middle Elamite PRIV | Silent record | Mofidi Nasrabadi 2018 pp. 245-246: no private documents survive |

**Recovery bias.** PAL, TEMP and PRIV are scored from the surviving record. Where one archive dominates (the Ebla palace, the Hellenistic temples), the score reflects that archive.

**Contested cells.** Twelve cells are contested: ED IIIb TEMP; Old Akkadian HIER, BUR and STD; Ur III TCTL, PRIV, BUR, SCHOOL and STD; Middle Babylonian TCTL; Neo-Assyrian HIER; Neo-Babylonian HIER. Five of the twelve are Ur III, which reflects the long debate on the nature of the Ur III state rather than a lack of evidence.

**Thin cells.** 74 cells rest on a single source. The thinnest main cell is ED IIIb COMM (one weak statement).

**Seshat correspondence.** TERR: Polity territory. HIER: Administrative levels. COMM: Couriers, Postal stations. LAW: Formal legal code, Judges, Courts. BUR: Full-time bureaucrats (partial). SCHOOL: Examination system (poor fit). STD: Calendar (partial). FISC, PAL, TEMP, TCTL, PRIV: none.

**Reproduction.** The evidence entries are in scripts 81_lit_evidence_*.py; script 85 derives the scores, 86 the statistics, 88 the bibliography, 91 the worksheet and 92 this codebook. Every quoted work is in the SI bibliography (lit_centralization.bib)."""

FMT=r'tablet shape|shape of the clay tablets|tablet format|format of|formats for|new type of tablet|elongated|layout|tafelformat|einheitlichkeit der urkunden|unterschrift|kolophon|colophon'
E['fmt']=E.quote.str.contains(FMT,case=False,regex=True)
def param_md(p):
    d=P[p]; out=[f"### {p}: {CB.loc[p,'name']}", f"**Definition.** {d['what']}", f"**Why it matters.** {d['why']}", f"**Origin.** {d['origin']}",
        "| Score | Anchor | Operational test |\n| --- | --- | --- |"]
    anchors=[s.split(' ',1)[1] for s in CB.loc[p,'anchors'].split(' | ')]
    out[-1]+=''.join(f"\n| {i} | {a} | {t} |" for i,(a,t) in enumerate(zip(anchors,d['tests'])))
    out.append(f"**Records that show it.** {CB.loc[p,'proxy']}.")
    out.append("**Decision rules and boundary cases.**\n\n"+'\n'.join(f"- {r}" for r in d['rules']))
    out.append(f"**Across periods.** {d['cross']}")
    out.append(f"**Evidence by period ({p}).**")
    rows=["| Period | Score | Key statement | Other statements |","| --- | --- | --- | --- |"]; contests=[]
    for per in MAIN+SI:
        if (per,p) not in L.index: continue
        s=L.loc[(per,p)]; g=E[(E.period==per)&(E.param==p)].copy()
        if not len(g): continue
        sup=g[g.stance=='supports']; pool=sup if len(sup) else g
        pool=pool.assign(m=(pool.score==s.score).astype(int), ln=pool.quote.str.len()).sort_values(['m','ln'],ascending=[False,False])
        k=pool.iloc[0]
        key=('[format] ' if k.fmt else '')+f"\"{clip(k.quote)}\" ({cite(k.key,k['where'])})"
        rest=g.drop(k.name)
        oth='; '.join(('[format] ' if r.fmt else '')+f"{cite(r.key,r.where)} ({int(r.score)} {r.stance[0]})" for r in rest.itertuples()) or '-'
        lab=per+(' (SI)' if per in SI else '')
        rows.append(f"| {lab} | {int(s.score)} ({s.lo}-{s.hi}, {s.conf}) | {key} | {oth} |")
        for r in g[g.stance=='contests'].itertuples():
            contests.append(f"- {per}, score {int(r.score)}: \"{clip(r.quote,400)}\" ({cite(r.key,r.where)})")
    out.append('\n'.join(rows))
    if contests: out.append("**Contesting statements.**\n\n"+'\n'.join(contests))
    return '\n\n'.join(out)

secs={'0_intro':INTRO}
for k,(h,lead,ps) in DIMS.items():
    secs[f'{ "ABC".index(k)+1}_{k}']='\n\n'.join([h,lead]+[param_md(p) for p in ps])
import numpy as np
def lowmed(x):
    x=sorted(x); n=len(x); return x[(n-1)//2] if n%2 else int(np.floor((x[n//2-1]+x[n//2])/2))
F=E[E.fmt]; chg=[]
for (per,p),g in E.groupby(['period','param']):
    if not g.fmt.any() or (per,p) not in L.index: continue
    h=g[~g.fmt]; sup=h[h.stance=='supports']
    new=lowmed(sup.score.tolist()) if len(sup) else (lowmed(h.score.tolist()) if len(h) else None)
    old=int(L.loc[(per,p)].score)
    chg.append(f"| {per} | {p} | {int(g.fmt.sum())} of {len(g)} | {old} | {new if new is not None else 'no evidence left'} |")
FMTP=("**Statements that mention tablet form.** "+str(len(F))+" of "+str(len(E))+" statements mention tablet shape, format or layout. Because tablet form is our outcome, a cautious reading drops them. The table gives each affected cell's score with and without them.\n\n| Period | Param | Format statements | Score | Without them |\n| --- | --- | --- | --- | --- |\n"+'\n'.join(chg))
LIMITS=LIMITS.replace('**Recovery bias.**',FMTP+'\n\n**Recovery bias.**')
secs['4_limits']=LIMITS
for k,v in secs.items(): open(f'{C}/si_codebook_{k}.md','w').write(v)
full="# SI codebook: centralization parameters\n\n"+'\n\n'.join(secs.values())
open(f'{C}/si_codebook.md','w').write(full)
print({k:len(v) for k,v in secs.items()}, 'words', len(full.split()))
