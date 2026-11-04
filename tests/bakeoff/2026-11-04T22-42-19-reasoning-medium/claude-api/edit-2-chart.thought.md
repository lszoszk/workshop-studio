I'm adding a new FIG.03 bar chart showing total records per year, placed right after the FIG.02 section, and keeping the change small.

I'm working out where to put the edit in the HTML: a unique anchor is the "How this is computed" note line followed by the empty figsrc div, and I'll insert the FIG.03 block after that. On the JS side I'm adding a third chart variable next to the existing ones, then appending the FIG.03 render after the FIG.02 block.

I'm placing the new FIG.03 code just before the `/* FIG.02 */` comment in the script, using vertical bars per year with value labels on top, the same label plugin pattern as the other charts. The figure source div is already set up by the render function, so that part needs no changes.

