---
id: uk-af-qa-code-testing
title: "Quality assurance of code for analysis and research: Testing code"
publisher: "UK Government Analysis Function (Analytical Standards and Pipelines hub)"
url: https://github.com/best-practice-and-impact/qa-of-code-guidance/blob/fa39f2089905fe07c08ae4d66671736a1becd3c5/book/testing_code.md
licence: OGL-3.0
licence_url: https://github.com/best-practice-and-impact/qa-of-code-guidance/blob/fa39f2089905fe07c08ae4d66671736a1becd3c5/LICENCE
retrieved: 2026-11-02
kind: excerpt
repo: best-practice-and-impact/qa-of-code-guidance
path: book/testing_code.md
commit: fa39f2089905fe07c08ae4d66671736a1becd3c5
topics: [quality-assurance, testing, validation, python, reproducibility]
---
> Excerpt from `book/testing_code.md` in https://github.com/best-practice-and-impact/qa-of-code-guidance at commit fa39f2089905fe07c08ae4d66671736a1becd3c5, part of "Quality Assurance of Code for Analysis and Research", Analysis Function, Analytical Standards and Pipelines hub. Crown copyright 2020; repository file LICENCE. Retrieved 2026-11-02.
> Contains public sector information licensed under the Open Government Licence v3.0.
> Trimmed; "[…]" marks cuts. Documentation-site (MyST) markup is simplified.

# Testing code

Code documentation helps others to understand what you expect your code to do and how to use it. Code tests verify that your analytical code is working as expected.  

You cannot confirm your code works correctly if you don’t carry out tests, so you cannot be confident that your analysis is fit for purpose without them.  
Good tests tell a story - given this data, having run this code, we expect this output.  

Testing brings strong benefits. It helps you assure your code quality and makes developing your code more efficient.
Code that has not been tested is more likely to contain errors and need more maintenance in the future.

## What should I test?

The question you need to answer here is a simple one:    

How can I demonstrate that my code does what it is supposed to do?    

As the developer of the code, you are best placed to decide what tests you need to put in place to answer that question confidently.

Take a risk-based approach to testing. You should use tests proportionately based on your analysis.  This usually means writing more tests for parts of your code that are very new, more complex, or carry more risk.  

When you are developing your tests, here are some points to think about:    

1.  You don't need to test everything. It is realistic to assume that third party functions and tools which are adequately quality assured (and you can verify this) work as intended.  For example, if you use R you would not expect to write tests to verify that simple arithmetic, base R, or packages published on [CRAN](https://cran.r-project.org/) operate correctly, because there is already sufficient assurance. You may be less confident about very new functionality from third parties, or experimental tools. Here, you might decide you do need to do some extra validation.    
2. Think carefully about whether third party tools really do what you need for your particular context.  For example, the base R `round()` function intentionally behaves differently to the rounding function in Excel. While we can be confident that `round()` works as specified, does it produce what you need?
3. Testing is a great way to verify that your approach is the right one. By thinking about what to test, you challenge your own assumptions and the way you have done things. This can reveal issues or scenarios that you had not considered. It means the code you write should be more resilient.
4. Be guided by the risks you need to mitigate. For example, if inputs are invalid or unusual, do you want the code to stop with an error message or do something else? Use tests to check that the code does the right thing at the right time. 

## How are tests structured?

Tests come in many shapes and sizes, but usually follow the pattern:

1. Arrange - set up any objects needed for your test, for example sample input data and expected output data.
2. Act - run the code that you are testing (one or more functions or methods).
3. Assert - verify that the code performed the expected action, for example, that the output matched the expected output.

[…]

## Write reproducible tests

As an analyst, you routinely check that your analysis is carried out correctly.
You might do this informally by running all or part of your analysis with example data or subsets of real data.

These tests give you confidence that your analysis is correct.
However, it's important you are able to produce the same checks against your code reproducibly.
Code changes over time, so you need to be able to repeat these checks against the updated code.
Additionally, other analysts should be able to carry out the same checks and get the same results.

You can consistently repeat the same steps when you represent your tests as code.
This lets you or another analyst carry out the same verification again to get the same results.
When you have carried out a test manually, you should ensure that you add a code test to reproduce this.

Code that you write for testing should also follow the good practices described earlier on in this book, in particular the "Readable code" chapter.

[…]

## Write tests to assure that bugs are fixed

Each time you find a bug in your code, you should write a new test to assert that the code works correctly.
Once you resolve the issue, this new test should pass and give you confidence that the bug has been fixed.

When you change or refactor your code in future, the new tests
will continue to assure that bugs you have already fixed will not reappear.
Doing this increases the coverage of your tests in a proportionate way.

[…]

## In a time crunch? The risks to skipping tests
In an ideal world, you would never skip testing code, ensuring the software is reliable
and easily reproducible. However, in practice there are times when skipping tests may be necessary —
perhaps due to tight deadlines, limited resources, or the need to quickly get a feature up
and running. While this can save time in the moment, it’s important to be cautious, as
skipping tests can lead to hidden problems that may become harder to fix later, particularly
as the project grows. Whenever tests are set aside, it’s best to have a plan for going back to add
them, to avoid risks to the stability and quality of the software.
