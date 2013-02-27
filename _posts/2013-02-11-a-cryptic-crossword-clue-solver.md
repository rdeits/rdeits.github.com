---
layout: post
title: "A Cryptic Crossword Clue Solver"
category: 
tags: []
---
{% include JB/setup %}

I really enjoy crosswords, and over the last year I've come to enjoy cryptic (or British-style) crosswords even more. Each cryptic clue consists of a _definition_ part, which behaves a lot like a regular crossword clue, and _wordplay_ part, which might consist of anagrams, initials, synonyms, reversals, acrostics, and other tricks. For example, here's a pretty easy cryptic clue:

	Initially babies are naked. (4)

The (4) is the length of the answer, which is BARE. Don't be fooled by the meaning of the whole clue; it's actually designed to be intentionally distracting. The key to solving this clue is to figure out the wordplay: "Initially" is actually a hint to take the first letter of "babies," which gives "b". If we combine "b" with "are" (from the clue), we get "bare", which means "naked," and is thus the answer. Confused yet? Let's try another:

	Sat up, interrupting sibling's balance (6)

The answer is STASIS. How did we get there? Well, this was a Down clue, so "Sat up" means we should reverse "sat" to get "tas". For "sibling," we'll try "sis" (as in "sister"), and we'll take "interrupting" to mean that "tas" goes inside "sis". That gives "stasis," which means "balance." The definition part of the clue is "balance" and the wordplay is "Sat up, interrupting sibling". We know we have a good answer when the wordplay and the definition match.

After spending many, many hours doing cryptic crosswords, I began to notice patterns in the way the wordplays and definitions worked, and I realized that I might be able to create an automatic solver for cryptic clues. A few months later, I have a working version that can solve many cryptic clues very effectively. It's often faster and smarter than I am, and it makes a fun tool to play with while I'm solving. Here are its answers for the two clues given above:
 
	'initially' means to take a substring of 'babies' to get B. 
	'naked' is the definition. 
	Combine 'b' and 'are' to get BARE. 
	BARE matches 'naked' with confidence score 100%. 

and

	'up' means to reverse 'sat' to get TAS. 
	Take a synonym of 'siblings' to get SIS. 
	'interrupting' means to insert 'tas' and 'sis' to get STASIS. 
	'balance' is the definition. 
	STASIS matches 'balance' with confidence score 100%. 


If you just want to play with it, check it out here: [https://github.com/rdeits/cryptics](https://github.com/rdeits/cryptics). Otherwise, read on. 

#Background
 Each cryptic clue consists of two parts: a definition and a wordplay, but the distinction between those two parts is intentionally obscured. Both parts of the clue, however, describe the same word, so we can be very confident in our answer if it matches the wordplay and the definition well. Here are a few more examples:

	Spin broken shingle. (7)

The answer here is ENGLISH. The definition is "Spin", and the wordplay is "broken shingle". "Broken" is an indicator to take an anagram, and an anagram of "shingle" is "english". In tennis, "english" can mean "spin", so it's the answer.   


	Throw out second-rate prevention measure? (6)

This one's much trickier: the answer is BOUNCE. The definition is "Throw out". "Second-rate" gives "B" (as in the letter grade) and "prevention measure" gives "ounce" (as in "an ounce of prevention is worth a pound of cure"). Putting them together, we get "bounce."

	She literally describes high society (5) 

The answer is ELITE. "High society" is the definition, and "describes" tells us to look for a word hidden within another phrase. If we look in "She literally", we can find "elite" (shE LITErally).

#Solving Cryptics
When I try to solve a cryptic clue, I am performing a search over a few dimensions. First, the _definition_ word must be identified. This is always the first or last element in the clue, but it may consist of more than one word. The remainder of the clue is the wordplay, and it has a lot of possible structures. Each word in the wordplay can do one of several possible things:

1. _literal_: The word itself
2. _synonym_: A synonym of the word
3. _first_: The first letter of the word
4. _null_: Nothing (some words are just filler)
5. _function indicator_: Indicates a particular manipulation of some other word in the wordplay

Function indicators are by far the most complex type. There are many functions which can combine and alter words in the wordplay. Some of the most common are substrings (taking part of a word), anagrams (rearranging a word), and reversals. Each function which is applied in the wordplay has an _indicator_ which identifies the function. For example, in

	Returning regal drink (5)

"Returning" is an indicator to try a reversal, and if we reverse "regal", we get "lager", a type of beer and thus a good synonym for "drink". 

Wordplay functions are hierarchical, so some functions can operate on the output of others. For example, a more complex clue:

	Join trio of astronomers in marsh (6)

The definition is "Join". "marsh" gives a synonym, "fen". "Trio of" is a function indicator, which tells us to take a substring of "astronomers", giving "ast". "in" is also a function indicator, telling us to put "ast" inside of "fen" to give "fasten", which means "Join", so the answer is FASTEN.

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



1. A clue always consists of two parts: a definition and a wordplay component. 

1. The definition is always the first or last phrase in the clue.

1. The wordplay consists of combinations of known functions, such as substrings, anagrams, synonyms, reversals, insertions, etc.

1. The structure of a cryptic crossword clue can be reasonably well-approximated by a fairly restricted [CFG (context-free grammar)](http://en.wikipedia.org/wiki/Context-free_grammar) and can be parsed into a syntactic tree using that grammar.

In practice, these assumptions are pretty good. 

## The Context-Free Grammar Parser

A CFG is a way of specifying the allowable structures of a series of _tokens_. In linguistics, those tokens are words and the structures are things like noun phrases, adjective phrases, sentences, prepositional phrases, and so on. The CFG specifies the rules about how those structures can be formed and combined. For example, in English, we might have a rule that says: "A _sentence_ consists of a _noun phrase_ and a _verb_", and another that says "A _noun phrase_ consists of the word 'the' and a _noun_". If we have a list of nouns and verbs, then we can make lots of valid English sentences using these rules, like "The cat sleeps" and "The man runs" and "The elephant commiserates". Obviously, we haven't covered all of English yet: to do that, we would need to add a lot more rules and ways for parts of a sentence to combine. 

We can create a similar structure for cryptic crossword clues. For example, we can define a rule which says: "an _anagram_ consists of an _anagram indicator_ and a _literal word_". That covers the structure in `Spin broken shingle`, where "broken" was the _anagram indicator_ and "shingle" was the _literal word_. We can build up similar rules for insertions, reversals, substrings, and so on, and by doing so we can describe all the allowable structures of a cryptic clue.

# Solving a Clue
To solve a clue, the solver first determines all possible ways to combine words from the clue into phrases (where a "phrase" is one or more words connected by underscores). For example, one phrasing of the clue "Initially babies are naked" is \["initially", "babies", "are", "naked\], another is \["initially", "babies_are", "naked"\], and another is \["initially", "babies_are_naked"\] 

Next, the definition of the clue is chosen to be the first or last phrase (both possibilities are fully explored by the solver). Finally, the remaining words are passed into the wordplay CFG to determine all of the ways that each word could be used. 

For each phrasing, we use the CFG to generate all possible syntactic structures for those words. The CFG is very lenient about allowing words to have a variety of meanings, but it does have lists of common function indicators, which it uses to eliminate unlikely parses. For example, "initially" is almost always a substring indicator, so it will almost certainly not act as an anagram or reversal indicator. 

Here are a few structures for "initially", "babies", "are", "naked"]:

	(top, 
	  (substring, 
	  	(substring indicator, 'initially'), 
	  	(literal, 'babies')), 
	  (literal, 'are'), 
	  (definition, 'naked')
	)

'top' is just a label for the top-level structure of every cryptic clue.

This structure says: "combine a substring of "babies" with "are" to get a word that means "naked"". 

	 (top, 
	   (definition, 'initially'), 
	   (substring
	     (reverse, 
	       (literal, 'babies'), 
	       (reversal indicator, 'are')), 
	     (substring indicator, 'naked')
	 )

This means: "reverse "babies" and then take a substring to get a word which means "initially". 

	(top,
      (definition, 'initially'),
      (anagram
	    (anagram indicator, 'babies')
	    (literal, 'are'))
	  (first letter, 'naked'))
	)

This means: "anagram "are", then add the first letter of "naked" to get a word which means "initially". 

And so on. Following the CFG will give us many, many possible structures, most of which are totally unreasonable. So how do we sort through those structures? The answer is, essentially, to evaluate each structure and see if it can produce an answer. Let's go through each of the three example structures above:  

	(top, 
	  (substring, 
	  	(substring indicator, 'initially'), 
	  	(literal, 'babies')), 
	  (literal, 'are'), 
	  (definition, 'naked')
	)

For the _substring_, we will try all possible substrings of "babies" and combine each one with "are". Most of those will not give us words which have the correct number of letters (4), but one will: "b" + "are" = "bare". This gives us "bare" as a possible answer. 

	 (top, 
	   (definition, 'initially'), 
	   (substring
	     (reverse, 
	       (literal, 'babies'), 
	       (reversal indicator, 'are')), 
	     (substring indicator, 'naked')
	 )

Reversing "babies" gives "seibab". No substring of that will give us a 4-letter word, so this structure is definitely wrong. 

	(top,
      (definition, 'initially'),
      (anagram
	    (anagram indicator, 'babies')
	    (literal, 'are'))
	  (first letter, 'naked'))
	)

Anagramming "are" gives, among other things, "ear", and adding the first letter of "naked" gives "ear" + "n" = "earn", which is a word. So "earn" is another possible answer. 

## Ranking Answers

Using the CFG to generate clue structures and the solving them gives us a long list of possible 
answers and the functions which produced them. How can we determine which structure (and thus which answer) is correct? 

For now, I'm relying entirely on the brilliance of the Python Natural Language Toolkit (NLTK). Using the Wordnet corpus, which groups English words by related meanings, we can actually compute the similarity in meaning between pairs of words. Let's check the answers generated in the examples above.

The first structure gave us "bare" as the answer and "naked" as the definition. Using the Python NLTK, we compute that the similarity in meaning between "bare" and "naked" is 1 (the highest possible value), so "bare" is a very good answer. 

The second structure gave no 4-letter answers, so we can move on.

The third structure gave "earn" as the answer and "initially" as the definition. The similarity in meaning between those words is only 0.4, which is quite low, so "earn" is probably not the answer. 

Repeating this process for all the possible answers generated by all the possible parsings, we get a ranked list of answers to the clue, and thus we've created a functional, automatic, cryptic clue solver! 

# Internal Implementation

Originally, the solver was implemented in a mix of Python (for its fantastic Natural Language Toolkit) and Go (for its speed and concurrency). The web server, CFG parser, and answer scoring were implemented in Python, while the solving mechanics were all implemented in Go. The Go code ran as a subprocess spawned from Python and communicated over Stdin/Stdout.  Structured clues, such as: 

	('top', (sub, ('sub_', 'initially'), ('lit', 'babies')), ('lit', 'are'), ('d', 'naked'))

were generated in Python and sent to the Go solver over Stdin, and solved structured clues, such as: 

	('top', ('sub', ('sub_', 'initially', ''), ('lit', 'babies', 'BABIES'), 'B'), ('lit', 'are', 'ARE'), ('d', 'naked', ''), 'BARE')

were returned from the Go solver to Python to have their answers scored and displayed.

However, I managed to pull a few clever tricks to reduce the amount of repeated computation and caching of answers which allowed me to implement the entire solver in Python without any loss of computing speed (actually, it got about 30% faster). So the system is now pure-Python and likely to stay that way for the immediate future.

# Examples

Here are some more clues, along with the first two answers returned by the solver. Each answer is given along with its meaning similarity score (converted to a percentage) and the wordplay structures which created it. The plain-English descriptions of each structure are actually generated automatically by the solver. 

##Spin broken shingle (7) 
Correct answer: ENGLISH

**english**: 100%

	100%: (top (d "spin") (ana (ana_ "broken") (lit "shingle") -> ENGLISH)) 
	'spin' is the definition. 'broken' means to anagram 'shingle' to get ENGLISH. 
	ENGLISH matches 'spin' with confidence score 100%. 

	['english', 0.24, '(top (syn "spin" -> ENGLISH) (d "broken_shingle"))'] 
	Take a synonym of 'spin' to get ENGLISH. 'broken_shingle' is the definition. 
	ENGLISH matches 'broken_shingle' with confidence score 24%.

**violate**: 33% 

	['violate', 0.3333333333333333, '(top (sub (sub_ "spin") (syn "broken" -> VIOLATED) -> VIOLATE) (d "shingle"))'] 
	Take a synonym of 'broken' to get VIOLATED. 
	'spin' means to take a substring of 'violated' to get VIOLATE. 
	'shingle' is the definition. VIOLATE matches 'shingle' with confidence score 33%. 


## M's Rob Titon pitching slider? (10)
Correct answer: TROMBONIST

**trombonist**: 63%

	['trombonist', 0.631578947368421, '(top (ana (lit "ms_rob_titon") (ana_ "pitching") -> TROMBONIST) (d "slider"))'] 
	'pitching' means to anagram 'ms_rob_titon' to get TROMBONIST. 'slider' is the definition. 
	TROMBONIST matches 'slider' with confidence score 63%. 

**surcharges**: 33%

	['surcharges', 0.3333333333333333, '(top (d "ms") (syn "rob" -> SURCHARGE) (sub (sub_ "titon") (rev (syn "pitching" -> SLOPING) (rev_ "slider") -> GNIPOLS) -> S) -> SURCHARGES)'] 
	'ms' is the definition. Take a synonym of 'rob' to get SURCHARGE. 
	Take a synonym of 'pitching' to get SLOPING. 
	'slider' means to reverse 'sloping' to get GNIPOLS. 
	'titon' means to take a substring of 'gnipols' to get S. 
	Combine 'surcharge' and 's' to get SURCHARGES. 
	SURCHARGES matches 'ms' with confidence score 33%. 

## Sat up, interrupting sibling's balance (6) s.....
Correct answer: STASIS

**stasis**: 100%

	[u'stasis', 1, u'(top (ins (rev (lit "sat") (rev_ "up") -> TAS) (ins_ "interrupting") (syn "siblings" -> SIS) -> STASIS) (d "balance"))'] 
	'up' means to reverse 'sat' to get TAS. Take a synonym of 'siblings' to get SIS. 
	'interrupting' means to insert 'tas' and 'sis' to get STASIS. 
	'balance' is the definition. STASIS matches 'balance' with confidence score 100%. 

	[u'stasis', 1, u'(top (ana (lit "sat") (ana_ "up_interrupting") -> STA) (syn "siblings" -> SIS) (d "balance") -> STASIS)'] 
	'up_interrupting' means to anagram 'sat' to get STA. Take a synonym of 'siblings' to get SIS. 
	'balance' is the definition. Combine 'sta' and 'sis' to get STASIS. 
	STASIS matches 'balance' with confidence score 100%. 

**sprout**: 53%

	['sprout', 0.5333333333333333, '(top (ins (sub (sub_ "sat") (syn "up" -> SPROUT) -> PROUT) (ins_ "interrupting") (first "siblings" -> S) -> SPROUT) (d "balance"))'] 
	Take a synonym of 'up' to get SPROUT. 'sat' means to take a substring of 'sprout' to get PROUT. 
	Take the first letter of 'siblings' to get S. 
	'interrupting' means to insert 'prout' and 's' to get SPROUT. 'balance' is the definition.
	 SPROUT matches 'balance' with confidence score 53%.


## Hungary's leader, stuffy and bald (8)

**hairless**: 100%

	100%: (top (sub (lit "hungarys") (sub_ "leader") -> H) (syn "stuffy" -> AIRLESS) (null "and") (d "bald") -> HAIRLESS) 
	'leader' means to take a substring of 'hungarys' to get H.
	 Take a synonym of 'stuffy' to get AIRLESS. 'and' is a filler word. 
	 'bald' is the definition. Combine 'h' and 'airless' to get HAIRLESS. 
	 HAIRLESS matches 'bald' with confidence score 100%. 

**baldpate**: 68%

	68%: (top (d "hungarys_leader") (sub (sub_ "stuffy_and") (syn "bald" -> BALD_PATED) -> BALDPATE) 
	'hungarys_leader' is the definition. Take a synonym of 'bald' to get BALD_PATED. 
	'stuffy_and' means to take a substring of 'bald_pated' to get BALDPATE. 
	BALDPATE matches 'hungarys_leader' with confidence score 68%. 


# Try It!
All the source code for the solver is available on [github.com/rdeits/cryptics](https://github.com/rdeits/cryptics). I'd be very interested to hear if this tool ends up being useful for anyone. 
	