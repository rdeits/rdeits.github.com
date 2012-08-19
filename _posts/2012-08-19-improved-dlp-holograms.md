---
layout: post
title: "Improved DLP Holograms"
category: 
tags: []
---
{% include JB/setup %}

Back in May, I wrote about a (mostly crazy) idea to create a [programmable holographic display](/2012/05/20/programmable-holograms/) using a Digital Micromirror Device (DMD), like the one found in a DLP projector or TV. There's a lot more background in the original post ([here](/2012/05/20/programmable-holograms/)), but the essence is that a DMD consists of an array of thousands or millions of tiny mirrors, each of which can be independently moved to one of two angles. By placing your eyes at the right spot above such a device, you can use a pair of those mirrors to create the *image* of a single point of light hovering below the DMD itself, like this:

<object data="/img/2012-05-21/DLP_holo_point.svg" type="image/svg+xml" style="height:350px">
</object>

At [the end of that post](/2012/05/20/programmable-holograms/#conclusion), I explained that a major limitation of this device is that, because the mirror angles are fixed, "we can't create 3D shapes, we can just display flat objects in a 3D space." On further reflection, this turns out to be entirely untrue. 

The apparent depth of the point image is set by a number of factors, but one of them is distance between the mirrors which reflect the light to each eye. My previous post implicitly assumed that the mirrors would need to be adjacent, but this is entirely unnecessary. Any pair of mirrors should be able to create a virtual point whose depth is proportional to the distance between them. 

We can see this easily by looking at two different pairs of mirrors and the image point each creates:

<object data="/img/2012-08-19/DLP_multi_point.svg" type="image/svg+xml" style="height:350px">
</object>

(For an explanation of why I can be so choosy about which particular light rays I've drawn in <font color="ff6464">red</font> and <font color="6464ff">blue</font> and why each eye doesn't see light that's meant for the other eye, see my [rather tedious mathematical explanation in the previous post](/2012/05/20/programmable-holograms/#problem_1_seeing_all_the_mirrors))

Note how the image point from the inner pair of pair of mirrors appears much closer to the plane of the mirrors than the point from the outer pair. That's exactly the effect I'm referring to: by choosing the right pair of mirrors, we create points at a wide variety of possible depths. That means that we can create a fully 3D shape, as long as it is composed entirely of points of light.

This does not, however, give us the ability to create arbitrarily many points. As far as I can tell, we would be limited to one point per row of pixels, otherwise there's no way for the viewer to identify where the image point should be. Take this example:

<object data="/img/2012-08-19/DLP_multi_point_confused.svg" type="image/svg+xml" style="height:350px">
</object>

Turning three mirrors "on" creates two virtual points. Each additional mirror in the row will create even more points, almost certainly leading to total confusion of the viewer. So, we're still limited, but significantly less so than I had previously stated.

Of course, I still can't be sure exactly how well your brain would interpret such a hologram. That will have to wait for the physical incarnation of this device, if it ever comes.