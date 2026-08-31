# CS 180 — Project Site

Static site (plain HTML/CSS/JS) for CS 180 project write-ups.

```
index.html      landing page: name + list of projects
styles.css      shared styles (copied from ethanransing.github.io, plus
                additions for the project list and project pages)
script.js       dark-mode toggle
images/         shared images
proj0/ …        one folder per project, each with an index.html
```

## Adding a project

1. `cp -r proj1 proj5` and edit `proj5/index.html` (title, heading, sections).
2. Add an `<li>` to the project list in `index.html`.

## Publishing

Site URL: **https://ethanransing.github.io/cs180/**

A project site under the personal account: a repo named `cs180` owned by
`ethanransing`. The site is plain static files, so there is no build step.

```
gh repo create ethanransing/cs180 --public --source=. --push
```

Then Settings -> Pages -> Source: **Deploy from a branch**, branch `main`,
folder `/ (root)`.

All links in the site are relative (`proj0/`, `../styles.css`), so it works
under the `/cs180/` subpath without any base-URL configuration.
