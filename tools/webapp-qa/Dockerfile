FROM node:20-bookworm-slim

ENV PUPPETEER_SKIP_DOWNLOAD=true

RUN apt-get update \
  && apt-get install -y --no-install-recommends chromium ca-certificates fonts-liberation \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/tools/webapp-qa

COPY package.json package-lock.json* ./
RUN npm install

CMD ["sleep", "infinity"]
