# Design QA — selected course design, 2026-10-15

## Authoritative visual reference

The user's final selection is the image ending `a5ba763a-0698-4201-93cc-2b785d59327b.png`, copied to `artifacts/selected-build/reference.png`. It supersedes earlier alternatives. Implementation uses a white school masthead, pale blue sidebar, numbered curriculum, large navy/teal title, three-paper illustration, four course steps and three starting PDF cards. The original official school logo is used in the masthead. The generated decorative illustration is separate from the HTML interface.

Same-viewport comparison: `artifacts/selected-build/comparison-final.jpg`, reference on the left and implementation on the right. Browser viewport 1487 × 1058. The 1472 × 1047 captured content was proportionally normalized to the reference dimensions for comparison. Final desktop evidence also includes `home-final.jpg`, `home-1280.jpg`, `materials-final.jpg` and `workflow-final.jpg` in that directory.

## Visual corrections

- Fixed P2: heading scale and empty margin around the illustration differed from the selected source. Adjusted typography and regenerated/reframed the separate illustration.
- Fixed P2: enlarged sidebar text wrapped two curriculum labels. Adjusted link spacing and desktop typography, preserving one-line labels.
- Fixed P2: laptop sidebar had internal horizontal overflow. Added compact desktop link spacing and checked at 1280 × 720.
- Fixed P2: earlier guide navigation replaced the main curriculum. Six primary entries now remain available, with detailed steps in a collapsed outline.
- Theory, materials, tools, skills, request form and document review share the selected header, sidebar and palette. Added teaching document downloads are below the main reference composition and in the materials view.

## Functional checks

- First lesson opens the four theory tabs; previous/next and the final link lead to preparation.
- Six main curriculum links open their intended routes. Guide top next advances the step; both next controls are disabled at 17/17.
- Materials show 11 sources; 개인정보 search returns one. Skills show nine items; 한글 search returns two, and the usage dialog opens and closes.
- Tool comparison changes to Claude. Request generation includes entered data and enables copying and TXT saving. Clipboard content and the downloaded TXT were checked.
- PDF download succeeds and its public copy matches the local deliverable. The Word download link was subsequently removed at the user's request; the existing lesson plan is preserved.
- At desktop widths 1487 and 1280 there is no document horizontal overflow. Desktop is the user's confirmed surface; additional mobile polish is outside this iteration.
- Current application console error log is empty.
- Static checker passes: 105 local references, 5 tools, 9 skills, 11 public sources, continuous 120-minute timetable.

## Document verification

- Word lesson plan: two Letter pages, black headings, readable tables and no isolated spill page. Bundled render_docx.py reported missing LibreOffice. Installed Microsoft Word exported the actual DOCX to PDF; all pages were then rasterized and inspected.
- Lecture PDF: 41 landscape 16:9 pages; all pages rendered and visually reviewed. Text bounds are inside the page. Second page contains the actual portrait extracted from the supplied resume and reviewed professional facts. Private contact details from the resume are absent.
- Longest screenshot instruction had little space before its result heading; increased spacing and reviewed the corrected page.
- Both QR codes, on pages 1 and 41, decode from rendered PDF pages to `https://zeusk302-png.github.io/teacher-ai-workshop/`.
- Screenshots 0, 15 and 16 show the current site. Service screenshots remain the originals dated 2026.10.14. Fictional example input is labelled as an example rather than a regulation quote.
- Budget exercise retains the CSV's original columns and adds amounts in F, with total 400,000 and a fictional 500,000 ceiling giving 100,000 difference.

## Scope

This verifies the local website and generated teaching documents. Actual participant learning, external AI account functionality, and learner-created Office files were not evaluated. Design preference remains the user's judgment. Public deployment evidence is recorded separately after deployment.

final result: passed

## RAG teaching update — 2026-10-18

- Preserved the selected home composition, logo and navigation. Expanded theory to six tabs covering the RAG pipeline, own-system resources, division of work, handoff contents and review.
- Explained text extraction/OCR, indexing, optional embedding/vector retrieval, model/API access, orchestration and operations. A dedicated vector database, model retraining and an on-site GPU are not presented as universal requirements.
- Mapped source search and instruction preparation to NotebookLM, document creation to an external AI with file tools and a template, and copy/attachment/review to the participant. The workflow is not described as an automatically connected RAG backend.
- Added the limits of the actual 2026-10-18 browser test: Claude Pro, PDF form rebuilt as DOCX, fictional case, no verified HWPX fidelity or free-account run.
- Rebalanced the continuous 120-minute plan to nine blocks, including five minutes of source/template preparation and a separate revision exercise. The PDF reads this same timetable from data.js. Prior seven-block progress uses a separate storage key.
- Local Chrome: all six tabs, counter, one visible panel, final practice link and keyboard Home verified. No page horizontal overflow on the current desktop viewport. New theory and schedule screenshots are in artifacts/rag-theory-2026-10-18/.
- Rebuilt the lecture PDF to 43 landscape pages. Reviewed all-page contact sheets and full-resolution changed pages 3, 9, 10 and 11; text remains above the footer. Pages 1 and 43 decode to the public course URL. Page 2 retains the instructor introduction.
- Static validation: 106 local references, five tools, nine skills, 11 unchanged public sources and 120 continuous minutes. The checker now recognizes valid PDF page fragments.
- These checks cover the local implementation and rendered course PDF; classroom pacing remains a plan. Public build and byte-verification results follow deployment.
