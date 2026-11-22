import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer } from "node:http";
import { fileURLToPath } from "node:url";

const viewer = new URL("../../../artifacts/science-shorts/coin-viewer-gate/viewer/", import.meta.url);
const types = {
  "index.html": "text/html; charset=utf-8",
  "source.mp4": "video/mp4",
  "zh-Hant.vtt": "text/vtt; charset=utf-8",
  "assignments.json": "application/json",
  "hook-0.webp": "image/webp",
  "hook-1.webp": "image/webp",
  "hook-2.webp": "image/webp",
};
const host = process.argv[2] ?? "127.0.0.1";
const port = Number(process.argv[3] ?? 8765);

createServer(async (request, response) => {
  const path = new URL(request.url, "http://viewer.local").pathname;
  const name = path === "/" ? "index.html" : path.slice(1);
  if (!Object.hasOwn(types, name)) return response.writeHead(404).end();
  if (!["HEAD", "GET"].includes(request.method)) return response.writeHead(405, {Allow: "GET, HEAD"}).end();

  const file = fileURLToPath(new URL(name, viewer));
  let size;
  try {
    ({ size } = await stat(file));
  } catch (error) {
    return response.writeHead(error.code === "ENOENT" ? 404 : 500).end();
  }
  const headers = { "Content-Type": types[name], "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" };
  let start = 0;
  let end = size - 1;
  let status = 200;
  if (name === "source.mp4") {
    headers["Accept-Ranges"] = "bytes";
    if (request.headers.range) {
      const range = /^bytes=(\d*)-(\d*)$/.exec(request.headers.range);
      if ((range?.[1] || range?.[2]) && (!range[1] || Number(range[1]) < size)) {
        start = range[1] ? Number(range[1]) : Math.max(size - Number(range[2]), 0);
        end = range[1] && range[2] ? Math.min(Number(range[2]), size - 1) : size - 1;
      } else {
        start = size;
      }
      if (start > end) return response.writeHead(416, {"Content-Range": "bytes */" + size}).end();
      headers["Content-Range"] = "bytes " + start + "-" + end + "/" + size;
      status = 206;
    }
  }
  headers["Content-Length"] = end - start + 1;
  response.writeHead(status, headers);
  if (request.method === "HEAD") return response.end();
  const stream = createReadStream(file, {start, end});
  stream.on("error", () => response.destroy());
  response.on("close", () => stream.destroy());
  stream.pipe(response);
}).listen(port, host, () => {
  console.log("短片試看伺服器  http://" + host + ":" + port + "/");
});

