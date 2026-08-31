# CS 180 — Project Site

Static site (plain HTML/CSS/JS) for CS 180 project write-ups.

```
index.html      landing page: name + list of projects
styles.css      shared styles (copied from ethanransing.github.io, plus
                additions for the project list and project pages)
script.js       dark-mode toggle
images/         shared images
proj1/ …        one folder per project, each with an index.html
```

## Adding a project

1. `cp -r proj1 proj6` and edit `proj6/index.html` (title, heading, sections).
2. Add an `<li>` to the project list in `index.html`.

## Publishing

The site is plain static files, so no build step is needed.

```
git remote add origin https://github.com/ethanransing/<repo>.git
git push -u origin main
```

Then in the repo on GitHub: **Settings → Pages → Source: Deploy from a branch**,
branch `main`, folder `/ (root)`. The site appears at
`https://ethanransing.github.io/<repo>/`.
