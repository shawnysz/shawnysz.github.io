---
title: "Writings"
description: "Notes, essays, and journal entries — ideas and observations across life and thinking."
layout: "default"
type: "writing"
status: "published"
order: null
canonical: true
noindex: false
theme: "auto"
---

# Writings
<a class="subtitle" href="/">By Shawn Zhou</a>

Ideas, observations, and fragments — capturing how I see the world.

## Notes

Short thoughts, fragments, and observations. Unpolished, immediate, close to the moment.

{% assign notes = site.writings | where_exp: "item", "item.path contains 'notes'" | sort: 'date' | reverse %}
{% if notes.size > 0 %}
<ul>
{% for note in notes %}
  <li><a href="{{ note.url }}">{{ note.title }}</a></li>
{% endfor %}
</ul>
{% else %}
<p>No notes published yet.</p>
{% endif %}

## Essays

Longer pieces with structure and intention. Deep thinking that takes time to build and time to absorb.

{% assign all_essays = site.writings | where_exp: "item", "item.path contains 'essays'" %}
{% assign essays_by_year = all_essays | group_by_exp: "essay", "essay.date | date: '%Y'" | sort: "name" | reverse %}

{% if essays_by_year.size > 0 %}
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

## Journal

Travel, restaurants, experiences, and observations. A record of places, moments, and things worth remembering.

{% assign journal = site.writings | where_exp: "item", "item.path contains 'journal'" | sort: 'date' | reverse %}
{% if journal.size > 0 %}
<ul>
{% for entry in journal %}
  <li><a href="{{ entry.url }}">{{ entry.title }}</a></li>
{% endfor %}
</ul>
{% else %}
<p>No journal entries published yet.</p>
{% endif %}
