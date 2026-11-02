---
id: govuk-service-manual-writing-for-user-interfaces
title: "GOV.UK Service Manual: Writing for user interfaces"
publisher: "GOV.UK Service Manual (Government Digital Service)"
url: https://www.gov.uk/service-manual/design/writing-for-user-interfaces
licence: OGL-3.0
licence_url: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
retrieved: 2026-11-02
kind: excerpt
topics: [writing, ux, plain-english, interface-text, microcopy, forms]
---
> Excerpt from "Writing for user interfaces", GOV.UK Service Manual (Government Digital Service), https://www.gov.uk/service-manual/design/writing-for-user-interfaces. Crown copyright. Retrieved 2026-11-02.
> Contains public sector information licensed under the Open Government Licence v3.0.
> Trimmed; "[…]" marks cuts. Not an official version.

## Writing for user interfaces

Aim to minimise cognitive load by being as clear as possible and using the same language as your users. This helps:

- reduce the amount of time you spend dealing with mistakes
- make your service inclusive for people who struggle with reading or have limited English
- make your service accessible

Even specialist users prefer clear language. No one likes having their time wasted, especially busy people like health workers.

It’s especially important to choose an intuitive name for your service. If your title reflects your users’ language, they’ll be able to find your service and understand what it does.

Do not follow strict grammar conventions if it makes things clearer not to.

## Think about alternatives before you add more words

On the internet people tend to scan rather than read. Even more so when they’re using a transactional service.

So start with less. If you’re creating a form, start with some simple questions and only add help text if user research shows that you need it.

Design your service to take account of the fact that lots of people will not read the content in detail. For example, ask questions to establish eligibility rather than putting a long list of eligibility conditions on the start page.

If you find yourself having to explain how the user interface works, that’s a sign something has gone wrong. Fix the interface so it does not need explaining.

## Keep copy short and direct

Break up copy into short sentences. One idea per sentence.

Space is at a premium with user interfaces. So put the important words first and drop any unnecessary words.

For example, if you’re writing help text there’s usually no need to say ‘This is the total cost’. Just say ‘Total cost’. If you’re writing an error message, do not say ‘You have entered the wrong password’. Say ‘Wrong password’.

You do not usually need the word ‘now’. For example, just say ‘apply’ rather than ‘apply now’ (unless you’re giving the user two options: apply now or apply later).

## Tone

Be approachable and helpful, but not overly familiar. Remember that it’s government ‘speaking’.

Say ‘sorry’ if something serious has gone wrong - for example, the service has stopped working completely. ‘Sorry, there is a technical problem. Please try again in a few moments.’

There’s no need to say ‘sorry’ in validation error messages.

There’s usually no need to say ‘please’ or ‘please note’.

There’s usually no need to say thank you. For example, it’s fine to say ‘Application complete’ rather than ‘Thank you for your application’.

Avoid things like humorous error messages. People often use government services for serious things or when under stress.

If people do not notice your copy, you’re probably doing it right. Aim to be boring.

## Do not exclude anyone

Do not rely on shape, size, colour or location alone to communicate information, because not all users will share that frame of reference. For example, do not say things like:

- ‘click the green button’
- ‘use the menu on the left of the page’
- ‘find more information in the square box’

Break up long pages with headings. It’s easier to scan and read. Headings should describe the purpose of the text that follows - they should not be part of the text.

Screen reader users often read out lists of links in isolation, so make the purpose of the link clear from the link text alone. For example, ‘click here’ is not accessible link text.

Sometimes you need to shorten link text to avoid lots of duplication. If you do that, make sure links are still accessible to screen readers. For example, by adding hidden text to the ‘change’ links on check your answers pages.

## Style

Follow the GOV.UK style guide on how to write times and dates, spelling, punctuation, acronyms and other conventions.

### Headings and `<title>`

It’s fine to have headings as questions. In fact, it can help to remove duplication.

But make sure every text box, set of radio buttons or other input field still has a question directly associated with it in the html, so it makes sense to screen readers. For example, by using a visually hidden `<legend>` or `<label>`.

Each page should have a single `<h1>`. The `<h1>` should describe what the page does.

The `<title>` should be based on the `<h1>`, and follow this format:

Where do you live? - Register to vote - GOV.UK

### Pronouns (we, you, me, my)

Forms are like a conversation between the service and the user.

If it’s the service ‘speaking’, the user is ‘you’ or ‘your’ and the service is ‘we’, ‘us’, ‘our’ and so on.

If it’s the user ‘speaking’, use ‘I’, ‘me’ or ‘my’.

This applies to all microcopy, including headings, input labels and link text.

For example, the Register to vote service asks users ‘What is your National Insurance number?’. If the user does not know it, they can select a link ‘find your National Insurance number’ or select ‘I am not sure what a National Insurance number is’.

Use ‘they’ instead of ‘he or she’ or ‘he/she’. It’s simpler, and works better for people who do not identify as male or female.

### Capitalisation and punctuation

Use sentence case everywhere, except for proper nouns.

Headings and input field labels are sentence case, but not punctuated. Write other copy in full sentences, with a full stop at the end.

### Contractions, abbreviations and acronyms

Do not use ‘ie’. Use ‘for example’ instead of ‘eg’.

Use simple contractions like ‘you’re’ and ‘we’ll’.

Avoid:

- should’ve, could’ve, would’ve, they’ve - these can be hard to read
- negative contractions like ‘can’t’ and ‘don’t’ - some users find them harder to read, or misread them as the opposite of what they say

Include any relevant acronyms on your GOV.UK start page for SEO purposes, but try to avoid using them inside the transaction.

And if you do use them, spell them out in full on each page. Do not rely on people remembering them across different pages.

## URLs

Make sure your URLs are clear and readable. This will help users understand where they are in your service.

Do not include personal information (like a user’s name or date of birth) in the `<title>` field of a URL - you do not want it to show up in your site analytics.

## Legal content

All language should be as simple to understand as possible, including privacy policies and declarations. Explaining users’ rights and obligations clearly is good legal practice as well as being good for usability.
