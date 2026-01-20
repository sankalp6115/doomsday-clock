export default async function handler(req, res) {
  const scan = await fetch(
    process.env.UPSTASH_REDIS_REST_URL + "/scan/0?match=viewer:*&count=1000",
    {
      headers: {
        Authorization: `Bearer ${process.env.UPSTASH_REDIS_REST_TOKEN}`
      }
    }
  );
  const data = await scan.json();
  const keys = data.result?.[1] || [];

  res.status(200).json({ viewers: keys.length });
}
