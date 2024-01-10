/**
  inkfill <https://metaist.github.io/inkfill/>
  @version 0.1.0
  @copyright 2023-2024 Metaist LLC
  @license MIT
*/

// resolve references
[].slice.apply(document.querySelectorAll("a.ref")).forEach((link) => {
  const href = link.getAttribute("href");
  const ref = document.querySelector(href);
  if (!ref) {
    console.error("[inkfill] Could not find reference:", href);
    return;
  }

  const attr = link.getAttribute("data-attr") || "data-cite";
  link.innerText = ref.getAttribute(attr);
  link.classList.remove("not-defined");
});
