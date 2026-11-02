Build the app. Concepts with synonym terms: mental privacy ["mental privacy"], freedom of thought ["freedom of thought"], self-incrimination ["self-incrimination"], lie detection ["lie detection","deception detection","brain fingerprinting"], consent ["consent"], neural data ["neural data"], data solidarity ["data solidarity"], proportionality ["proportionality"]. Case-insensitive, ignore line breaks (replace \n with space before matching).

Citation for journal articles: surnames. Szoszkiewicz-Yuste: "Szoszkiewicz & Yuste 2025, p. 3471". Prainsack-et-al: "Prainsack et al. 2022, p. N". Detect kind === "Journal article", take author surnames split by " and ". Prainsack author field likely "Barbara Prainsack and others" or similar — I don't know. Safer: parse author string, split on " and "/"&", take last token of each name; if more than 2 names → first surname + " et al.". Fallback to author as written.

Groups in library order. Passages match if any term found in text (case-insensitive, line breaks normalized).

Draft summary: first 12 passages, prompt with citations and text, ask three sentences each ending with citation. Button hidden if no passages. data-source="ai" box.

Related concepts: for passages matching current concept, which other concepts' terms also appear.

Keep under 700 lines. Write single HTML.