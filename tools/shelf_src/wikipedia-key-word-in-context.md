---
id: wikipedia-key-word-in-context
title: "Wikipedia: Key Word in Context (KWIC) and permuted indexes"
publisher: "Wikipedia contributors (Wikimedia Foundation)"
url: https://en.wikipedia.org/w/index.php?title=Key_Word_in_Context&oldid=1368354439
licence: CC-BY-SA-4.0
licence_url: https://creativecommons.org/licenses/by-sa/4.0/
retrieved: 2026-11-02
kind: excerpt
topics: [text-search, kwic, concordance, snippets, search-ui]
---
> Text of the Wikipedia article "Key Word in Context", revision 1368354439 of 8 August 2026, by Wikipedia contributors (authors: https://en.wikipedia.org/w/index.php?title=Key_Word_in_Context&action=history). Original: https://en.wikipedia.org/w/index.php?title=Key_Word_in_Context&oldid=1368354439. Retrieved 2026-11-02.
> Licensed under the Creative Commons Attribution-ShareAlike 4.0 licence (https://creativecommons.org/licenses/by-sa/4.0/). Changes made: trimmed ("[…]" marks cuts), converted from wiki markup to plain Markdown, the example index shown as a Markdown table, a quoted passage and the reference list omitted. Share-alike: any adaptation of this text must be released under CC BY-SA 4.0 or a compatible licence.

# Key Word in Context

Key Word in Context (KWIC) is the most common format for concordance lines. The term KWIC was coined by Hans Peter Luhn. The system was based on a concept called keyword in titles, which was first proposed for Manchester libraries in 1864 by Andrea Crestadoro.

A KWIC index is formed by sorting and aligning the words within an article title to allow each word (except the stop words) in titles to be searchable alphabetically in the index. It was a useful indexing method for technical manuals before computerized full text search became common.

For example, a search query including all of the words in an example definition ("KWIC is an acronym for Key Word in Context, the most common format for concordance lines") and the Wikipedia slogan in English ("the free encyclopedia"), searched against a Wikipedia page, might yield a KWIC index as follows. A KWIC index usually uses a wide layout to allow the display of maximum 'in context' information (not shown in the following example).

| Left context | Keyword | Page |
|---|---|---:|
| KWIC is an | **acronym** for Key Word in Context, ... | page 1 |
| ... Key Word in Context, the most | **common** format for concordance lines. | page 1 |
| ... the most common format for | **concordance** lines. | page 1 |
| ... is an acronym for Key Word in | **Context**, the most common format ... | page 1 |
| Wikipedia, The Free | **Encyclopedia** | page 0 |
| ... in Context, the most common | **format** for concordance lines. | page 1 |
| Wikipedia, The | **Free** Encyclopedia | page 0 |
| KWIC is an acronym for | **Key** Word in Context, the most ... | page 1 |
|  | **KWIC** is an acronym for Key Word ... | page 1 |
| ... common format for concordance | **lines**. | page 1 |
| ... for Key Word in Context, the | **most** common format for concordance ... | page 1 |
|  | **Wikipedia**, The Free Encyclopedia | page 0 |
| KWIC is an acronym for Key | **Word** in Context, the most common ... | page 1 |

A KWIC index is a special case of a permuted index. This term refers to the fact that it indexes all cyclic permutations of the headings. Books composed of many short sections with their own descriptive headings, most notably collections of manual pages, often ended with a permuted index section, allowing the reader to easily find a section by any word from its heading. This practice, also known as Key Word Out of Context (KWOC), is no longer common.

[…]

## References in literature

David L. Parnas uses a KWIC index as an example on how to perform modular design in his paper On the Criteria To Be Used in Decomposing Systems into Modules, available as an ACM Classic Paper

Christopher D. Manning and Hinrich Schütze describe a KWIC index and computer concordancing in section 1.4.5 of their book Foundations of Statistical Natural Language Processing. Cambridge, Mass: MIT Press, 1999. ISBN 9780262133609. They cite an article from H.P. Luhn from 1960, "Key word-in-context index for technical literature (kwic index)".

[…]

## See also

- ptx, a Unix command-line utility producing a permuted index
- Concordancer
- Burrows–Wheeler transform
- Suffix tree
