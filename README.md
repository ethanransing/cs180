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

Site URL: **https://ethanransing-cs180.github.io/**

That is a *user/org* Pages domain, so it requires a GitHub account or
organization literally named `ethanransing-cs180`, holding a repo named
`ethanransing-cs180.github.io`. A free organization is the easy way:

1. Create the org at https://github.com/organizations/plan (name:
   `ethanransing-cs180`).
2. Create the repo and push:

   ```
   gh repo create ethanransing-cs180/ethanransing-cs180.github.io \
       --public --source=. --push
   ```

3. Settings -> Pages -> Source: **Deploy from a branch**, branch `main`,
   folder `/ (root)`.

The site is plain static files, so there is no build step.
