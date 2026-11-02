---
id: mdn-javascript-regular-expressions
title: "MDN: JavaScript regular expressions (patterns, escaping, methods, flags)"
publisher: "MDN Web Docs (Mozilla contributors)"
url: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions
licence: CC-BY-SA-2.5
licence_url: https://github.com/mdn/content/blob/d6b230abd1d23d02c6641727ddcbf5095082fdd0/LICENSE.md
retrieved: 2026-11-02
kind: excerpt
repo: mdn/content
path: files/en-us/web/javascript/guide/regular_expressions/index.md
commit: d6b230abd1d23d02c6641727ddcbf5095082fdd0
topics: [text-search, regex, javascript, pattern-matching]
---
> Excerpt from "Regular expressions" (JavaScript Guide), MDN Web Docs, by Mozilla Contributors. Original: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions ; source file `files/en-us/web/javascript/guide/regular_expressions/index.md` in https://github.com/mdn/content at commit d6b230abd1d23d02c6641727ddcbf5095082fdd0. Retrieved 2026-11-02.
> Prose is licensed under CC BY-SA 2.5 (https://creativecommons.org/licenses/by-sa/2.5/; see LICENSE.md in the repository); code examples added on or after 20 August 2010 are public domain (CC0). Changes made: trimmed ("[…]" marks cuts); documentation macros and relative links reduced to plain text. Share-alike: any adaptation of the prose must be released under CC BY-SA or a compatible licence.

Regular expressions are patterns used to match character combinations in strings.
In JavaScript, regular expressions are also objects. These patterns are used with the exec() and test() methods of RegExp, and with the match(), matchAll(), replace(), replaceAll(), search(), and split() methods of String.
This chapter describes JavaScript regular expressions. It provides a brief overview of each syntax element. For a detailed explanation of each one's semantics, read the regular expressions reference.

## Creating a regular expression

You construct a regular expression in one of two ways:

- Using a regular expression literal, which consists of a pattern enclosed between slashes, as follows:

  ```js
  const re = /ab+c/;
  ```

  Regular expression literals provide compilation of the regular expression when the script is loaded.
  If the regular expression remains constant, using this can improve performance.

- Or calling the constructor function of the RegExp object, as follows:

  ```js
  const re = new RegExp("ab+c");
  ```

  Using the constructor function provides runtime compilation of the regular expression.
  Use the constructor function when you know the regular expression pattern will be changing, or you don't know the pattern and are getting it from another source, such as user input.

## Writing a regular expression pattern

A regular expression pattern is composed of simple characters, such as `/abc/`, or a combination of simple and special characters, such as `/ab*c/` or `/Chapter (\d+)\.\d*/`.
The last example includes parentheses, which are used as a memory device.
The match made with this part of the pattern is remembered for later use, as described in Using groups.

### Using simple patterns

Simple patterns are constructed of characters for which you want to find a direct match. For example, the pattern `/abc/` matches character combinations in strings only when the exact sequence `"abc"` occurs (all characters together and in that order).
Such a match would succeed in the strings `"Hi, do you know your abc's?"` and `"The latest airplane designs evolved from slabcraft."`.
In both cases the match is with the substring `"abc"`.
There is no match in the string `"Grab crab"` because while it contains the substring `"ab c"`, it does not contain the exact substring `"abc"`.

[…]

### Escaping

If you need to use any of the special characters literally (actually searching for a `"*"`, for instance), you should escape it by putting a backslash in front of it. For instance, to search for `"a"` followed by `"*"` followed by `"b"`, you'd use `/a\*b/` — the backslash "escapes" the `"*"`, making it literal instead of special.

> [!NOTE]
> In many cases, when trying match a special character, you can wrap it in a character class as an alternative to escaping, for example `/a[*]b/`.

Similarly, if you're writing a regular expression literal and need to match a slash ("/"), you need to escape that (otherwise, it terminates the pattern).
For instance, to search for the string "/example/" followed by one or more alphabetic characters, you'd use `/\/example\/[a-z]+/i`—the backslashes before each slash make them literal.

To match a literal backslash, you need to escape the backslash.
For instance, to match the string "C:\\" where "C" can be any letter, you'd use `/[A-Z]:\\/` — the first backslash escapes the one after it, so the expression searches for a single literal backslash.

If using the `RegExp` constructor with a string literal, remember that the backslash is an escape in string literals, so to use it in the regular expression, you need to escape it at the string literal level.
`/a\*b/` and `new RegExp("a\\*b")` create the same expression, which searches for "a" followed by a literal "\*" followed by "b".

The RegExp.escape() function returns a new string where all special characters in regex syntax are escaped. This allows you to do `new RegExp(RegExp.escape("a*b"))` to create a regular expression that matches only the string `"a*b"`.

[…]

## Using regular expressions in JavaScript

Regular expressions are used with the RegExp methods test() and exec() and with the String methods match(), matchAll(), replace(), replaceAll(), search(), and split().

| Method | Description |
| --- | --- |
| exec() | Executes a search for a match in a string. It returns an array of information or `null` on a mismatch. |
| test() | Tests for a match in a string. It returns `true` or `false`. |
| match() | Returns an array containing all of the matches, including capturing groups, or `null` if no match is found. |
| matchAll() | Returns an iterator containing all of the matches, including capturing groups. |
| search() | Tests for a match in a string. It returns the index of the match, or `-1` if the search fails. |
| replace() | Executes a search for a match in a string, and replaces the matched substring with a replacement substring. |
| replaceAll() | Executes a search for all matches in a string, and replaces the matched substrings with a replacement substring. |
| split() | Uses a regular expression or a fixed string to break a string into an array of substrings. |

When you want to know whether a pattern is found in a string, use the `test()` or `search()` methods; for more information (but slower execution) use the `exec()` or `match()` methods.
If you use `exec()` or `match()` and if the match succeeds, these methods return an array and update properties of the associated regular expression object and also of the predefined regular expression object, `RegExp`.
If the match fails, the `exec()` method returns `null` (which coerces to `false`).

[…]

### Advanced searching with flags

Regular expressions have optional flags that allow for functionality like global searching and case-insensitive searching.
These flags can be used separately or together in any order, and are included as part of the regular expression.

| Flag | Description | Corresponding property |
| --- | --- | --- |
| `d` | Generate indices for substring matches. | hasIndices |
| `g` | Global search. | global |
| `i` | Case-insensitive search. | ignoreCase |
| `m` | Makes `^` and `$` match the start and end of each line instead of those of the entire string. | multiline |
| `s` | Allows `.` to match newline characters. | dotAll |
| `u` | "Unicode"; treat a pattern as a sequence of Unicode code points. | unicode |
| `v` | An upgrade to the `u` mode with more Unicode features. | unicodeSets |
| `y` | Perform a "sticky" search that matches starting at the current position in the target string. | sticky |

[…]

For example, `re = /\w+\s/g` creates a regular expression that looks for one or more characters followed by a space, and it looks for this combination throughout the string.

```js
const re = /\w+\s/g;
const str = "fee fi fo fum";
const myArray = str.match(re);
console.log(myArray);

// ["fee ", "fi ", "fo "]
```
