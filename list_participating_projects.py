import csv
from collections import defaultdict
from html import escape

# Identify the input CSV and the output HTML fragment.
input_file = 'projects.csv'
output_file = 'interactive_projects_grouped.html'


PAGE_STYLE = """
<style type="text/css">
    div#content.core {
        max-width: 100%;
        padding: 0;
    }
    .content-right {
        margin: 0;
    }
    h2 {
        color: #500000;
        border-bottom: 2px solid #500000;
        padding-bottom: 5px;
        margin-top: 40px;
    }
    details.major-section {
        margin: 30px 0;
        border: none;
        padding: 0;
        background-color: transparent;
        box-shadow: none;
    }
    details.major-section > summary {
        color: #500000;
        border-bottom: 2px solid #500000;
        padding-bottom: 5px;
        margin-top: 40px;
        margin-bottom: 20px;
        font-size: 1.5em;
        font-weight: bold;
        list-style-position: outside;
    }
    details.major-section > summary:hover {
        color: #500000;
    }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 20px;
        align-items: start;
    }
    details {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    details[open] {
        border-color: #bbb;
    }
    summary {
        font-weight: 600;
        font-size: 1.1em;
        cursor: pointer;
        outline: none;
        list-style-position: inside;
    }
    summary:hover {
        color: #0056b3;
    }
    .content {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #eee;
        font-size: 0.95em;
    }
    .meta {
        font-size: 0.9em;
        color: #444;
        margin-bottom: 12px;
        background: #f0f4f8;
        padding: 10px;
        border-radius: 6px;
    }
    .meta strong {
        color: #111;
    }
    .banner-container-sponsor {
        background-color: #500000;
    }
    :root {
        --maroon: #500000;
        --ink: #211f1f;
        --bg: #f4f0eb;
        --paper: #ffffff;
        --highlight: #f7c948;
        --muted: #6b6762;
        --edge: #d8ccc2;
        --accent: #007f7f;
    }
    * { box-sizing: border-box; }
    body {
        margin: 0;
        font-family: "Segoe UI", "Trebuchet MS", Helvetica, Arial, sans-serif;
        color: var(--ink);
        background:
            radial-gradient(circle at 10% 0%, #fff7d6 0%, transparent 28%),
            radial-gradient(circle at 95% 90%, #e4f6f6 0%, transparent 32%),
            var(--bg);
        min-height: 100vh;
    }
    .page-shell {
        max-width: 1200px;
        margin: 0 auto;
        padding: 24px;
    }
    .page-header {
        background: linear-gradient(120deg, #500000 0%, #6b1010 55%, #8f2b2b 100%);
        color: #fff;
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 10px 28px rgba(80, 0, 0, 0.25);
    }
    .page-header h1 {
        margin: 0;
        font-size: clamp(1.65rem, 1.2rem + 1.6vw, 2.4rem);
        line-height: 1.15;
    }
    .page-header p {
        margin: 10px 0 0;
        color: #ffefef;
        max-width: 74ch;
    }
    .controls-panel {
        margin: 22px 0 16px;
        padding: 18px;
        border: 1px solid var(--edge);
        border-radius: 14px;
        background: linear-gradient(180deg, #fffefc 0%, #fff7ef 100%);
        box-shadow: 0 6px 20px rgba(30, 24, 16, 0.08);
    }
    .controls-panel h2 {
        margin: 0 0 12px;
        font-size: 1.15rem;
        color: var(--maroon);
    }
    .filters-grid {
        display: grid;
        gap: 12px;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        align-items: end;
    }
    .field {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .field label {
        font-weight: 700;
        font-size: 0.92rem;
        color: #3f2f2f;
    }
    .field input,
    .field select {
        padding: 11px 12px;
        border: 1px solid #ccb7a5;
        border-radius: 10px;
        font-size: 0.96rem;
        background: #fff;
    }
    .field input:focus,
    .field select:focus {
        outline: 3px solid rgba(247, 201, 72, 0.38);
        border-color: #9a6e46;
    }
    .results-status {
        margin: 12px 0 0;
        color: black;
        font-size: 0.95rem;
    }
    .major-wrapper {
        margin: 28px 0;
    }
    .major-section {
        border: 0;
        background: transparent;
        padding: 0;
    }
    .major-section > summary {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        color: var(--maroon);
        border-bottom: 2px solid var(--maroon);
        padding: 6px 0;
        font-size: clamp(1.25rem, 1.1rem + 0.8vw, 1.6rem);
        font-weight: 800;
        cursor: pointer;
        list-style-position: outside;
    }
    .major-section > summary:focus-visible {
        outline: 3px solid var(--highlight);
        outline-offset: 4px;
        border-radius: 8px;
    }
    .count-badge {
        font-size: 0.84rem;
        font-weight: 700;
        color: #063a3a;
        background: #dff4f4;
        border: 1px solid #b2dddd;
        border-radius: 999px;
        padding: 4px 10px;
        white-space: nowrap;
    }
    .grid-container {
        margin-top: 14px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 16px;
        align-items: start;
    }
    .project-card {
        border: 1px solid #ded9d3;
        border-radius: 12px;
        padding: 14px;
        background: var(--paper);
        box-shadow: 0 4px 14px rgba(36, 28, 20, 0.08);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(36, 28, 20, 0.14);
        border-color: #b9a999;
    }
    .project-card summary {
        font-weight: 700;
        font-size: 1.02rem;
        cursor: pointer;
        outline: none;
    }
    .project-card summary:focus-visible {
        outline: 3px solid var(--highlight);
        outline-offset: 4px;
        border-radius: 6px;
    }
    .project-card:focus-within {
        border-color: #9a6e46;
        box-shadow: 0 0 0 3px rgba(247, 201, 72, 0.35), 0 10px 20px rgba(36, 28, 20, 0.14);
    }
    .project-card summary:hover { color: var(--accent); }
    .content {
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #efe6dd;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .meta {
        font-size: 0.9rem;
        color: #413c37;
        margin-bottom: 12px;
        background: #f4f8fb;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #dde8ee;
    }
    .is-hidden { display: none !important; }
    .no-results {
        margin: 20px 0;
        padding: 14px 16px;
        border-radius: 12px;
        background: #fff8df;
        border: 1px solid #e7d899;
        color: #4f3f12;
        font-weight: 700;
    }
    @media (max-width: 700px) {
        .page-shell {
            padding: 14px;
        }
        .page-header {
            padding: 20px;
        }
        .controls-panel {
            padding: 14px;
        }
    }
</style>
"""


def clean_text(value, fallback):
        """Return stripped text with a fallback for empty/null values."""
        text = (value or '').strip()
        return text if text else fallback


def build_page(projects_by_major):
        sorted_majors = sorted(projects_by_major.keys())
        html_parts = [
                PAGE_STYLE,
                """
<div aria-label="Page header" role="banner" style="text-align: center">
    <div class="banner-container-sponsor">
        <img alt="Sponsors Banner" class="banner-img" src="https://engineering.tamu.edu/news/2019/04/_news-images/NUEN-news-TRIGA-reactor-23April20191.jpg" />
        <div class="banner-overlay-sponsor">&nbsp;</div>
        <h1 class="banner-heading oswald-heading header-underline-sponsor">2026 EPS Participating Projects</h1>
    </div>
</div>

<div class="section-wrapper" style="background-color: #ffffff; padding: 3rem 1rem">
    <div class="content-box" style="background: white; padding: 2rem; max-width: 1200px; margin: 0 auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
        <div class="page-shell">
            <main id="main-content" role="main">
                <section class="controls-panel" role="search" aria-label="Project search and filters">
                    <h2>Find a Project</h2>
                    <div class="filters-grid">
                        <div class="field">
                            <label for="project-search">Search keyword</label>
                            <input id="project-search" type="search" placeholder="Project title, description, sponsor, or team member" autocomplete="off" />
                        </div>
                        <div class="field">
                            <label for="major-filter">Filter by major</label>
                            <select id="major-filter">
                                <option value="all">All majors</option>
""",
        ]

        for major_index, major in enumerate(sorted_majors):
                major_value = f"major-{major_index}"
                html_parts.append(
                        f'                <option value="{major_value}">{escape(major)}</option>\n'
                )

        html_parts.append(
                """
                            </select>
                        </div>
                        <div class="field">
                            <label for="sort-filter">Sort by name</label>
                            <select id="sort-filter">
                                <option value="asc">A to Z</option>
                                <option value="desc">Z to A</option>
                            </select>
                        </div>
                    </div>
                    <p id="results-status" class="results-status" role="status" aria-live="polite"></p>
                </section>

                <section aria-label="Project listings">
""",
        )

        for major_index, major in enumerate(sorted_majors):
                major_value = f"major-{major_index}"
                major_id = f"major-heading-{major_index}"
                projects = sorted(projects_by_major[major], key=lambda item: item['name'].lower())

                html_parts.append(
                        f"""
                    <section class="major-wrapper" data-major="{major_value}" aria-labelledby="{major_id}">
                        <details class="major-section" open>
                            <summary id="{major_id}">
                                <span>{escape(major)}</span>
                                <span class="count-badge" data-major-count>{len(projects)} projects</span>
                            </summary>
                            <div class="grid-container" role="list">
"""
                )

                for project in projects:
                        name = escape(project['name'])
                        booth_number = escape(project['booth__number'])
                        sponsor = escape(project['sponsor'])
                        description = escape(project['description'])
                        first_name = escape(project['first_name'])
                        last_name = escape(project['last_name'])
                        search_blob = escape(
                                ' '.join(
                                        [
                                                project['name'],
                                                project['booth__number'],
                                                project['description'],
                                                project['sponsor'],
                                                project['first_name'],
                                                project['last_name'],
                                                major,
                                        ]
                                ).lower()
                        )

                        html_parts.append(
                                f"""
                                <details class="project-card" role="listitem" data-search="{search_blob}" data-name="{name}">
                                    <summary>{name}</summary>
                                    <div class="content">
                                        <div class="meta">
                                            <strong>Booth Number:</strong> {booth_number}<br />
                                            <strong>Primary Team Member:</strong> {first_name} {last_name}<br />
                                            <strong>Sponsor:</strong> {sponsor}
                                        </div>
                                        <p>{description}</p>
                                    </div>
                                </details>
"""
                        )

                html_parts.append(
                        """
                            </div>
                        </details>
                    </section>
"""
                )

        html_parts.append(
                """
                </section>
                <p id="no-results" class="no-results is-hidden" role="status" aria-live="polite">No projects match the current search and filters.</p>
            </main>
        </div>
    </div>
</div>

<script>
    (function () {
        const searchInput = document.getElementById('project-search');
        const majorFilter = document.getElementById('major-filter');
        const sortFilter = document.getElementById('sort-filter');
        const majorWrappers = Array.from(document.querySelectorAll('.major-wrapper'));
        const noResults = document.getElementById('no-results');
        const resultsStatus = document.getElementById('results-status');

        function sortCards(grid, direction) {
            const cards = Array.from(grid.querySelectorAll('.project-card'));
            cards.sort(function (left, right) {
                return left.dataset.name.localeCompare(right.dataset.name, undefined, { sensitivity: 'base' });
            });
            if (direction === 'desc') {
                cards.reverse();
            }
            cards.forEach(function (card) {
                grid.appendChild(card);
            });
        }

        function updateResults() {
            const keyword = searchInput.value.trim().toLowerCase();
            const selectedMajor = majorFilter.value;
            let totalVisibleProjects = 0;
            let visibleMajors = 0;

            majorWrappers.forEach(function (wrapper) {
                const majorValue = wrapper.dataset.major;
                const majorDetails = wrapper.querySelector('.major-section');
                const grid = wrapper.querySelector('.grid-container');
                const cards = Array.from(wrapper.querySelectorAll('.project-card'));

                sortCards(grid, sortFilter.value);

                let visibleProjectsInMajor = 0;
                cards.forEach(function (card) {
                    const matchesKeyword = !keyword || card.dataset.search.indexOf(keyword) !== -1;
                    const matchesMajor = selectedMajor === 'all' || selectedMajor === majorValue;
                    const isVisible = matchesKeyword && matchesMajor;

                    card.classList.toggle('is-hidden', !isVisible);
                    if (isVisible) {
                        visibleProjectsInMajor += 1;
                    }
                });

                wrapper.classList.toggle('is-hidden', visibleProjectsInMajor === 0);
                majorDetails.open = visibleProjectsInMajor > 0;

                const countBadge = wrapper.querySelector('[data-major-count]');
                countBadge.textContent = visibleProjectsInMajor + ' project' + (visibleProjectsInMajor === 1 ? '' : 's');

                if (visibleProjectsInMajor > 0) {
                    totalVisibleProjects += visibleProjectsInMajor;
                    visibleMajors += 1;
                }
            });

            const hasResults = totalVisibleProjects > 0;
            noResults.classList.toggle('is-hidden', hasResults);

            if (hasResults) {
                resultsStatus.textContent = 'Showing ' + totalVisibleProjects + ' project' + (totalVisibleProjects === 1 ? '' : 's') + ' across ' + visibleMajors + ' major' + (visibleMajors === 1 ? '' : 's');
            } else {
                resultsStatus.textContent = 'No matching projects found.';
            }
        }

        searchInput.addEventListener('input', updateResults);
        majorFilter.addEventListener('change', updateResults);
        sortFilter.addEventListener('change', updateResults);
        updateResults();
    })();
</script>
"""
        )

        return ''.join(html_parts)


try:
        projects_by_major = defaultdict(list)

        with open(input_file, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)

                for row in reader:
                        category = clean_text(row.get('Selected Category'), 'Uncategorized')
                        project_data = {
                                'name': clean_text(row.get('Application Name'), 'Unnamed Project'),
                                'booth__number': clean_text(
                                        row.get('(Team & Judge Registration - Phase I - Team Registration) Booth Number'),
                                        'N/A',
                                ),
                                'sponsor': clean_text(
                                        row.get('(Team & Judge Registration - Phase I - Team Registration) SPONSOR NAME'),
                                        'N/A',
                                ),
                                'description': clean_text(
                                        row.get('(Team & Judge Registration - Phase I - Team Registration) PROJECT DESCRIPTION'),
                                        'No description available.',
                                ),
                                'first_name': clean_text(row.get('Applicant First Name'), 'N/A'),
                                'last_name': clean_text(row.get('Applicant Last Name'), 'N/A'),
                        }
                        projects_by_major[category].append(project_data)

        html_content = build_page(projects_by_major)

        with open(output_file, mode='w', encoding='utf-8') as file:
                file.write(html_content)

        print(f"Success! Your grouped interactive fragment has been saved as '{output_file}'.")

except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'. Please ensure it is in the same folder as this script.")
except Exception as e:
        print(f"An unexpected error occurred: {e}")