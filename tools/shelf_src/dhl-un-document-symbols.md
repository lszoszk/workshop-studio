---
id: dhl-un-document-symbols
title: "Dag Hammarskjöld Library research guide: structure of UN document symbols (summary)"
publisher: "United Nations Dag Hammarskjöld Library"
url: https://research.un.org/en/docs/symbols
licence: summary
licence_url: https://www.un.org/en/about-us/copyright
retrieved: 2026-11-02
kind: summary
topics: [un-documents, document-symbols, citation, metadata, parsing, research-guides]
---
> Summary of the page "UN Document Symbols" in the research guide "About UN Documents", United Nations Dag Hammarskjöld Library (page showed "Updated Oct 12, 2026"). Original: https://research.un.org/en/docs/symbols . Retrieved 2026-11-02.
> No open licence for this page could be confirmed (the footer links to the UN copyright page, https://www.un.org/en/about-us/copyright, which refused automated access). This page is an original summary; the tables of the original are not reproduced.

## Summary written for the workshop

A UN document symbol is a code of letters, numbers and slashes that identifies a document. The guide explains it as a sequence of parts, read from left to right. Knowing the parts lets an app split a symbol into fields, validate it, or guess what kind of document it names.

**1. First part: the organ or body that issues the document.** The common prefixes are A for the General Assembly, S for the Security Council, E for the Economic and Social Council and ST for the Secretariat. Some bodies have their own series that does not show the parent organ; the guide gives CRC/C for the Committee on the Rights of the Child, DP for the UN Development Programme, TD for UNCTAD and UNEP for the UN Environment Programme.

**2. Next parts: subsidiary bodies.** Letter groups after the first slash mark the kind of subsidiary body: ad hoc committee (AC), standing or main committee (C), commission (CN), conference (CONF), governing council (GC), preparatory committee (PC), subcommittee (SC), subcommission (Sub) and working group (WG).

**3. Special parts: the nature of the document.** Examples: CRP (conference room paper), INF (information series such as lists of participants), L (limited distribution, usually drafts), NGO (statements by non-governmental organizations), PET (petitions), PRST (statements by the President of the Security Council), PV (verbatim records of meetings), R (restricted distribution), RES (resolutions), SR (summary records of meetings) and WP (working papers).

**4. Final part: changes to the original text.** Add (addendum), Amend (amendment), Corr (corrigendum, which may not exist in every language), Rev (revision replacing earlier versions), Summary (a summarised version), and a trailing asterisk when a document is reissued for technical reasons.

**5. Extra parts in brackets.** When a meeting is suspended and resumed, the record can carry a note such as Resumption or Resumed, written in parentheses.

**6. Session or year.** Many symbols include a session number or a year after the body parts. The General Assembly has put the session into all symbols since 1976 (the guide's example is A/31/99 for the 31st session). The Security Council and the Economic and Social Council use the year (S/1994/99 and E/1978/99 are the guide's examples). Before 1976 the session usually appeared only for resolutions, in Roman numerals in parentheses. Subsidiary bodies generally follow the practice of their parent organ.

**More detail.** For an exhaustive list of series symbols the guide refers to the Library's publication ST/LIB/SER.B/5/Rev.5, "United Nations Document Series Symbols, 1946-1996".

## Notes for a citation finder or parser

- Split on "/" and keep the ordered list of parts; do not assume a fixed number of parts. Resolutions follow the pattern body, RES, session and number (for example A/RES/70/1 is the General Assembly resolution that adopted the 2030 Agenda, as cited in the OHCHR data note on this shelf).
- Parentheses, asterisks and suffixes such as Rev.1 or Corr.1 belong to the same document family but are different versions: keep them as separate fields and link versions to a base symbol.
- The prefix of a treaty-body symbol varies by body (the guide shows only CRC/C as an example), so check a symbol against an official source rather than against a pattern list built from memory.
- Always keep the original string exactly as found, in addition to any parsed fields.
