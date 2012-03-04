---
layout: post
title: "Analog Integers in Python"
category: Projects
tags: [python]
---
{% include JB/setup %}

[This fantastic post](http://weegen.home.xs4all.nl/eelis/analogliterals.xhtml) by Eelis asks the question, "Have you ever felt that integer literals like "4" don't convey the true size of the value they denote?" Uh, well, honestly, no. 

If, however, you're intrigued enough to keep reading, then his solution is to define an "analog literal" which gives a proper visualization of its own size:

	assert( I-I == 0 );
    assert( I---I == 1 );
    assert( I-----I == 2 );
    assert( I-------I == 3 );

(According to the author, "Due to the way C++ operators work, we must use N * 2 + 1 dashes between the I's to get a value of N")

Thinking that this could be a fun opportunity to play with some of the
weirder overloads that Python allows, I decided to implement this on my
own.

This turned out to be surprisingly easy, and I was even able to get
around the 2N+1 dashes rule:

	>>> from analogInt import *
	>>> (I---I) == 3
	True
	>>> (I----I) / (I--I)
	(I--I)
	>>> (I--I) + (I--I)
	(I----I)
	>>> (I---I) - (I-I)
	(I--I)
	>>> (I---I) / (II)
	ZeroDivisionError: integer division or modulo by zero
	>>> (I---I) ** (I--I)
	(I---------I)

[PyAnalogInt](https://github.com/rdeits/PyAnalogInt) at github. 

Next up: implementing 2- and 3-dimensional analog literals in Python...
