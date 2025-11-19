---
layout: page
title: Essays
description: "Structure, decisions, and long-form thinking."
---

# Essays
<a class="subtitle" href="/">By Shawn Zhou</a>

Structure, decisions, and long-form thinking. I write about systems, design, real estate, and the mechanics behind how things work. These are slower, deeper pieces — the kind that take time to build and time to absorb.

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" | sort: "name" | reverse %}

{% if posts_by_year.size > 0 %}
{% for year in posts_by_year %}
## {{ year.name }}

<ul>
  {% for post in year.items %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

{% endfor %}
{% else %}
<p>No essays published yet.</p>
{% endif %}
