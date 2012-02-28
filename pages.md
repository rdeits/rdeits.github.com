---
layout: page
title: Pages 
header: Pages
group: navigation
---
{% include JB/setup %}

* [Home](index.html)
* [Archive](archive.html)
* [Yak Shaving](pages/yak_shaving.html)

<h2>All Pages</h2>
<ul>
{% assign pages_list = site.pages %}
{% include JB/pages_list %}
</ul>
