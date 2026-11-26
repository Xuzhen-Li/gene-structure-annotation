import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import SVG, PAL, tint, tw, wrap

OUT = sys.argv[1]
B, O, G, R, P, S, GR = PAL["blue"], PAL["orange"], PAL["green"], PAL["red"], PAL["purple"], PAL["sky"], PAL["grey"]

def badge(s, x, y, n, color):
    s.raw("<circle cx=\"%.1f\" cy=\"%.1f\" r=\"11\" fill=\"%s\"/>" % (x, y, color))
    s.text(x, y + 4.6, str(n), 12.5, True, "#FFFFFF", "middle")

# ---------- 1. route map ----------
def route_map():
    W, H = 1320, 560
    s = SVG(W, H, "Structural annotation route in gene-structure-annotation")
    # inputs band
    s.text(24, 34, "Inputs", 14, True, GR)
    chips = [("Genome FASTA (haplotype)", B), ("Trusted TE library (from vitis-te)", G), ("RNA-seq and/or Iso-Seq reads", O), ("Proteins of related species", P), ("Curated reference GFF3 (if one exists)", R)]
    x = 90
    for t, c in chips:
        w = tw(t, 12.5) + 24
        s.rect(x, 18, w, 26, c, rx=13)
        s.text(x + w / 2, 35.5, t, 12.5, False, "#000000", "middle")
        x += w + 12
    stages = [
        ("Assembly and QC", "Asm0 / Asm1", ["Default: hifiasm (HiFi)", "Check: BUSCO or compleasm, Merqury, LAI", "Already assembled: treat as a checklist"], B),
        ("Soft-mask", "A0", ["RepeatMasker with the trusted vitis-te library", "Soft-mask only; never hard-mask for BRAKER or GALBA"], G),
        ("Evidence and one primary draft", "S-branch", ["RNA: HISAT2 or STAR, then StringTie", "Long reads: minimap2, IsoQuant", "Proteins: miniprot hints", "Default draft S1: BRAKER4"], O),
        ("Combine gene sets", "A4", ["EVidenceModeler (EVM)", "Optional: TSEBRA, Mikado, PASA update", "Only for S14 or when a second gene set exists"], P),
        ("Gene-model QC", "L0 / L1 / L2", ["BUSCO (protein mode), OMArk, PSAURON", "gffcompare, AGAT statistics", "Acceptance levels in docs/EVALUATION.md"], R),
        ("Release and handoff", "A6", ["Clean GFF3, proteins.faa, METHODS", "Validate: gt gff3validator", "Hand proteins.faa to gene-function-annotation"], "#1D7CBB"),
    ]
    n = len(stages); gap = 26; x0 = 24; bw = (W - 2 * x0 - gap * (n - 1)) / n; y0 = 92
    hs = []
    for i, (t, sid, lines, c) in enumerate(stages):
        x = x0 + i * (bw + gap)
        h = s.node(x, y0, bw, t, lines, c, tsize=15, bsize=12, align="start", min_h=190)
        hs.append(h)
        badge(s, x + bw - 16, y0 - 2, i + 1, c)
        s.text(x + 10, y0 + h - 10, sid, 11.5, True, tint(c, 0.25))
    hmax = max(hs)
    for i in range(n - 1):
        x = x0 + (i + 1) * (bw + gap) - gap + 2
        s.line([(x, y0 + 60), (x + gap - 5, y0 + 60)], "#333333", 2.0)
    # branch panel under stage 3
    by = y0 + hmax + 40
    sx = x0 + 2 * (bw + gap)
    s.line([(sx + bw / 2, y0 + hmax + 2), (sx + bw / 2, by - 4)], O, 1.6)
    s.rect(x0, by, W - 2 * x0, 186, O, rx=10, fill=tint(O, 0.96), shadow=False, dash="5 4")
    s.text(x0 + 14, by + 24, "Pick ONE primary branch from the data you have (README, Branches)", 14, True, O)
    br = [("S1 (default)", "RNA-seq + proteins, no close curated reference", "HISAT2 or STAR, StringTie, BRAKER4 + miniprot", O),
          ("S11", "Trusted curated annotation of the same species or cultivar", "Liftoff, LiftOn, CAT (lift-only = S11-lite)", R),
          ("S2", "Proteins only", "GALBA2, GeMoMa, miniprot", P),
          ("S3", "Deep long-read RNA (Iso-Seq or ONT)", "minimap2, IsoQuant, SQANTI3", B),
          ("S13", "GPU, want an ab initio comparison", "Helixer, Tiberius, ANNEVO (beside S1, not instead)", G),
          ("S14", "Classic multi-evidence stack", "PASA, AUGUSTUS or GeneMark, EVM", "#8A4C38")]
    cw = (W - 2 * x0 - 28 - 5 * 12) / 6
    for i, (nm, when, tools, c) in enumerate(br):
        x = x0 + 14 + i * (cw + 12)
        s.node(x, by + 38, cw, nm, [when, tools], c, tsize=14, bsize=11.5, align="start", min_h=128)
    s.text(x0 + 14, by + 182 + 0, "", 1)
    s.text(W - x0, H - 14, "Stage names and tools from README (Usage, Branches, Default route) and catalog/SOFTWARE_AUTHORITY.tsv roles.", 11, False, GR, "end")
    return s

# ---------- 2. branch decision ----------
def decision():
    W, H = 1320, 640
    s = SVG(W, H, "Which structural annotation branch to run")
    def q(x, y, w, t, c="#333333"):
        return s.node(x, y, w, t, [], c, tsize=14, align="middle")
    def leaf(x, y, w, t, lines, c):
        return s.node(x, y, w, t, lines, c, tsize=14.5, bsize=12, align="start")
    def lab(x, y, t, c="#333333"):
        s.text(x, y, t, 12.5, True, c, "middle")
    # Start
    s.node(470, 18, 380, "Assembly passed QC and is soft-masked (A0)", [], "#333333", tsize=14)
    s.line([(660, 52), (660, 78)], "#333333", 1.8)
    h = q(380, 80, 560, "Is there a trusted curated annotation of the same species or cultivar?")
    s.line([(940, 80 + h / 2), (998, 80 + h / 2)], R, 1.8); lab(968, 80 + h / 2 - 7, "yes", R)
    leaf(1000, 56, 300, "S11  Lift-over first", ["Liftoff (same or close species), LiftOn (adds protein alignments), CAT", "Check: a lift-only S11-lite set is not an L1 release"], R)
    s.line([(660, 80 + h), (660, 168)], "#333333", 1.8); lab(680, 80 + h + 22, "no")
    h2 = q(470, 170, 380, "Do you have RNA-seq for this genome?")
    s.line([(470, 170 + h2 / 2), (300, 170 + h2 / 2), (300, 238)], "#333333", 1.8); lab(385, 170 + h2 / 2 - 7, "yes")
    s.line([(850, 170 + h2 / 2), (1010, 170 + h2 / 2), (1010, 306)], "#333333", 1.8); lab(930, 170 + h2 / 2 - 7, "no")
    h3 = q(110, 240, 380, "Deep long-read RNA (Iso-Seq or ONT)?")
    s.line([(300, 240 + h3), (300, 270 + h3), (160, 270 + h3), (160, 300 + h3)], B, 1.8); lab(200, 262 + h3, "yes", B)
    s.line([(300, 270 + h3), (470, 270 + h3), (470, 300 + h3)], O, 1.8); lab(430, 262 + h3, "no", O)
    ly = 302 + h3
    leaf(20, ly, 290, "S3  Long-read transcripts", ["minimap2, IsoQuant, SQANTI3", "Check: SQANTI-style filters on isoforms"], B)
    leaf(330, ly, 300, "S1  Default route", ["HISAT2 or STAR, StringTie, BRAKER4 with miniprot protein hints", "Check: mono- to multi-exonic ratio after TSEBRA"], O)
    h4 = q(830, 308, 360, "Proteins of related species available?")
    s.line([(1010, 308 + h4), (1010, 338 + h4), (900, 338 + h4), (900, 368 + h4)], P, 1.8); lab(935, 330 + h4, "yes", P)
    s.line([(1010, 338 + h4), (1180, 338 + h4), (1180, 368 + h4)], GR, 1.8); lab(1150, 330 + h4, "no", GR)
    leaf(745, 370 + h4, 300, "S2  Proteins only", ["GALBA2, GeMoMa, miniprot", "Check: no UTR claims from protein evidence alone"], P)
    leaf(1065, 370 + h4, 240, "Collect evidence first", ["RNA-seq or related-species proteins (Usage, Step 1)"], GR)
    # side branches
    yb = 520
    s.rect(20, yb, W - 40, 96, "#6B6B6B", rx=10, fill="#F7F7F7", shadow=False, dash="5 4")
    s.text(34, yb + 22, "Run beside the primary draft, never as a silent replacement", 13.5, True, "#333333")
    side = [("S13  GPU ab initio comparison", "Helixer, Tiberius (trained on mammals), ANNEVO", G),
            ("S14  Classic multi-evidence stack", "PASA, AUGUSTUS or GeneMark, EVidenceModeler", "#8A4C38"),
            ("S4  Second haplotype", "Liftoff, SynGAP", S),
            ("Overlays  L2 / S7", "Paper or T2T bar (S5); plant NLR or tandem windows", "#A8127F")]
    cw = (W - 40 - 28 - 3 * 12) / 4
    for i, (t, l, c) in enumerate(side):
        s.node(34 + i * (cw + 12), yb + 32, cw, t, [l], c, tsize=13, bsize=11.5, align="start", min_h=54)
    return s

# ---------- 3. gene model and GFF3 ----------
def gene_model():
    W, H = 1320, 585
    s = SVG(W, H, "A gene model and its GFF3 rows")
    x0, x1 = 70, 1250; g0, g1 = 1000, 5400
    def X(p):
        return x0 + (p - g0) / (g1 - g0) * (x1 - x0)
    y = 50
    s.raw("<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" stroke=\"#333333\" stroke-width=\"2\"/>" % (x0 - 20, y, x1 + 20, y))
    s.text(x0 - 20, y - 12, "chr01 (soft-masked genome, plus strand)", 12.5, False, GR)
    for p in range(1000, 5401, 1000):
        s.raw("<line x1=\"%.1f\" y1=\"%d\" x2=\"%.1f\" y2=\"%d\" stroke=\"#333333\" stroke-width=\"1\"/>" % (X(p), y, X(p), y + 6))
        s.text(X(p), y + 20, "%d" % p, 11, False, GR, "middle")
    # gene
    gy = 104
    s.raw("<rect x=\"%.1f\" y=\"%d\" width=\"%.1f\" height=\"14\" fill=\"#333333\" rx=\"2\"/>" % (X(1200), gy, X(5100) - X(1200)))
    s.text(X(1200) - 8, gy + 11, "gene  ID=g1", 12.5, True, "#333333", "end")
    tx = {"mRNA  g1.t1": [(1200, 1500, "u"), (1500, 1900, "c"), (2600, 3100, "c"), (3900, 4500, "c"), (4500, 5100, "u")],
          "mRNA  g1.t2": [(1200, 1500, "u"), (1500, 1900, "c"), (3900, 4650, "c"), (4650, 5100, "u")]}
    ty = 152
    for name, ex in tx.items():
        s.raw("<line x1=\"%.1f\" y1=\"%d\" x2=\"%.1f\" y2=\"%d\" stroke=\"#6B6B6B\" stroke-width=\"1.4\"/>" % (X(ex[0][0]), ty, X(ex[-1][1]), ty))
        for a, b, k in ex:
            hh = 26 if k == "c" else 14
            col = PAL["blue"] if k == "c" else tint(PAL["blue"], 0.55)
            s.raw("<rect x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"%d\" fill=\"%s\" stroke=\"#1D5A8A\" stroke-width=\"0.8\"/>" % (X(a), ty - hh / 2, X(b) - X(a), hh, col))
        # intron chevrons
        segs = []
        for (a1, b1, k1), (a2, b2, k2) in zip(ex, ex[1:]):
            if a2 > b1:
                m = (X(b1) + X(a2)) / 2
                s.raw("<polyline points=\"%.1f,%d %.1f,%d %.1f,%d\" fill=\"none\" stroke=\"#6B6B6B\" stroke-width=\"1.4\"/>" % (X(b1), ty - 13, m, ty - 24, X(a2), ty - 13))
        s.text(X(1200) - 8, ty + 5, name, 12.5, True, PAL["blue"], "end")
        ty += 62
    # legend
    ly = 286
    s.raw("<rect x=\"%d\" y=\"%d\" width=\"30\" height=\"16\" fill=\"%s\" stroke=\"#1D5A8A\" stroke-width=\"0.8\"/>" % (x0, ly, PAL["blue"]))
    s.text(x0 + 38, ly + 13, "CDS (coding exon part)", 12.5)
    s.raw("<rect x=\"%d\" y=\"%d\" width=\"30\" height=\"9\" fill=\"%s\" stroke=\"#1D5A8A\" stroke-width=\"0.8\"/>" % (x0 + 230, ly + 4, tint(PAL["blue"], 0.55)))
    s.text(x0 + 268, ly + 13, "UTR (exon, not translated)", 12.5)
    s.raw("<polyline points=\"%d,%d %d,%d %d,%d\" fill=\"none\" stroke=\"#6B6B6B\" stroke-width=\"1.4\"/>" % (x0 + 470, ly + 14, x0 + 485, ly + 2, x0 + 500, ly + 14))
    s.text(x0 + 510, ly + 13, "intron", 12.5)
    s.text(x0 + 590, ly + 13, "Exon = UTR + CDS pieces of one transcript; g1.t2 skips the middle exon (alternative isoform).", 12.5, False, GR)
    # GFF3 table
    ty0 = 330
    cols = [("seqid", 70), ("source", 90), ("type", 140), ("start", 70), ("end", 70), ("score", 55), ("strand", 60), ("phase", 55), ("attributes (column 9)", 400)]
    rows = [("chr01", "BRAKER", "gene", "1200", "5100", ".", "+", ".", "ID=g1"),
            ("chr01", "BRAKER", "mRNA", "1200", "5100", ".", "+", ".", "ID=g1.t1;Parent=g1"),
            ("chr01", "BRAKER", "five_prime_UTR", "1200", "1499", ".", "+", ".", "Parent=g1.t1"),
            ("chr01", "BRAKER", "exon", "1200", "1900", ".", "+", ".", "Parent=g1.t1"),
            ("chr01", "BRAKER", "CDS", "1500", "1900", ".", "+", "0", "ID=g1.t1.cds;Parent=g1.t1"),
            ("chr01", "BRAKER", "exon", "2600", "3100", ".", "+", ".", "Parent=g1.t1"),
            ("chr01", "BRAKER", "CDS", "2600", "3100", ".", "+", "1", "ID=g1.t1.cds;Parent=g1.t1"),
            ("...", "", "", "", "", "", "", "", "more exon, CDS and UTR rows; g1.t2 has its own")]
    tot = sum(w for _, w in cols); tx0 = (W - tot) / 2
    s.rect(tx0 - 8, ty0 - 4, tot + 16, 28 + 22 * len(rows), "#6B6B6B", rx=6, fill="#FAFAFA", shadow=False)
    x = tx0
    for nm, w in cols:
        s.text(x + 4, ty0 + 16, nm, 12, True, "#333333"); x += w
    s.raw("<line x1=\"%.1f\" y1=\"%d\" x2=\"%.1f\" y2=\"%d\" stroke=\"#BFBFBF\" stroke-width=\"1\"/>" % (tx0, ty0 + 24, tx0 + tot, ty0 + 24))
    tcol = {"gene": "#333333", "mRNA": PAL["blue"], "exon": PAL["green"], "CDS": PAL["orange"], "five_prime_UTR": PAL["purple"]}
    for j, r in enumerate(rows):
        x = tx0; yy = ty0 + 42 + j * 22
        for k, ((nm, w), v) in enumerate(zip(cols, r)):
            c = tcol.get(r[2], "#333333") if k == 2 else ("#333333" if k != 8 else "#000000")
            s.raw("<text x=\"%.1f\" y=\"%.1f\" font-family=\"Liberation Mono, DejaVu Sans Mono, monospace\" font-size=\"12\" fill=\"%s\">%s</text>" % (x + 4, yy, c, v.replace("&", "&amp;")))
            x += w
    s.text(W / 2, ty0 + 28 + 22 * len(rows) + 26, "Each child row points to its parent with Parent=; CDS phase (0, 1, 2) says where the next codon starts. Toy coordinates, not a real locus.", 12.5, False, GR, "middle")
    return s

# ---------- 4. evidence combination ----------
def evidence():
    W, H = 1320, 560
    s = SVG(W, H, "How a combiner turns several evidence tracks into one gene model")
    x0, x1 = 300, 1290; g0, g1 = 0, 1000
    def X(p):
        return x0 + (p - g0) / (g1 - g0) * (x1 - x0)
    tracks = [
        ("RNA-seq alignments", "HISAT2 or STAR", O, [(60, 180), (300, 420), (560, 660)], "reads"),
        ("Assembled transcript", "StringTie / IsoQuant", O, [(60, 180), (300, 420), (560, 660)], "tx"),
        ("Protein alignment", "miniprot / ProtHint", P, [(90, 180), (300, 420), (560, 640)], "tx"),
        ("Ab initio prediction", "AUGUSTUS / GeneMark-ETP", B, [(90, 180), (300, 420), (480, 520), (560, 640)], "tx"),
        ("Deep-learning prediction", "Helixer", G, [(90, 180), (300, 420), (560, 640), (760, 880)], "tx"),
        ("Lift-over from a reference", "Liftoff / LiftOn", R, [(90, 180), (300, 420), (560, 640)], "tx"),
    ]
    y = 40
    s.text(20, 24, "Evidence for one locus", 13.5, True, "#333333")
    for name, tool, c, ex, kind in tracks:
        s.text(20, y + 14, name, 13, True, c)
        s.text(20, y + 30, tool, 11.5, False, GR)
        if kind == "reads":
            import random
            rnd = random.Random(7)
            for a, b in ex:
                for k in range(7):
                    ra = a + rnd.randint(-10, 30); rb = min(b + rnd.randint(-30, 10), ra + 70)
                    s.raw("<rect x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"3.2\" fill=\"%s\"/>" % (X(ra), y + 6 + k * 4.4, X(rb) - X(ra), tint(c, 0.25)))
            # spliced reads
            for (a1, b1), (a2, b2) in zip(ex, ex[1:]):
                s.raw("<polyline points=\"%.1f,%.1f %.1f,%.1f\" stroke=\"%s\" stroke-width=\"1\" fill=\"none\"/>" % (X(b1 - 15), y + 37, X(a2 + 15), y + 37, c))
        else:
            s.raw("<line x1=\"%.1f\" y1=\"%.1f\" x2=\"%.1f\" y2=\"%.1f\" stroke=\"%s\" stroke-width=\"1.3\"/>" % (X(ex[0][0]), y + 20, X(ex[-1][1]), y + 20, tint(c, 0.3)))
            for a, b in ex:
                s.raw("<rect x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"18\" fill=\"%s\" stroke=\"%s\" stroke-width=\"0.8\"/>" % (X(a), y + 11, X(b) - X(a), tint(c, 0.35), c))
        y += 52
    # annotations
    s.text(X(500), 40 + 3 * 52 - 4, "extra exon (one source only)", 11.5, False, B, "middle")
    s.text(X(820), 40 + 4 * 52 - 4, "neighbouring gene fused in", 11.5, False, G, "middle")
    # combiner band
    cy = y + 8
    s.rect(20, cy, W - 40, 62, "#333333", rx=10, fill="#F4F4F4", shadow=False)
    s.text(36, cy + 25, "Combiner", 14, True, "#333333")
    s.text(36, cy + 45, "weights the tracks and keeps the structure most evidence supports", 12, False, GR)
    opts = [("EVidenceModeler", "weighted consensus (S14 / A4)"), ("TSEBRA", "chooses among BRAKER transcripts"), ("Mikado", "picks the best transcript per locus"), ("PASA update", "adds UTRs and isoforms")]
    ox = 520
    for t, d in opts:
        w = max(tw(t, 12.5, True), tw(d, 11)) + 20
        s.rect(ox, cy + 10, w, 42, "#333333", rx=6, fill="#FFFFFF", shadow=False)
        s.text(ox + w / 2, cy + 27, t, 12.5, True, "#333333", "middle")
        s.text(ox + w / 2, cy + 44, d, 11, False, GR, "middle")
        ox += w + 10
    s.line([(X(370), cy + 62), (X(370), cy + 88)], "#333333", 2)
    fy = cy + 96
    s.text(20, fy + 14, "Consensus gene model", 13, True, "#000000")
    s.text(20, fy + 30, "then QC: BUSCO, OMArk, PSAURON", 11.5, False, GR)
    ex = [(90, 180), (300, 420), (560, 640)]
    s.raw("<line x1=\"%.1f\" y1=\"%.1f\" x2=\"%.1f\" y2=\"%.1f\" stroke=\"#333333\" stroke-width=\"1.5\"/>" % (X(60), fy + 20, X(660), fy + 20))
    for a, b in [(60, 90)] + ex + [(640, 660)]:
        hh = 22 if (a, b) in ex else 12
        s.raw("<rect x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"%d\" fill=\"%s\" stroke=\"#000000\" stroke-width=\"0.8\"/>" % (X(a), fy + 20 - hh / 2, X(b) - X(a), hh, "#333333" if (a, b) in ex else "#9A9A9A"))
    s.text(X(700), fy + 25, "UTRs from transcripts; CDS agreed by protein and predictors", 11.5, False, GR)
    s.text(W - 20, H - 12, "Schematic (toy locus, not real data). Combiner roles as described in README section 8 and book chapter 9.", 11, False, GR, "end")
    return s

figs = {"structure_route_map": route_map, "structure_branch_decision": decision, "structure_gene_model_gff3": gene_model, "structure_evidence_combination": evidence}
for name, fn in figs.items():
    s = fn()
    ov = s.save(os.path.join(OUT, name + ".svg"))
    print(name, s.w, s.h, "overflow:", ov)
