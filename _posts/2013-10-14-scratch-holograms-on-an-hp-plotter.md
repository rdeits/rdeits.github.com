---
layout: post
title: "Scratch Holograms on an HP Plotter"
category: Projects
tags: []
---
{% include JB/setup %}

I've been interested in abrasion or scratch holography for a few years, and have used it in a few art and engineering projects. I've written about it before [here](/2011/09/26/scratch-holograms/) and [here](/2012/02/20/more-scratch-holograms/). The basic concept is that a hologram of 3-dimensional points of light is created from the reflections of a single light source on curved scratches in a flat material. The effects can be both beautiful and mathematically interesting, and the level of detail that can be created is impressive:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/matt-brand-knot.jpg" width="100%">
	<figcaption>Specular Hologram by Matt Brand, as seen in MoMath New York. <a href="http://www.zintaglio.com/momath.html">Source</a></figcaption>
</figure>

Creating these holograms by hand, however, is pretty tedious, since each point of light requires a separate arc with a precise position and radius. Naturally, I'd like to automate the actual creation of the scratches so that I don't have to make them by hand. I've had some success with doing this on a CNC milling machine using a vinyl cutting bit, as I mentioned in a [previous post](/2012/02/20/more-scratch-holograms/). I'd prefer, though, to be able to do this in my own home, so I've been searching for a smaller, cheaper, and lighter tool to do the same job. 

# Enter the Plotter

My friend [phleb](http://phlebowtish.wordpress.com/2013/02/22/a-guide-to-setting-up-a-hp7475a-on-a-modern-machine/) managed to get his hands on an HP7475A pen plotter, a 2D drawing machine which predates most modern printers. The plotter has a pen holder which moves vertically, a stepper motor to move the pen left and right across the page, and a stepper motor to move the paper forward and backward. Naturally, my first thought on seeing this device was that it could be the perfect machine for making scratch holograms. 

## Mounting the tools

The HP7475A is designed to use special pens which look something like this: 

<figure class='onecol-figure' style="width:50%;">
	<img src="/img/2013-10-14-micro-scratches/hp-plotter-pen.jpg" width="100%">
	<figcaption>HP Plotter Pen. <a href="http://www.smithdrafting.com/plottingpens.htm">Source</a></figcaption>
</figure>

Originally, I decided to manufacture a piece to hold a scratch cutting tool in place of the pen, based on [this 3D model of an HP pen](http://www.practicalmachinist.com/vb/general/cnc-mill-6-plotter-pen-203343/). What I came up with was this: 

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_1782.jpg" width="100%">
	<figcaption>Custom cutting tool holder for HP Plotter with nail inserted.</figcaption>
</figure>

I can mount a nail or compass point for etching, or a piece of pencil lead for drawing, and the set screw in the side holds the tool in place:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_1770.jpg" width="100%">
	<figcaption>Cutting tool holder with pencil lead.</figcaption>
</figure>

The holder mounts into the plotter just like a pen would:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_1774.jpg" width="100%">
	<figcaption>HP 7475A plotter with custom cutting tool.</figcaption>
</figure>

Using the wonderfully-named [chiplotle](http://music.columbia.edu/cmc/chiplotle/) library, I was able to command the plotter to draw basic geometric shapes and text in Python. Here's the result:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_1767.jpg" width="100%">
</figure>

This was tremendously promising! Unfortunately, using this setup to create scratch holograms didn't work at all. Scratch holograms require extremely clean, smooth scratches, as explained by Willeam Beaty in [his original post about scratch holograms](http://amasci.com/amateur/hand1.html). The perfectly vertical orientation of the cutting tool in my holder, however, caused the tool to skip and jump as it moved across the plastic, resulting in jagged and unusable scratches. Instead, I needed a cutting tool that would smoothly drag across the surface without skipping. 

## Vinyl cutters

Another use for devices like my HP plotter is in cutting vinyl for signs or other artistic projects. Doing this requires a special vinyl cutting tool, which consists of a tiny, extremely sharp blade mounted on a pivot. The tip of the blade is a millimeter or two off the axis of the pivot, so the tip is always dragged behind when the cutter is moved, resulting in a very clean cut in any direction. These cutters also come in cases designed to fit into plotters like mine, which look like this:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/ebay_cutter.jpg" width="100%">
	<figcaption>Vinyl cutting tool for HP Plotter. <a href="http://www.ebay.com/itm/11-5mm-Blade-Holder-for-Roland-Cutting-Plotter-Cutter-3-pcs-45-Blade-Knife-/121074873476?ssPageName=ADME:L:OC:US:3160">Source (ebay).</a></figcaption>
</figure>

The vinyl cutter seemed to perfectly solve the problem of the tool skipping as it moved.

# Results

So, did it work? Er...no. Not at all. I'll demonstrate what happened, and then try to explain why. Here's an image of the results:

<figure class='onecol-figure' style="width:80%;">
	<img src="/img/2013-10-14-micro-scratches/DSC_1791.jpg" width="100%">
	<figcaption>Two scratches, illuminated by a point light source. The top scratch was created by the vinyl cutter held in the HP 7475A plotter, and the lower scratch was created by hand using a compass point.</figcaption>
</figure>

You can see two illuminated scratches in the above photo. The lower scratch, created by hand, shows a relatively small, brilliant spot of reflected light. The upper scratch, created on the plotter, shows a dull smear of light. Scratch holograms require that each scratch arc produce a single, concentrated reflection of light, so the upper arc will produce a very poor holographic image. All of my attempts with the plotter resulted in similar, dull scratches which failed to produce clear holograms.

## Understanding the results

Why does the plotter produce such bad scratches? To figure this out, I needed to wait until I had the mechanism to examine the microscopic structure of the scratches themselves. My recent experiments [building a microscope](/2013/09/27/more-microscope-or-how-not-to-build-a-linear-bearing) provided exactly the tool I needed. First, let's look at the tools I'm using. For my holograms, I'm primarily using a compass point to etch the arcs. My compass point looks like this under a microscope:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_2592.jpg" width="100%">
	<figcaption>Compass point, magnified approximately 20X.</figcaption>
</figure>

I've also had success using a different, duller compass point, shown here:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_2589.jpg" width="100%">
	<figcaption>Another compass point, magnified approximately 20X.</figcaption>
</figure>

Finally, here's the vinyl cutter's tip, which is much sharper than either of the compass points:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_2593.jpg" width="100%">
	<figcaption>Vinyl cutting bit, magnified approximately 20X.</figcaption>
</figure>

Here's a magnified image of a scratch created by hand using the first compass point:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_2662.jpg" width="100%">
	<figcaption>Scratch in polyester sheet made by compass point controlled by hand. Magnified approx. 20X.</figcaption>
</figure>

And here's a scratch in the same material using the vinyl cutter, still controlled by hand:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_2672.jpg" width="100%">
	<figcaption>Scratch in polyester sheet made by vinyl cutter controlled by hand. Magnified approx. 20X.</figcaption>
</figure>

The dark line through the center of the scratch is, I believe, the flat surface at the bottom of the scratch. It's much narrower than in the previous photo since the vinyl cutter has a much sharper point. Both of these scratches produce acceptable holographic reflections in my experiments.

Now, however, let's look at the result from the HP plotter using the vinyl cutter:

<figure class='onecol-figure'>
	<img src="/img/2013-10-14-micro-scratches/DSC_2661.jpg" width="100%">
	<figcaption>Scratch in polyester sheet made by vinyl cutter controlled by HP 7475A plotter. Magnified approx. 20X.</figcaption>
</figure>

This scratch is a mess, and now we can begin to understand why the reflection produced is so poor. The twisted, rough edges provide many locations for weak reflections of light, so we get a smeared-out, dull reflection of our illumination. None of these problems were present with the hand-held vinyl cutter, so the problem must stem from imprecision in the movements of the plotter. 

# Conclusions

I think that this is probably the end for my HP plotter as a scratch hologram device. Without serious hardware modifications, it doesn't seem to be precise enough to create the clean arcs that I need. I'm sure I'll find some other use for it down the road, but for now it'll have to be restricted to [more two-dimensional art forms](http://www.youtube.com/watch?v=VRGO8613g1I). 