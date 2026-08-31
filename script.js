// Dark-mode toggle. The initial theme is applied inline in each page's <head>
// (before paint) to avoid a flash; this only handles clicks afterwards.
document.getElementById('theme-toggle').addEventListener('click', function () {
  var root = document.documentElement;
  var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});
