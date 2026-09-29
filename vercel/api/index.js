// Serves the dashboard page from the public GitHub repo, so pushes to main update the site
// without a redeploy. The page itself fetches data/snapshot.json from the market-data branch.
const SRC = "https://raw.githubusercontent.com/vamsikrishna2421/Investment_Challenge/main/site/index.html";

module.exports = async function handler(req, res) {
  try {
    const r = await fetch(SRC, { headers: { "User-Agent": "h1b-1k-challenge-site" } });
    if (!r.ok) throw new Error("upstream " + r.status);
    const html = await r.text();
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    res.setHeader("Cache-Control", "public, s-maxage=120, stale-while-revalidate=600");
    res.status(200).send(html);
  } catch (e) {
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.setHeader("Cache-Control", "no-store");
    res.status(502).send("The dashboard source is temporarily unavailable. Try again in a minute.");
  }
};
