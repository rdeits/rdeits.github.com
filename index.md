---
layout: home
title: Playing with Legos (and other activities)
feed: http://blog.robindeits.com/atom.xml
---
{% include JB/setup %}

<ul class="posts">
{% assign posted = false %}
{% for post in site.posts %}
	{% unless posted %}
		{% unless post.category == "Yak Shaving" %}
			{% assign posted = true %}
			{% assign first_post = post %}
		{% endunless %}
	{% endunless %}
{% endfor %}

<span>{{ first_post.date | date_to_string }}</span> &raquo; 
<h1><a href="{{ BASE_PATH }}{{ first_post.url }}">{{ first_post.title }}</a></h1>
{{ first_post.content }}
</ul>

# All Posts
<ul class="posts">
  {% for post in site.posts %}
	{% if post.category != "Yak Shaving" %}
		<span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a><br>
	{% endif %}
  {% endfor %}
</ul>

