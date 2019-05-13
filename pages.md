---
layout: page
title: Pages
header: Pages
group: navigation
---
{% include JB/setup %}

* [Home](index.html)
* [About](pages/about/)
* [Archive](archive/)
* [Yak Shaving](pages/yak_shaving/)

<h2>All Pages</h2>
<ul>
{% assign pages_list = site.pages %}
{% include JB/pages_list %}
</ul>
