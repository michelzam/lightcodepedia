# @karmicsoft/lc-gateway — one image for an OVH VPS (Docker) and for
# Scaleway Serverless Containers (fr-par). Config is the environment; the
# image holds no secret and no fixture. See DEPLOY.md.
#
# Build from the bricks workspace, so the two bricks the gateway imports
# come from the same checkout, npm or not:
#     cd packages && docker build -f lc-gateway/Dockerfile -t lc-gateway .
FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
# Only what runs: the three bricks' sources and manifests. No tests, no
# fixtures, no docs travel into the image.
COPY lc-serialize/package.json lc-serialize/index.js lc-serialize/
COPY lc-patch/package.json lc-patch/index.js lc-patch/
COPY lc-gateway/package.json lc-gateway/index.js lc-gateway/config.js lc-gateway/server.js lc-gateway/
RUN printf '{"name":"lc-gateway-image","private":true,"type":"module","workspaces":["lc-serialize","lc-patch","lc-gateway"]}' > package.json \
 && npm install --omit=dev --no-audit --no-fund --silent \
 && chown -R node:node /app
EXPOSE 8080
USER node
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:${PORT:-8080}/health || exit 1
CMD ["node", "lc-gateway/server.js"]
