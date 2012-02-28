---
layout: page
title: Playing with Legos, and other activities
---
{% include JB/setup %}

<a href="http://www.flickr.com/photos/26769928@N02/sets/72157627194290064/" target="_blank"><img src="/img/header.jpg" width="100%"></a>

<br>
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

