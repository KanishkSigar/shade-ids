const paths = [
  "app.py",
  "src/__init__.py",
  "src/signature/__init__.py",
  "src/signature/rules.py",
  "demo/sample_flows.csv",
];

const start = document.querySelector("#start");
const dashboard = document.querySelector("#dashboard");

try {
  const [{ mount }, files] = await Promise.all([
    import("https://cdn.jsdelivr.net/npm/@stlite/browser@1.12.3/build/stlite.js"),
    Promise.all(paths.map(async path => {
      const response = await fetch(new URL(path, import.meta.url));
      if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
      return [path, await response.text()];
    })),
  ]);
  const app = mount({
    entrypoint: "app.py",
    files: Object.fromEntries(files),
    requirements: ["pandas"],
    env: { SHADE_BROWSER_BASE: new URL("./", import.meta.url).href },
  }, dashboard);
  await app._kernel.loaded;
  dashboard.hidden = false;
  start.hidden = true;
} catch (error) {
  dashboard.hidden = true;
  console.error(error);
  document.querySelector("#status").textContent =
    "The dashboard could not start. Reload to retry, or use the local setup link below.";
}
