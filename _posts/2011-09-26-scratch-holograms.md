---
layout: post
title: "Scratch Holograms"
category: 
tags: []
---
{% include JB/setup %}

When I first came across William Beaty's technique for <a href="http://amasci.com/amateur/holo1.html">"abrasion holograms"</a> which can be used to quickly create holographic images by hand, I was immediately hooked. The idea of the technique is to create a 3D object by making  a series of circular scratches in a plastic sheet. When viewed in the sun, the light reflected by each scratch creates an image of a point of light above or below the surface of the plastic. The radius of the arc sets the depth of the point, and its orientation (concave up or down) determines whether the point is above or below the plane. The easiest way to make these is with a compass, but with anything more complex than a simple flat shape it rapidly becomes difficult to determine the correct location and radius for each arc in a 3D shape.

To combat this, I decided to create a method for generating hologram "patterns" which could be easily traced by hand. My initial version starts out with a 3D model of an object in <a href="http://sketchup.google.com/">Google SketchUp</a>, a simple free modeling program. A slightly modified version of the <a href="http://rhin.crai.archi.fr/rld/plugin_details.php?id=101">dataexporter </a>script extracts the edge locations from the model, and then a Python script translates those edges into a pattern which can be printed and used to trace out a hologram by hand.

Here's an example:

* The original object, a tilted 3D model of a cube:
<img src="/img/2011-09-26/cube_model.png" width="75%"/>
* The scratch pattern generated from the 3D model, ready to be printed and traced. The blue arcs are for points below the plastic; the red ones are for points above it.
<img src="/img/2011-09-26/cube_tilted.png" width="75%"/>
* The final result, scratched into polyester film by hand:
<p><object width="420" height="315"><param name="movie" value="http://www.youtube.com/v/0RP-PyvZ4eE?version=3&amp;hl=en_US&amp;rel=0"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/0RP-PyvZ4eE?version=3&amp;hl=en_US&amp;rel=0" type="application/x-shockwave-flash" width="420" height="315" allowscriptaccess="always" allowfullscreen="true"></embed></object></p>
