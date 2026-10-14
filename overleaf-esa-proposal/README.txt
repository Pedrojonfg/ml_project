Overleaf / Turnitin package — ESA Collision Avoidance proposal
==============================================================

Contents
--------
main.tex                 Proposal body (clean mode)
bam-proposal.cls         Template-matched class (IE header, BAMblue headings)
references.bib           Bibliography
figures/*.pdf            Three proposal figures (PNG copies included)
figures/ie-logo.png      IE logo extracted from the official annotated template

Before upload / submit
----------------------
1. OPTIONAL: if Blackboard/Overleaf gave you the official IE bam-proposal.cls,
   REPLACE the cls in this folder with the official file (same filename).
   Keep main.tex / bib / figures (logo may already be in the official cls).
2. Compile with pdfLaTeX (+ BibTeX / second pass if references show as [?]).
3. Check that proposal TEXT is ≤ 2 pages (figures do not count).

Overleaf
--------
New Project → Upload Project → upload
  `esa-collision-proposal-overleaf.zip`
or re-upload the updated files into the existing project.

Local compile
-------------
  pdflatex main && bibtex main && pdflatex main && pdflatex main
