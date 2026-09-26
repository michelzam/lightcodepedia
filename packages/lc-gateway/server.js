#!/usr/bin/env node
/*!
 * @karmicsoft/lc-gateway — the HTTP adapter. © KarmicSoft — LightCode.
 * Reads the environment, builds the gateway, answers on PORT. Everything
 * that decides lives in index.js; this file only moves bytes.
 */
import { createServer } from 'node:http';
import { createGateway } from './index.js';
import { configFromEnv } from './config.js';

const cfg = configFromEnv();
const gw = createGateway(cfg, { log: (m) => console.log('[lc-gateway] ' + m) });
const origin = cfg.appUrl ? new URL(cfg.appUrl).origin : '';

const server = createServer(async (req, res) => {
  const cors = origin ? { 'access-control-allow-origin': origin, 'access-control-allow-credentials': 'true',
    'access-control-allow-headers': 'content-type', 'access-control-allow-methods': 'GET,POST,OPTIONS', vary: 'Origin' } : {};
  if (req.method === 'OPTIONS') { res.writeHead(204, cors); res.end(); return; }
  let body = '';
  for await (const chunk of req) { body += chunk; if (body.length > 2_000_000) { res.writeHead(413); res.end(); return; } }
  const out = await gw.request({ method: req.method, path: req.url, headers: req.headers, body });
  const headers = { ...cors, ...out.headers };
  res.writeHead(out.status, headers);
  res.end(typeof out.body === 'string' ? out.body : JSON.stringify(out.body));
});

server.listen(cfg.port, () => console.log('[lc-gateway] ' + gw.version + ' on :' + cfg.port + ' for ' + cfg.repo));
