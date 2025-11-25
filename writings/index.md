---
title: "Writings"
description: "Long-form essays and journal fragments."

layout: "default"
type: "writing"
status: "published"
order: null

canonical: true
noindex: false

theme: "auto"

# Custom fields
---

# Writings
<a class="subtitle" href="/">By Shawn Zhou</a>

My writings gather both longer ideas and shorter fragments as they shift over time. Essays capture the full structure and decisions behind a project, while journal entries stay closer to the moment they were written.

{% assign essays_by_year = site.essays | group_by_exp: "essay", "essay.date | date: '%Y'" | sort: "name" | reverse %}

{% if essays_by_year.size > 0 %}
## Essays

Structure, decisions, and long-form thinking. These slower pieces take time to build and time to absorb.

{% for year in essays_by_year %}
### {{ year.name }}

<ul>
  {% for essay in year.items %}
    <li><a href="{{ essay.url }}">{{ essay.title }}</a></li>
  {% endfor %}
</ul>

{% endfor %}
{% else %}
<p>No essays published yet.</p>
{% endif %}

{% assign entries = site.journals | sort: 'date' | reverse %}

{% if entries.size > 0 %}
## Journal

A timeline of milestones, small notes, things I’m learning, and fragments not polished enough to become essays.

<ul>
{% for entry in entries %}
  <li><a href="{{ entry.url }}">{{ entry.title }}</a></li>
{% endfor %}
</ul>
{% else %}
<p>No journal entries published yet.</p>
{% endif %}
