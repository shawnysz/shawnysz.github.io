#!/usr/bin/env python3
"""
Static site generator for shawnysz.github.io
Converts Markdown files to HTML using Jinja2 templates
"""

import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import markdown
    import yaml
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install markdown pyyaml jinja2")
    exit(1)


class SiteBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.content_dir = self.root_dir / "content"
        self.templates_dir = self.root_dir / "templates"
        self.dist_dir = self.root_dir / "dist"
        self.assets_dir = self.root_dir / "assets"

        # Setup Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(str(self.templates_dir)))
        self.base_template = self.env.get_template('base.html')

        # Markdown converter (disable smarty to prevent smart quotes)
        self.md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.fenced_code'
            ],
            extension_configs={
                'markdown.extensions.extra': {
                    'enable': ['abbr', 'attr_list', 'def_list', 'footnotes', 'tables']
                }
            }
        )

    def parse_frontmatter(self, file_path):
        """Parse YAML front matter from Markdown file"""
        content = file_path.read_text(encoding='utf-8')

        # Match YAML front matter
        match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)

        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                body = match.group(2)
                return frontmatter or {}, body
            except yaml.YAMLError as e:
                print(f"WARNING:  YAML error in {file_path}: {e}")
                return {}, match.group(2)

        # No front matter found
        print(f"WARNING:  No front matter in {file_path}")
        return {}, content

    def markdown_to_html(self, markdown_text):
        """Convert Markdown to HTML"""
        self.md.reset()
        return self.md.convert(markdown_text)

    def get_output_path(self, md_file, section=None):
        """Generate output HTML path from Markdown file path"""
        relative = md_file.relative_to(self.content_dir)

        # Replace .md with /index.html for clean URLs
        # e.g., writings/essays/2024-11-25-Against the Void.md
        #    -> writings/essays/2024-11-25-Against the Void/index.html
        parts = list(relative.parts)
        filename = parts[-1].replace('.md', '')
        parts[-1] = filename
        parts.append('index.html')

        return self.dist_dir / Path(*parts)

    def validate_date_consistency(self, file_path, frontmatter):
        """Validate filename date matches front matter date"""
        filename = file_path.stem
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)

        if date_match:
            filename_date = date_match.group(1)
            frontmatter_date = str(frontmatter.get('date', ''))

            if filename_date not in frontmatter_date:
                print(f"WARNING:  Date mismatch in {file_path.name}")
                print(f"   Filename: {filename_date}, Front matter: {frontmatter_date}")

    def build_page(self, md_file, is_home=False):
        """Build a single page from Markdown file"""
        frontmatter, body = self.parse_frontmatter(md_file)

        # Validate date consistency
        self.validate_date_consistency(md_file, frontmatter)

        # Convert Markdown to HTML
        html_content = self.markdown_to_html(body)

        # Prepare context for template
        context = {
            'title': frontmatter.get('title', ''),
            'description': frontmatter.get('description', ''),
            'date': frontmatter.get('date', ''),
            'content': html_content,
            'is_home': is_home,
            'body_class': 'home' if is_home else ''
        }

        # Render template
        html = self.base_template.render(**context)

        # Determine output path
        if is_home:
            output_path = self.dist_dir / 'index.html'
        else:
            output_path = self.get_output_path(md_file)

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding='utf-8')

        return frontmatter, output_path

    def collect_items(self, section):
        """Collect all items from a section (writings, projects, collections)"""
        section_dir = self.content_dir / section

        if not section_dir.exists():
            return []

        items = []

        for md_file in section_dir.rglob('*.md'):
            frontmatter, _ = self.parse_frontmatter(md_file)

            # Calculate URL
            relative = md_file.relative_to(self.content_dir)
            parts = list(relative.parts)
            filename = parts[-1].replace('.md', '')
            parts[-1] = filename
            url = '/' + '/'.join(parts)

            # Extract category (e.g., 'essays', 'journal', 'notes')
            category = relative.parts[1] if len(relative.parts) > 1 else 'other'

            items.append({
                'title': frontmatter.get('title', md_file.stem),
                'date': frontmatter.get('date', ''),
                'url': url,
                'category': category,
                'file_path': md_file
            })

        # Sort by date (newest first)
        items.sort(key=lambda x: x['date'], reverse=True)

        return items

    def group_items_by_category(self, items):
        """Group items by category"""
        grouped = defaultdict(list)

        for item in items:
            grouped[item['category']].append(item)

        return grouped

    def build_index_page(self, section):
        """Build index page for a section (Projects/Writings/Collections)"""
        items = self.collect_items(section)

        if not items:
            print(f"WARNING:  No items found for section: {section}")
            return

        # Group by category
        grouped = self.group_items_by_category(items)

        # Build HTML content
        html_parts = [f'<h1>{section.title()}</h1>\n']

        # Category display names
        category_names = {
            'essays': 'Essays',
            'journal': 'Journal',
            'notes': 'Notes',
            'design-build': 'Design + Build',
            'development': 'Development + Investment',
            'frameworks': 'Frameworks',
            'retired': 'Previously Used',
        }

        for category, category_items in grouped.items():
            category_name = category_names.get(category, category.replace('-', ' ').title())
            html_parts.append(f'<h2>{category_name}</h2>\n<ul>\n')

            for item in category_items:
                html_parts.append(f'  <li>\n')
                html_parts.append(f'    <a href="{item["url"]}">{item["title"]}</a>\n')

                if item['date']:
                    # Format date
                    try:
                        date_obj = datetime.fromisoformat(str(item['date']))
                        formatted_date = date_obj.strftime('%B %d, %Y')
                        html_parts.append(f'    <span class="subtitle">{formatted_date}</span>\n')
                    except:
                        html_parts.append(f'    <span class="subtitle">{item["date"]}</span>\n')

                html_parts.append(f'  </li>\n')

            html_parts.append('</ul>\n')

        html_content = ''.join(html_parts)

        # Render with template
        context = {
            'title': section.title(),
            'description': f'{section.title()} by Shawn Zhou',
            'content': html_content,
            'is_home': False,
            'body_class': ''
        }

        html = self.base_template.render(**context)

        # Write to dist/section/index.html
        output_path = self.dist_dir / section / 'index.html'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding='utf-8')

        print(f"OK: Built {section}/index.html ({len(items)} items)")

    def build(self):
        """Main build function"""
        print("Building site...\n")

        # 1. Clean dist/
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir()

        # 2. Build homepage
        home_file = self.root_dir / 'index.md'
        if home_file.exists():
            self.build_page(home_file, is_home=True)
            print("OK: Built homepage")
        else:
            print("WARNING:  No index.md found")

        # 2.5. Build 404 page
        error_file = self.root_dir / '404.md'
        if error_file.exists():
            frontmatter, body = self.parse_frontmatter(error_file)
            html_content = self.markdown_to_html(body)
            context = {
                'title': frontmatter.get('title', '404'),
                'description': frontmatter.get('description', ''),
                'content': html_content,
                'is_home': False,
                'body_class': ''
            }
            html = self.base_template.render(**context)
            output_path = self.dist_dir / '404.html'
            output_path.write_text(html, encoding='utf-8')
            print("OK: Built 404 page")

        # 3. Build all content pages
        content_count = 0
        for md_file in self.content_dir.rglob('*.md'):
            self.build_page(md_file)
            content_count += 1

        print(f"OK: Built {content_count} content pages")

        # 4. Build index pages
        for section in ['writings', 'projects', 'collections']:
            self.build_index_page(section)

        # 5. Copy static assets
        if self.assets_dir.exists():
            dist_assets = self.dist_dir / 'assets'
            shutil.copytree(self.assets_dir, dist_assets)
            print("OK: Copied assets")

        print(f"\nSUCCESS: Build complete! Output in {self.dist_dir}/")
        print(f"   To preview: cd {self.dist_dir} && python -m http.server 8000")


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()
