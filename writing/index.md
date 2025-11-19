---
layout: default
title: Writing
---

<section>
  <h1>Writing</h1>
  <div class="writing-list">
    {% assign posts = site.posts | sort: 'date' | reverse %}
    {% for post in posts %}
    <article class="writing-entry">
      <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %-d, %Y" }}</time>
      {% if post.excerpt %}
      <p>{{ post.excerpt | strip_html | truncate: 140 }}</p>
      {% endif %}
    </article>
    {% endfor %}
  </div>
</section>
