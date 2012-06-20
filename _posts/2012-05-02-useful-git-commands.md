---
layout: post
title: "Useful git commands"
category: Yak Shaving
tags: []
---
{% include JB/setup %}

Useful git tricks I've learned that I always end up coming back to:

## Replace master with another branch:
From [stackoverflow](http://stackoverflow.com/questions/2862590/how-to-replace-master-branch-in-git-entirely-from-another-branch):

	git checkout seotweaks
	git merge -s ours master
	git checkout master
	git merge seotweaks

## Update the submodules in a newly cloned project:
From the [git book](http://book.git-scm.com/5_submodules.html):

	git submodule init
	git submodule update
