---
id: turing-way-data-documentation-and-metadata
title: "The Turing Way: Documentation and metadata (README for datasets, codebook or data dictionary, metadata, tagging)"
publisher: "The Turing Way Community"
url: https://github.com/the-turing-way/the-turing-way/blob/bcd8050eed319acc55f8ce0fe0410db157a17f04/book/website/reproducible-research/rdm/rdm-metadata.md
licence: CC-BY-4.0
licence_url: https://github.com/the-turing-way/the-turing-way/blob/bcd8050eed319acc55f8ce0fe0410db157a17f04/LICENSE.md
retrieved: 2026-11-02
kind: excerpt
repo: the-turing-way/the-turing-way
path: book/website/reproducible-research/rdm/rdm-metadata.md
commit: bcd8050eed319acc55f8ce0fe0410db157a17f04
topics: [reproducibility, data-documentation, metadata, data-dictionary, readme]
---
> Excerpt from `book/website/reproducible-research/rdm/rdm-metadata.md` in https://github.com/the-turing-way/the-turing-way at commit bcd8050eed319acc55f8ce0fe0410db157a17f04, "The Turing Way". Copyright © The Turing Way Community. Licensed under the Creative Commons Attribution 4.0 International licence (https://creativecommons.org/licenses/by/4.0/); see the repository file LICENSE.md. Retrieved 2026-11-02.
> Changes made: trimmed ("[…]" marks cuts); MyST markup, figures, citation roles and internal cross-references removed or reduced to plain text. No endorsement by the licensor is implied.

# Documentation and Metadata

Having data available is of no use if it cannot be understood. Without metadata to provide provenance and context, the data can't be used effectively.
For example, a table of numbers is useless if no headings describe what the columns/rows contain.
Therefore you should ensure that open datasets include consistent metadata, that is information about the data so that the data is fully described.
This requires that information accompanying data is captured in documentation and metadata.

## Documentation
Documentation provides context for your work.
It allows your collaborators, colleagues and future you to understand what has been done and why.

Data documentation can be done on different levels.
All documentation accompanying data should be written in clear, plain language.
Documentation allows data users have sufficient information to understand the source, strengths, weaknesses, and analytical limitations of the data so that they can make informed decisions when using it.

### README for datasets

A README file provides information about data (or software) and is intended to help ensure that the data can be correctly interpreted and used, by yourself or others.
A README file is generally shared together with an open dataset, or can be the landing page of your software/project repository.

README text files should describe the methods used for data collection and analysis and include data/software-specific information (parameters, variables, column headings, symbols used).
See [Make a README](https://www.makeareadme.com/) for more information on why README files are important and how you can set up your own README files.

#### README tips and examples

* Create one README file for each dataset
* Name the file README
* Use plain text file (`README.txt` or `README.md`).
  Or use README.pdf when text formatting is important for your file.

Example templates:

* [Cornell Template](https://cornell.app.box.com/v/ReadmeTemplate)
* [4TU.ResearchData’s guidelines for readme files](https://data.4tu.nl/s/documents/Guidelines_for_creating_a_README_file.pdf)

### Codebook or Data dictionary

A data dictionary or codebook ensures that the dataset is interpretable and reusable in the future, and has also been called the '[single most important piece of documentation you will create in your research study](https://cghlewis.com/blog/data_dictionary/)'.
A guiding question when setting up your data dictionary is: Can another researcher analyse/interpret the data using solely the codebook?

* Useful codebooks are human and machine readable (information provided can be accessed using automated approaches) and consistent.
* The codebook should at least list all variables and labels that are included in the dataset/article, and may include additional variables.
* You should explain the (range) of numerical values, units of measurement, sources, classification schemes used, or labels of questions asked.
* You can also include documentation or metadata not shown in the dataset itself, with an explanation of why it is not included in the final data/article, or outline in detail what missing data means (if there is any in the dataset).

You can check the [OSF guidance for data dictionaries](https://help.osf.io/article/217-how-to-make-a-data-dictionary) for more detailed variable guidance.

When using a spreadsheet as a codebook, the same formatting principles apply as to regular spreadsheet data

#### Data dictionary examples

* See Tables 1 and 2 in [Horstmann et al. 2020](https://doi.org/10.1027/1015-5759/a000620) or their [templates in spreadsheet format](https://osf.io/nerpa/)

## Metadata

Metadata is information about the data, descriptors that facilitate cataloguing data and data discovery.
Often, metadata are intended for machine reading.

When data is submitted to a trusted data repository, the machine-readable metadata is generated by the repository.
If the data is not in a repository a text file with machine-readable metadata can be added as part of the documentation.

- The type of research and the nature of the data also influence what kind of documentation is necessary.
- The level of documentation and metadata will vary according to the project, and the range of people the data needs to be understood by.
- Examples of documentation may include items like [data dictionaries](https://help.osf.io/hc/en-us/articles/360019739054-How-to-Make-a-Data-Dictionary) (see [here for a template](https://data.nal.usda.gov/data-dictionary-blank-template)) or codebooks, protocols, logbooks or lab journals, README files, research logs, analysis syntax, algorithms and code comments.
- Variables should be defined and explained using data dictionaries or codebooks.
- Data should be stored in logical and hierarchical folder structures, with a README file used to describe the structure.
The README file is helpful for others and will also help you find your data in the future.
See the [README template from Cornell](https://cornell.app.box.com/v/ReadmeTemplate) for an example.
- It is best practice to use recognised community metadata standards to make it easier for datasets to be combined.

[…]

## Tagging

Tags are keywords assigned to files, and a way to add metadata to a file to organise them more flexibly.
While a file can only be in one folder at a time, it can have an unlimited number of tags.

Some tips include:
- Use short tag names (one or two words)
- Be consistent with tags
- Not all file formats allow tags, and when files are transferred tags may be stripped

See [Tagging and Finding Your Files by MIT libraries](https://libguides.mit.edu/metadataTools)) for more information. 
