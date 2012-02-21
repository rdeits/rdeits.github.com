---
layout: page
title: Playing with Legos, and other activities
---
{% include JB/setup %}

<img src="/img/header.jpg" width="100%">

<br>
<ul class="posts">
{% assign first_post = site.posts.first %}
<span>{{ first_post.date | date_to_string }}</span> &raquo; 
<h1><a href="{{ BASE_PATH }}{{ first_post.url }}">{{ first_post.title }}</a></h1>

{{ first_post.content }}
</ul>

# All Posts
<ul class="posts">
  {% for post in site.posts %}
    <span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a><br>
  {% endfor %}
</ul>

