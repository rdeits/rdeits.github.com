---
layout: post
title: "PyAudio with Homebrew"
category: Yak Shaving
tags: [PyAudio, Homebrew, Mac, Python]
---
{% include JB/setup %}

I'm trying to get pyaudio to play nicely with my Homebrew Python 2.7
installation. Apparently this is difficult...

	pip install pyaudio

This failed with:

	Downloading/unpacking pyaudio
	  Downloading pyaudio-0.2.4.tar.gz (80Kb): 80Kb downloaded
	  Running setup.py egg_info for package pyaudio
		
	Installing collected packages: pyaudio
	  Running setup.py install for pyaudio
		building '_portaudio' extension
		/usr/bin/llvm-gcc -fno-strict-aliasing -fno-common -dynamic -O3
			-march=core2 -w -pipe -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
			-DMACOSX=1
			-I/usr/local/Cellar/python/2.7.2/Frameworks/Python.framework/Versions/2.7/include/python2.7
			-c src/_portaudiomodule.c -o
			build/temp.macosx-10.4-x86_64-2.7/src/_portaudiomodule.o
			-fno-strict-aliasing
		src/_portaudiomodule.c:35:25: error: pa_mac_core.h: No such file or directory

Downloaded and ran the binary installer. This still didn't let me import pyaudio.

I'm going to try installing from source. To get the portaudio source, I did:

	svn co https://www.portaudio.com/repos/portaudio/trunk ./portaudio
	cd portaudio
	./configure
	make 
	sudo make install

Then downloaded and extracted pyaudio and did

	python setup.py install

This fails with

	/usr/bin/llvm-gcc -fno-strict-aliasing -fno-common -dynamic -O3
		-march=core2 -w -pipe -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
		-DMACOSX=1
		-I/usr/local/Cellar/python/2.7.2/Frameworks/Python.framework/Versions/2.7/include/python2.7
		-c src/_portaudiomodule.c -o
		build/temp.macosx-10.4-x86_64-2.7/src/_portaudiomodule.o
		-fno-strict-aliasing
	src/_portaudiomodule.c:35:25: error: pa_mac_core.h: No such file or directory

I found that missing file at:<br>
[http://www.portaudio.com/trac/browser/portaudio/branches/v19-devel/include/pa_mac_core.h?rev=1074](http://www.portaudio.com/trac/browser/portaudio/branches/v19-devel/include/pa_mac_core.h?rev=1074) and downloaded it to the same folder as setup.py. This didn't work, so I copied it to /usr/bin. Also didn't work. Sigh.

Next step, based on [https://github.com/mxcl/homebrew/pull/3926](https://github.com/mxcl/homebrew/pull/3926):

	brew install portaudio
	sudo brew link portaudio
	pip install pyaudio

This fails with:

	/usr/bin/llvm-gcc -fno-strict-aliasing -fno-common -dynamic -O3
		-march=core2 -w -pipe -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
		-DMACOSX=1
		-I/usr/local/Cellar/python/2.7.2/Frameworks/Python.framework/Versions/2.7/include/python2.7
		-c src/_portaudiomodule.c -o
		build/temp.macosx-10.4-x86_64-2.7/src/_portaudiomodule.o
		-fno-strict-aliasing

	In file included from src/_portaudiomodule.c:35:

	/usr/local/include/pa_mac_core.h:93: error: expected ‘=’, ‘,’, ‘;’,
		‘asm’ or ‘__attribute__’ before ‘PaMacCore_GetStreamInputDevice’

	/usr/local/include/pa_mac_core.h:102: error: expected ‘=’, ‘,’, ‘;’,
		‘asm’ or ‘__attribute__’ before ‘PaMacCore_GetStreamOutputDevice’

I'm going to try to update the formula:

	sudo brew remove portaudio
	brew update
	brew install portaudio
	sudo brew link portaudio
	pip install pyaudio

Same error. I'm looking at this file to see what's up with it. I think I must be pulling in the wrong version of portaudio, not the homebrew one. How do I uninstall it?
cd into the source directory and do

	sudo make uninstall

Now pip install pyaudio can't find portaudio.h. I did

	cd /usr/local/Cellar/portaudio/19.20111121/include
	sudo ln -s /usr/local/Cellar/portaudio/19.20111121/include/portaudio.h
		/usr/local/include/portaudio.h

Now pip install still gives me the same error about pa_mac_core.h.

Okay, new strategy. I edited my portaudio.rb formula to be this: [portaudio.rb](https://github.com/beniamino38/homebrew/blob/8e5307b42d427f8b142aea9277c431d01cafbaf1/Library/Formula/portaudio.rb#L7) I then did:

	brew install portaudio
	sudo brew link portaudio
	pip install pyaudio

SUCCESS!!
