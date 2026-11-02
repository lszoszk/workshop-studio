---
id: wikipedia-help-searching-operators
title: "Wikipedia Help:Searching: exact phrase, exclusion, wildcards, AND / OR / NOT and field operators"
publisher: "Wikipedia contributors (Wikimedia Foundation)"
url: https://en.wikipedia.org/w/index.php?title=Help:Searching&oldid=1379184667
licence: CC-BY-SA-4.0
licence_url: https://creativecommons.org/licenses/by-sa/4.0/
retrieved: 2026-11-02
kind: excerpt
topics: [text-search, boolean-operators, query-syntax, search-ui]
---
> Text from the Wikipedia help page "Help:Searching", revision 1379184667, by Wikipedia contributors (authors: https://en.wikipedia.org/w/index.php?title=Help:Searching&action=history). Original: https://en.wikipedia.org/w/index.php?title=Help:Searching&oldid=1379184667. Retrieved 2026-11-02.
> Licensed under the Creative Commons Attribution-ShareAlike 4.0 licence (https://creativecommons.org/licenses/by-sa/4.0/). Changes made: trimmed ("[…]" marks cuts); headings converted to Markdown. The page describes the syntax of Wikipedia's own search box (a Boolean-style engine); other search tools differ in detail, for example in whether OR needs capital letters. Share-alike: any adaptation of this text must be released under CC BY-SA 4.0 or a compatible licence.

## Search string syntax
Search is case insensitive, that is, upper and lowercase is ignored.
Search "folds" character families, matching similar-looking letters across alphabets, to match foreign terms. So, you don't have to type in diacritical letters, and your terms will still match. For example, a search on Citroen will also match Citroën, and Aeroskobing matches Ærøskøbing.
Characters that are not numbers or letters (punctuation marks, brackets and slashes, math and other symbols) are generally ignored. For example, Credit (finance) will return articles with the words credit and finance, ignoring the parentheses, unless an article with exact title Credit (finance) exists. Similarly, a search for the string |LT| (letters LT between two pipe symbols) will only return articles with lt. In order to search for terms that contain non-alphanumeric characters, a regex search must be used instead (using the \ escape character if required); for example, insource:/\|LT\|/ will successfully return all instances of |LT|.

[…]

### Special characters

For regex searches, see the insource: parameter below.

#### Double quotes for exact phrase search
A phrase can be matched by enclosing it in double quotes, "like this". Double quotes can define a single search term that contains spaces. For example, "holly dolly" where the space is quoted as a character, differs much from holly dolly where the space is interpreted as a logical AND.

#### Suffixed tilde character for fuzzy search
Spelling relaxation is requested by suffixing a tilde ~, like this~ to match results like thus and thins. It covers any two character-changes for any character except the first: it returns addition, exchange, or subtraction. This search technique is sometimes called a "sounds-like" search. For example, searching for charlie~ parker~ returns Charlie Parker, Charles Palmer, Charley Parks, etc.

[…]

#### Prefixed hyphen or exclamation point for exclusion
Pages matching a search term can be excluded by prefixing an exclamation point (!) or a hyphen (-) to the term. This is the logical NOT. For example, credit card -"credit card" finds all articles with credit and card except those with the phrase credit card.

#### Wildcard characters
The two wildcard characters are * and \?, and both can come in the middle or end of a word. The escaped question mark stands for one character and the star stands for any number of characters. Because many users ask questions when searching, question marks are ignored by default, and the escaped question mark (\?) must be used for a wildcard.

[…]

#### Logical operators
The search engine supports limited boolean logic in searches. Logical NOT (negation) can be indicated by a "-" (minus sign) or a "!" (exclamation point) character prefixed to a search term, or by the NOT keyword.
Parentheses (…) are ignored by the search engine and have no effect.
Search terms are implicitly joined by logical AND (conjunction). For example "credit card" housecat searches for pages containing both "credit card" and "housecat". An OR operator is supported, but will only give intuitive results (corresponding to logical disjunction) if all search terms are separated by OR (e.g. red OR green OR blue has the expected behaviour, but red OR green blue does not). OR also does not behave predictably with special keywords (like intitle:) or namespaces. (See mw:Help:CirrusSearch/Logical operators for a more detailed explanation.)

[…]

#### intitle:
Page titles and redirects can be searched with intitle:query, where query is the search string. The search results highlight occurrences in both the title and page content. Multiple intitle: filters may be used to search for words in titles regardless of order, or in different titles (i.e., redirects) for the same article. Regular expressions can be used with intitle:/regexp/ or the case insensitive intitle:/regexp/i. (See more in the insource section.)

#### insource:
This can find template arguments, URLs, links, html, etc. It has two forms, one is an indexed search, and the other is regex-based.
