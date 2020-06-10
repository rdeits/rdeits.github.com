---
layout: post
title: "More Cryptic Crosswords"
category: Projects
tags: [cryptics]
---
{% include JB/setup %}

<style>
@media (min-width: 800px) {
 .input_prompt,
 .output_prompt {
  width:0px;
  position:relative;
  float:left;
  margin-top:3px
 }

 .output_prompt {
  left:-4em;
 }

 .input_prompt {
  left:-3.5em;
 }
 #page {
    padding: 2em 4.5em 1.5em 4.5em;
}
</style>

Recently, I've done a bunch of work to clean up the cryptic crossword clue solver which I first described in [an earlier post](/2013/02/11/a-cryptic-crossword-clue-solver). I have simplified the code layout and added more flexibility to the solver's interface, so it should be easier to experiment and play around with. What follows are a few examples of what the new solver can do. You can also view these examples as [a rendered IPython notebook](http://nbviewer.ipython.org/github/rdeits/cryptics/blob/master/cryptic_demo.ipynb) on nbviewer.org.

{% include posts/2013-12-26-cryptics/cryptic_demo.html %}