---
id: claude-cookbook-citations
title: "Claude Cookbooks: Citations (API-grounded citations, document types, rendering numbered references)"
publisher: "Anthropic (claude-cookbooks contributors)"
url: https://github.com/anthropics/claude-cookbooks/blob/c43f56d0360b9b1f631bd090fd199231d4c880cc/misc/using_citations.ipynb
licence: MIT
licence_url: https://github.com/anthropics/claude-cookbooks/blob/c43f56d0360b9b1f631bd090fd199231d4c880cc/LICENSE
retrieved: 2026-11-02
kind: code
repo: anthropics/claude-cookbooks
path: misc/using_citations.ipynb
commit: c43f56d0360b9b1f631bd090fd199231d4c880cc
topics: [citations, llm, retrieval, python, grounding]
---
> Excerpt from `misc/using_citations.ipynb` ("Citations") in https://github.com/anthropics/claude-cookbooks at commit c43f56d0360b9b1f631bd090fd199231d4c880cc. Copyright (c) 2023 Anthropic. Released under the MIT licence (notice at the end of this page). Retrieved 2026-11-02.
> The notebook was converted to Markdown (text cells as written, code cells in fences, outputs not included). Trimmed; "[…]" marks cuts. In the code, the long system prompt is replaced by "[…]" and the helper that prints the raw response is cut. The code uses the Anthropic Python SDK and the Citations feature of the Claude API; model names and options change, so check the current API documentation before copying.

# Citations 

The Claude API features citation support that enables Claude to provide detailed citations when answering questions about documents. Citations are a valuable affordance in many LLM powered applications to help users track and verify the sources of information in responses.

Citations are supported on all current Claude models; see the [citations documentation](https://platform.claude.com/docs/en/build-with-claude/citations) for the list. This notebook uses `claude-sonnet-5-5`.

The citations feature is an alternative to prompt-based citation techniques. Using this featue has the following advantages:
- Prompt-based techniques often require Claude to output full quotes from the source document it intends to cite. This increases output tokens and therefore cost.
- The citation feature will not return citations pointing to documents or locations that were not provided as valid sources.
- While testing we found the citation feature to generate citations with higher recall and percision than prompt based techniques.

The documentation for citations can be found [here](https://platform.claude.com/docs/en/build-with-claude/citations).

## Setup

First, let's install the required libraries and initalize our Anthropic client. 

```python
!pip install anthropic  --quiet
```

```python
import json
import os

import anthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
# ANTHROPIC_API_KEY = "" # Put your API key here!

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
MODEL = "claude-sonnet-5-5"
```

[…]

### Plain Text Documents

With plain text document citations you provide your document as raw text to the model. You can provide one or multiple documents. This text will get automatically chunked into sentences. The model will cite these sentences as appropriate. The model is able to cite multiple sentences together at once in a single citation but will not cite text smaller than a sentence.

Along with the outputted text the API response will include structured data for all citations. 

Let's see a complete example using a help center customer chatbot for a made up company PetWorld.

```python
# Read all help center articles and create a list of documents
articles_dir = "./data/help_center_articles"
documents = []

for filename in sorted(os.listdir(articles_dir)):
    if filename.endswith(".txt"):
        with open(os.path.join(articles_dir, filename)) as f:
            content = f.read()
            # Split into title and body
            title_line, body = content.split("\n", 1)
            title = title_line.replace("title: ", "")
            documents.append(
                {
                    "type": "document",
                    "source": {"type": "text", "media_type": "text/plain", "data": body},
                    "title": title,
                    "citations": {"enabled": True},
                }
            )

QUESTION = "I just checked out, where is my order tracking number? Track package is not available on the website yet for my order."

# Add the question to the content
content = documents

response = client.messages.create(
    model=MODEL,
    max_tokens=2048,
    system="[…]",
    messages=[
        {"role": "user", "content": documents},
        {
            "role": "user",
            "content": [{"type": "text", "text": f"Here is the user's question: {QUESTION}"}],
        },
    ],
)

# […]
```

#### Visualizing Citations
By leveraging the citation data, we can create UIs that:

1. Show users exactly where information comes from
2. Link directly to source documents
3. Highlight cited text in context
4. Build trust through transparent sourcing

Below is a simple visualization function that transforms Claude's structured citations into a readable format with numbered references, similar to academic papers.

The function takes Claude's response object and outputs:
- Text with numbered citation markers (e.g., "The answer [1] includes this fact [2]")
- A numbered reference list showing each cited text and its source document

```python
def visualize_citations(response):
    """
    Takes a response object and returns a string with numbered citations.
    Example output: "here is the plain text answer [1][2] here is some more text [3]"
    with a list of citations below.
    """
    # Dictionary to store unique citations
    citations_dict = {}
    citation_counter = 1

    # Final formatted text
    formatted_text = ""
    citations_list = []

    print("\n" + "=" * 80 + "\nFormatted response:\n" + "=" * 80)

    for content in response.content:
        if content.type == "text":
            text = content.text
            if hasattr(content, "citations") and content.citations:
                # Sort citations by their appearance in the text
                def get_sort_key(citation):
                    if hasattr(citation, "start_char_index"):
                        return citation.start_char_index
                    elif hasattr(citation, "start_page_number"):
                        return citation.start_page_number
                    elif hasattr(citation, "start_block_index"):
                        return citation.start_block_index
                    return 0  # fallback

                sorted_citations = sorted(content.citations, key=get_sort_key)

                # Process each citation
                for citation in sorted_citations:
                    doc_title = citation.document_title
                    cited_text = citation.cited_text.replace("\n", " ").replace("\r", " ")
                    # Remove any multiple spaces that might have been created
                    cited_text = " ".join(cited_text.split())

                    # Create a unique key for this citation
                    citation_key = f"{doc_title}:{cited_text}"

                    # If this is a new citation, add it to our dictionary
                    if citation_key not in citations_dict:
                        citations_dict[citation_key] = citation_counter
                        citations_list.append(
                            f'[{citation_counter}] "{cited_text}" found in "{doc_title}"'
                        )
                        citation_counter += 1

                    # Add the citation number to the text
                    citation_num = citations_dict[citation_key]
                    text += f" [{citation_num}]"

            formatted_text += text

    # Combine the formatted text with the citations list
    final_output = formatted_text + "\n\n" + "\n".join(citations_list)
    return final_output

formatted_response = visualize_citations(response)
print(formatted_response)
```

---

## Licence notice (MIT)

MIT License

Copyright (c) 2023 Anthropic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
