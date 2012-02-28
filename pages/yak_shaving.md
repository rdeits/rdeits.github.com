---
layout: page
title: "Yak Shaving"
---
{% include JB/setup %}

From [wiktionary](http://en.wiktionary.org/wiki/yak_shaving)

><b>yak shaving</b>:
>
>1. (idiomatic) Any apparently useless activity which, by allowing you to overcome intermediate difficulties, allows you to solve a larger problem.<br>
>_I was doing a bit of yak shaving this morning, and it looks like it might have paid off._
>2. (idiomatic) The actually useless activity you do that appears important when you are consciously or unconsciously procrastinating about a larger problem.<br>
>_I thought I'd get more work done if I just fixed a problem with my .emacs file, but then I spent the whole afternoon yak shaving._

# All Posts
<ul class="posts">
  {% for post in site.posts %}
	{% if post.category == "Yak Shaving" %}
		<span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a><br>
	{% endif %}
  {% endfor %}
</ul>
