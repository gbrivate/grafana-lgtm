# =========================================
# Stage 1: Build the Angular Application
# =========================================
ARG NODE_VERSION=20-alpine
ARG NGINX_VERSION=alpine3.22

FROM node:${NODE_VERSION} AS builder

WORKDIR /app


# Copy only dependency manifests (better cache)
COPY package.json pnpm-lock.yaml ./

# Enable pnpm via corepack
RUN corepack enable

# Install dependencies (deterministic & fast)
RUN pnpm install --frozen-lockfile

# Copy application source
COPY . .

# Build Angular app
RUN pnpm run build_prd


# =========================================
# Stage 2: Nginx runtime
# =========================================
FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

USER nginx

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --chown=nginx:nginx \
  --from=builder \
  /app/dist/fastapi-mfe-test/browser \
  /usr/share/nginx/html/fastapi-mfe-test

CMD ["nginx", "-g", "daemon off;"]
