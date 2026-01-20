export default async function handler(req, res) {
  const cid = req.query.cid || "anon";

  const key = `viewer:${cid}`;
  const value = Date.now();
  const url =
    process.env.UPSTASH_REDIS_REST_URL +
    `/set/${key}/${value}?ex=7`;

  const r = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.UPSTASH_REDIS_REST_TOKEN}`
    }
  });

  const text = await r.text();
  console.log("SET:", key, text);

  res.status(200).json({ ok: true });
}
