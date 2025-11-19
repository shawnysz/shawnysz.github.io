---
layout: page
title: Journal
description: "A running log of milestones, notes, and fragments."
---

# Journal
<a class="subtitle" href="/">By Shawn Zhou</a>

A timeline of what’s happening in my life — milestones, small notes, things I’m learning, and fragments not polished enough to become essays. Updated whenever something feels worth remembering.

{% assign entries = site.journal | sort: 'date' | reverse %}

{% if entries.size > 0 %}
<ul>
{% for entry in entries %}
  <li><a href="{{ entry.url }}">{{ entry.title }}</a></li>
{% endfor %}
</ul>
{% else %}
<p>No journal entries published yet.</p>
{% endif %}
