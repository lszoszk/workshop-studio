---
id: uk-af-charts-choosing-and-supplying
title: "Data visualisation: charts (choosing a chart, titles, alt text, source, data download)"
publisher: "UK Government Analysis Function"
url: https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/
licence: OGL-3.0
licence_url: https://analysisfunction.civilservice.gov.uk/terms-of-use/
retrieved: 2026-11-02
kind: excerpt
topics: [dataviz, charts, accessibility, alt-text, bar-chart]
---
> Excerpt from "Data visualisation: charts", Government Analysis Function, Crown copyright, https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/. Retrieved 2026-11-02.
> Contains public sector information licensed under the Open Government Licence v3.0. Text only; images on the source site are not covered by the licence.
> Trimmed; "[…]" marks cuts. Original headings kept. Not an official version.

## Choosing the right chart

### What is the message?

Think about the message your chart is aiming to get across. A good way of thinking about this is to imagine you are describing what the chart is showing over the phone – what would you say?

If you cannot write down the message your chart is giving in a few sentences, you should think again about the chart you have chosen.

Ask yourself: Can I simplify this? Can I break it down in another way? Am I trying to communicate too many messages within one chart?

### Statistical relationships

After you have decided on the message, consider the statistical relationship you’re trying to show.

The right chart will depend on the values in your data and the statistical story you’re telling. Try out different options and test your ideas (see the Testing section of this guidance).

The Visual Vocabulary tool from the Financial Times can help you choose the best chart

#### Table matching chart types to statistical relationships

| Relationship | Example | Recommended chart types |
|---|---|---|
| Distribution | Population by age | Bar chart, population pyramid, box plot, dot plot |
| Time series | Price inflation over time | Line chart, calendar heat map |
| Ranking | Schools ranked by performance | Bar chart, lollipop chart, slope chart |
| Deviation | Rail company performance compared with target | Bar chart, dot plot - figure 7 in this release |
| Correlation | Relationship between weight and height | Scatterplot, line graph |
| Magnitude | Average income by region | Bar chart |
| Spatial | Geographical clusters of notifiable diseases | Map |
| Part-to-whole | Total economic production by industrial sector | Bar chart, pie chart, donut chart, tree map, bubble chart |
| Flow | Trade between countries | Sankey graph |

## Publishing charts

### HTML or image?

If the website you publish on has the functionality to build charts within the HTML code which meets the accessibility standards, use this functionality.

For example, if you publish on GOV.UK you can create horizontal bar charts in HTML.

Examples of bar charts you can create on GOV.UK.

If you work for the Office for National Statistics or publish on the Explore Education Statistics website, your options for HTML charts are much wider.

If you cannot publish charts in HTML you will have to upload your chart as an image.

#### Scalable Vector Graphic (SVG) format

It is best practice to use the Scalable Vector Graphic (SVG) format when publishing images of charts. Unlike bitmap file types such as JPG or PNG, SVGs retain the same quality no matter what screen resolution or size they are viewed at. This means a user can zoom in and out and the image retains its quality. This adaptability makes it a more accessible format.

Changing a PNG or JPEG file into an SVG does not make it scalable, it must be done from the source file.

It is possible to save images of charts made in Microsoft programs, R and Python in the SVG format. More information is in our ‘Making analytical publications accessible’ guidance.

[…]

### Titles

All charts need at least one title, but it is considered best practice to give them two. These should be: a headline title and a formal statistical subtitle.

The headline title should communicate the headline message of the chart. For example ‘Increase in number of people living alone’.

The statistical subtitle should say what the data is, the geography the data relates to and the time period shown. For example, ‘Figure 1: Number of people living in one person households, England, 1991 to 2021’.

We advise that one of the titles should have ‘Figure n’ at the start to denote which figure it is in the report. This helps navigation and it can help screen reader users understand there is a figure coming up in the next part of the publication.

Both titles should be tagged correctly to meet the accessibility legislation. For example, first level subheadings should have a Headings 2 tag, second level subheadings should have a Headings 3 tag and so on.

[…]

### Alternative text

Alternative text is often thought of as the text that sits in the code behind an image, but really it refers to any text that describes non-text content. It is needed so that people with visual or certain cognitive impairments can understand the content communicated by images.

To meet accessibility success criterion 1.1.1 all non-text content should have alternative text that “serves the equivalent purpose”.

For charts this can be given by:

- a table of the data presented in the chart
- a text description of the message the chart is presenting

Which you choose should depend on what you would expect a non-disabled user to get from the chart. If you expect a non-disabled user to read the data from the chart, give a table. If you expect them to take away an overall understanding of the data, give a text description of what you want them to understand. If you expect them to do both, give both.

The text description should describe what you want users to understand from the chart. It should not repeat the chart title, be a literal description or outline every data point shown. Imagine you are describing what the chart is showing to someone who cannot see it.

#### Placement of text description

If you use a text description, our advice is that this should live in the body of the page, directly underneath the chart. In this situation the image of the chart should be marked as decorative and therefore hidden from screen reader software. This is usually done by leaving the ‘alt attribute’ blank but sometimes there will be a box to tick.

Depending on the length of your publication and how your commentary is written it can be a good idea to place the text description under a subheading. This subheading should be marked up correctly (given the structure of the page you are publishing on). It should also be specific to the figure, for example “Description of figure 1”.

If you find the subheadings break up the text too much you can start the text under the chart with “Description of figure 1: . . . ” instead.

Example: in this publication from Welsh Government each chart is followed by a text description that starts with “Description of figure n . . . “

[…]

### Source

You should give the specific data source for each chart and link directly to it if you can. Avoid stating things like ‘Office for National Statistics’ and then linking to the website homepage. You should help users find the data.

As with titles, this text should be in the body text of the page and not part of the chart image.

It is best practice to provide source information in the following format: [publication, survey or other source of data] from the [organisation]

For example: Source: Childcare and early years survey of parents from the Department for Education.

Please note this is recently updated guidance (the older guidance said to use a dash instead of “from the”), so source information may look different across the website until this approach becomes embedded.

### Data download

It is best practice to provide the data displayed in each chart as an accessible data download. Providing data downloads improves the transparency of our data visualisations and allows people to accurately recreate our charts for their own needs.

Providing an accessible data download is a necessity if it is going to act as the alternative text for your chart. More information on alternative text can be found in our ‘Making analytical publications accessible’ guidance.

You should link to a data download underneath each chart. The file type and size should be included in the link.

The text used in the link to the data download should be specific and should not be identical to other links on the same webpage. Using multiple identical links that lead to different places on the same webpage can be very confusing for screen reader users.

For example avoid repeatedly using ‘Download the data’. Either state the title of the chart, or the figure number. For example: ‘Download the data for number of people living in single person households’ or ‘Download the data for figure 1’.

More information on providing data downloads is in our ‘Making analytical publications accessible’ guidance.
