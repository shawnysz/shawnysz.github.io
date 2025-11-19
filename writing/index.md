---
layout: page
title: Writing
description: "Long-form writing, notes, and thoughts I’m working through."
---

# Writing
<a class="subtitle" href="/">By Shawn Zhou</a>

Here’s a list of my writing:

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" | sort: "name" | reverse %}

{% for year in posts_by_year %}
## {{ year.name }}

<ul>
  {% for post in year.items %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

{% endfor %}
