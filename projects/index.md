---
layout: default
title: Projects
projects:
  - title: Field Lab
    description: Adaptive workplace and fabrication studio focused on fast prototyping for spatial ideas.
  - title: Neighborhood Residences
    description: A multi-building housing concept exploring modular construction, daylight, and flexible shared space.
  - title: Systems Atlas
    description: A long-form research guide that maps how physical and digital systems overlap inside civic projects.
---

<section>
  <h1>Projects</h1>
  <div class="projects-list">
    {% for project in page.projects %}
    <article class="project-card">
      <h2>{{ project.title }}</h2>
      <p>{{ project.description }}</p>
    </article>
    {% endfor %}
  </div>
</section>
