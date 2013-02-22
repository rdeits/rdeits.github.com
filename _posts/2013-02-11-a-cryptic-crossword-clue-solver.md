---
layout: post
title: "A Cryptic Crossword Clue Solver"
category: 
tags: []
---
{% include JB/setup %}

I really enjoy crosswords, and over the last year I've come to enjoy cryptic (or British-style) crosswords even more. Cryptics combine standard crossword clues with wordplay like anagrams, reversals, and acrostics to create clues which can be more interesting and challenging to solve. This fall, I decided to write a tool to solve cryptic crossword clues. It works now (sort of), and will successfully solve many of the easier cryptic clues. It's often faster and smarter than I am, and it makes a fun tool to play with while I'm solving. If you just want to play with it, check it out here: [https://github.com/rdeits/cryptics](https://github.com/rdeits/cryptics). Otherweise, read on. 

#Background
 Each cryptic clue consists of two parts: a definition and a wordplay, but the distinction between those two parts is intentionally obscured. Both parts of the clue, however, describe the same word, so once an answer is found, the solver can be very confident that it is correct. These clues are easier to describe with examples. Here are a few easy cryptic clues and their solutions:

	Initially babies are naked. (4)

The definition part of this clue is "naked," and the wordplay is "Initially babies are". The word "Initially" is actually a clue to take the first letter of "babies", which gives "b". Adding "b" to "are" gives "bare", which also means "naked", so the answer is "bare". 

	Spin broken shingle. (7)

The definition is "Spin", and the wordplay is "broken shingle". "Broken" is a clue to take an anagram, and an anagram of "shingle" is "english". In tennis, "english" can mean "spin", so the answer is "english". 

Having done a lot of cryptic crosswords, I began to notice the patterns common to the clues and the wordplays involved, and I decided that this would be a fun language and search problem. A few months later, I've created a general-purpose tool for solving cryptic clues, written in Python and Go. 

#Solving Cryptics
When I try to solve a cryptic clue, I am performing a search over a few dimensions. First, the _definition_ word must be identified. This is always the first or last element in the clue, but it may consist of more than one word. The remainder of the clue is the wordplay, and it has a lot of possible structures. Each word in the wordplay can do one of several possible things:

1. _literal_: The word itself
2. _synonym_: A synonym of the word
3. _first_: The first letter of the word
4. _null_: Nothing (some words are just filler)
5. _function indicator_: Indicates a particular manipulation of some other word in the wordplay

Function indicators are by far the most complex type. There are many functions which can combine and alter words in the wordplay. Some of the most common are substrings (taking part of a word), anagrams (rearranging a word), and reversals. Each function which is applied in the wordplay has an _indicator_ which identifies the function. For example, in

	Returning regal drink (5)

"Returning" is a clue to try a reversal, and if we reverse "regal", we get "lager", a type of beer and thus a good synonym for "drink". 

Wordplay functions are hierarchical, so some functions can operate on the output of others. For example, a more complex clue:

	Join trio of astronomers in marsh (6)

The definition is "Join". "marsh" gives a synonym, "fen". "Trio of" is a function indicator, which tells us to take a substring of "astronomers", giving "ast". "in" is also a function indicator, telling us to put "ast" inside of "fen" to give "fasten", which means "Join", so the answer is "fasten".

It's much easier to see this if we write it out as a hierarchy:

	(reverse, 
		(literal, 'regal') -> 'regal'
	) -> 'lager'

	(insert, 
		(substring of, 'astronomers') -> 'ast', 
		(synonym of, 'marsh') -> 'fen')
	) -> 'fasten

This begins to suggest a method for solving cryptic clues with software. If we can define all of the available functions and the ways they can combine, then we can search over all possible wordplays for a given clue. If we find a wordplay which gives a good match to the definition, then we have a good candidate answer. 

#How the Solver Works
>"Do the stupidest thing that could possibly work"

Rather than trying to predict the way a particular clue will be solved from its text alone, the solver attempts to try all remotely possible solutions for a given clue, then scores them by how well their answers match the clue. To do that, I make some assumptions:

1. The structure of a cryptic crossword clue can be reasonably well-approximated by a fairly restricted [CFG (context-free grammar)](http://en.wikipedia.org/wiki/Context-free_grammar) and can be parsed into a syntactic tree using that grammar.

2. A clue always consists of two parts: a definition and a wordplay component. 

3. The definition is always the first or last phrase in the clue.

4. The wordplay consists of combinations of known functions, such as substrings, anagrams, synonyms, reversals, insertions, etc.

In practice, these assumptions are pretty good. 



To solve a clue, the solver first determines all possible ways to combine words from the clue into phrases (where a "phrase" is one or more words connected by underscores). For example, one phrasing of the clue "Initially babies are naked" is \["initially", "babies", "are", "naked\], another is \["initially", "babies_are", "naked"\], and another is \["initially", "babies_are_naked"\] 

Next, the definition of the clue is chosen to be the first or last phrase (both possibilities are fully explored by the solver). Finally, the remaining words are passed into the wordplay context-free grammar to determine all of the ways that each word could be used. The CFG used is one that I developed based on my observations about cryptic clues. It encodes various rules which are commonly followed, such as that we almost never take an anagram of anything except a literal word from the clue, but we might insert that anagram into another word. 

For each phrasing, we use the CFG to generate all possible syntactic structures for those words. For example, a structure for ["initially", "babies", "are", "naked] is:

	('top', 
	  (sub, 
	  	('sub_', 'initially'), 
	  	('lit', 'babies')), 
	  ('lit', 'are'), 
	  ('d', 'naked')
	). 

'top' means to concatenate the strings produced by all of its arguments, and is always the top-level structure in a cryptic clue.

'sub' indicates a substring

'sub_' identifies the substring indicator word ("initially")

'lit' returns a word literally

'd' indicates the definition part of the clue

So, this structure says: "combine a substring of BABIES with ARE to get a word that means NAKED". Evaluating this for all substrings of BABIES, we come up with a single answer which is actually a word: B + ARE = BARE. Since BARE and NAKED are truly synonyms, we give this answer the maximal score of 1. 


The output format of the solver gives not only this score, but also the substrings which each part of the clue yielded: 

	['bare', 
	 1, 
	 ('top', 
	   ('sub', 
	     ('sub_', 'initially', ''), 
	     ('lit', 'babies', 'BABIES'), 
	   	  'B'), 
	   ('lit', 'are', 'ARE'), 
	   ('d', 'naked', ''), 
	  'BARE')
	] 

Of course, we are certain to produce a great many bad answers using this method, for example: 

	['evil', 
	 0, 
	 ('top', 
	   ('d', 'initially', ''), 
	   ('rev', 
	     ('rev_', 'babies', ''), 
	     ('syn', 'are', 'LIVE'), 
	    'EVIL'), 
	   ('null', 'naked', ''), 
	  'EVIL')
	]

The above says: "Take a synonym of 'are': LIVE, reverse it: EVIL to get a word meaning INITIALLY. However, the similarity in meaning between EVIL and INITIALLY is essentially zero, so this answer gets a score of 0. 
In this way, we generate the most probable interpretation and solution for a given clue. 

# Internal Implementation

Currently, the solver is implemented in a mix of Python (for its fantastic Natural Language Toolkit) and Go (for its speed and concurrency). The web server, CFG parser, and answer scoring are implemented in Python, while the solving mechanics are all implemented in Go. The Go code runs as a subprocess spawned from Python and communicates over Stdin/Stdout.  Structured clues, such as: 

	('top', (sub, ('sub_', 'initially'), ('lit', 'babies')), ('lit', 'are'), ('d', 'naked'))

are generated in Python and sent to the Go solver over Stdin, and solved structured clues, such as: 

	('top', ('sub', ('sub_', 'initially', ''), ('lit', 'babies', 'BABIES'), 'B'), ('lit', 'are', 'ARE'), ('d', 'naked', ''), 'BARE')

are returned from the Go solver to Python to have their answers scored and displayed.

## Update 2013-02-22:
As of now, the solver has been reimplemented entirely in Python. I've spent some time playing around with the [RunSnakeRun](http://www.vrplumber.com/programming/runsnakerun/) profiling tool, and I've managed to make the pure-Python solver faster than the hybrid Python-Go solver was. 

# Examples

Here are some clues, along with the first few answers returned by the solver. Each answer is given along with its score (from 0 to 1) and the wordplay structures which created it. 

##Spin broken shingle (7) 
Correct answer: ENGLISH

**english**: 1 

	['english', 1, '(top (d "spin") (ana (ana_ "broken") (lit "shingle") -> ENGLISH))'] 
	['english', 0.24, '(top (syn "spin" -> ENGLISH) (d "broken_shingle"))'] 
**violate**: 0.333333333333 

	['violate', 0.3333333333333333, '(top (sub (sub_ "spin") (syn "broken" -> VIOLATED) -> VIOLATE) (d "shingle"))'] 
**reached**: 0.333333333333 

	['reached', 0.3333333333333333, '(top (sub (sub_ "spin") (syn "broken" -> BREACHED) -> REACHED) (d "shingle"))'] 

## M's Rob Titon pitching slider? (10)
Correct answer: TROMBONIST

**trombonist**: 0.631578947368 

	['trombonist', 0.631578947368421, '(top (ana (lit "ms_rob_titon") (ana_ "pitching") -> TROMBONIST) (d "slider"))'] 
**surcharges**: 0.333333333333 

	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (sub_ "titon") (rev (syn "pitching" -> SLOPING) (rev_ "slider") -> GNIPOLS) -> S) -> SURCHARGES)'] 
	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (rev (rev_ "titon") (syn "pitching" -> SLOPING) -> GNIPOLS) (sub_ "slider") -> S) -> SURCHARGES)'] 
	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (sub_ "titon_pitching") (lit "slider") -> S) -> SURCHARGES)'] 
	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (sub_ "titon_pitching") (syn "slider" -> SKIDDER) -> S) -> SURCHARGES)'] 
**manuscript**: 0.25 

	['manuscript', 0.25, '(top (sub (syn "ms" -> MANUSCRIPT) (sub_ "rob") -> MANUSCRIP) (sub (sub_ "titon") (syn "pitching" -> CANT) -> T) (d "slider") -> MANUSCRIPT)'] 
	['manuscript', 0.25, '(top (sub (syn "ms" -> MANUSCRIPT) (sub_ "rob") -> MANUSCRIP) (first "titon_pitching" -> T) (d "slider") -> MANUSCRIPT)'] 
	['manuscript', 0.225, '(top (sub (syn "ms" -> MANUSCRIPT) (sub_ "rob") -> MANUSCRIP) (first "titon" -> T) (d "pitching_slider") -> MANUSCRIPT)'] 

## Sat up, interrupting sibling's balance (6) s.....
Correct answer: STASIS

**stasis**: 1 

	[u'stasis', 1, u'(top (ins (rev (lit "sat") (rev_ "up") -> TAS) (ins_ "interrupting") (syn "siblings" -> SIS) -> STASIS) (d "balance"))'] 
	[u'stasis', 1, u'(top (ana (lit "sat") (ana_ "up_interrupting") -> STA) (syn "siblings" -> SIS) (d "balance") -> STASIS)'] 
**sprout**: 0.533333333333 

	['sprout', 0.5333333333333333, '(top (ins (sub (sub_ "sat") (syn "up" -> SPROUT) -> PROUT) (ins_ "interrupting") (first "siblings" -> S) -> SPROUT) (d "balance"))'] 
	['sprout', 0.5333333333333333, '(top (first "sat" -> S) (sub (syn "up" -> SPROUT) (sub_ "interrupting_siblings") -> PROUT) (d "balance") -> SPROUT)'] 

**sprint**: 0.25 

	['sprint', 0.25, '(top (sub (sub_ "sat") (syn "up" -> SPROUT) -> SPR) (sub (lit "interrupting") (sub_ "siblings") -> INT) (d "balance") -> SPRINT)'] 


# Try It!
All the source code for the solver is available on [github.com/rdeits/cryptics](https://github.com/rdeits/cryptics). I'd be very interested to hear if this tool ends up being useful for anyone. 
	