---
layout: default
title: Uses
sections:
  - title: Devices
    items:
      - 14" MacBook Pro (M3 Pro)
      - iPad mini for reading and sketching
      - Leica Q for quick documentation
  - title: Software
    items:
      - Figma, Rhino, and Shapr3D for spatial design
      - Notion for shared systems and lightweight docs
      - Obsidian for private notes and links
      - VS Code + Zed for writing code
  - title: Everyday Tools
    items:
      - Traveler’s Notebook + Muji pens
      - Kindle Paperwhite
      - Audio-Technica M50x headphones
  - title: Clothing
    items:
      - Engineered Garments work jackets
      - Nike Zoom GT Cut 3 for the court
      - A rotation of vintage-inspired watches
---

<section>
  <h1>Uses</h1>
  <div class="uses-sections">
    {% for section in page.sections %}
    <div class="uses-section">
      <h2>{{ section.title }}</h2>
      <ul>
        {% for item in section.items %}
        <li>{{ item }}</li>
        {% endfor %}
      </ul>
    </div>
    {% endfor %}
  </div>
</section>
