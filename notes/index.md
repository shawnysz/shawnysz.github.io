---
layout: page
title: Notes
description: "Fragments, quotes, and sketches before they grow into longer essays."
---

# Notes
<a class="subtitle" href="/">By Shawn Zhou</a>

{% assign notes = site.notes | sort: 'date' | reverse %}

<ul>
{% for note in notes %}
  <li><a href="{{ note.url }}">{{ note.title }}</a></li>
{% endfor %}
</ul>
