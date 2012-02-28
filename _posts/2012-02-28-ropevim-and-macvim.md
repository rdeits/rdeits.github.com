---
layout: post
title: "Ropevim and MacVim"
category: Yak Shaving
tags: [Vim, MacVim, Rope, Python]
---
{% include JB/setup %}

I'm trying to get rope to work with omnicomplete in Vim. To do this, I want to use [rope-omni](https://github.com/rygwdn/rope-omni) to provide the omnifunc.

	easy_install ropevim


This fails because macvim still can't import ropevim, even though I have it installed. The problem seems to be that macvim is linked against the system python, not the homebrew python (through which everything else is installed). I don't like this.

Okay, here goes... following these instructions:
[http://buntin.org/2011/05/12/os-x-hombrew-macvim-and-python-2-7-1-troubles/](http://buntin.org/2011/05/12/os-x-hombrew-macvim-and-python-2-7-1-troubles/)

Uninstalled MacVim. Then did:

	cd /System/Library/Frameworks/Python.framework/Versions/
	sudo rm Current
	sudo ln -s /usr/local/Cellar/python/2.7.2/Frameworks/Python.framework/Versions/Current
	brew install macvim
	brew linkapps

Cool! Now the macvim python path seems to be using the /usr/local/Cellar python, not the system one, as desired.

Now I can have successful auto-completion of class methods (such as
self.abc, etc), which previously didn't work with the built-in
pythoncomplete#Complete. I've saved myself literally seconds of typing
with my hours of research and hacking!
