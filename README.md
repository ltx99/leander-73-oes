# leander-73-oes
Website for Leander Chapter No. 73, Order of the Eastern Star, served by GitHub Pages.

## Updating styles

The page uses Tailwind CSS, prebuilt into `styles.css` (no CDN script). After changing classes in `index.html` or styles in `src/input.css`, rebuild and commit `styles.css`:

```
npm install
npm run build:css
```

`npm run watch:css` rebuilds automatically while you edit.
