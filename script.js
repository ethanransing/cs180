// Dark-mode toggle. The initial theme is applied inline in each page's <head>
// (before paint) to avoid a flash; this only handles clicks afterwards.
document.getElementById('theme-toggle').addEventListener('click', function () {
  var root = document.documentElement;
  var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

/* ===== "Latest project" marker (landing page only) =====
   Walks the project list in order, fetches each project page, and marks the
   last one that isn't still an empty template. A page counts as having content
   when any of its <section>s holds more than just its <h2> heading — so the
   marker moves on its own as pages get filled in, with nothing to update here. */
(function () {
  var list = document.querySelector('.project-list');
  if (!list || !window.fetch) return;

  var links = Array.prototype.slice.call(list.querySelectorAll('.project-title a'));

  function hasContent(href) {
    return fetch(href)
      .then(function (r) { return r.ok ? r.text() : ''; })
      .then(function (html) {
        if (!html) return false;
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var sections = doc.querySelectorAll('main section');
        return Array.prototype.some.call(sections, function (s) {
          return s.children.length > 1;
        });
      })
      .catch(function () { return false; });
  }

  Promise.all(links.map(function (a) { return hasContent(a.getAttribute('href')); }))
    .then(function (filled) {
      // Gray out the ones still empty, so the finished work reads first.
      filled.forEach(function (isFilled, i) {
        if (!isFilled) links[i].closest('li').classList.add('is-template');
      });

      var latest = filled.lastIndexOf(true);
      if (latest < 0) return;
      var marker = document.createElement('span');
      marker.className = 'latest-marker';
      marker.textContent = '\u2192';
      marker.title = 'Most recent project';
      marker.setAttribute('aria-hidden', 'true');
      links[latest].parentNode.insertBefore(marker, links[latest]);
    });
})();
