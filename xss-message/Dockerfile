FROM oven/bun:latest as base
RUN apt-get update \
    && apt-get install -y chromium \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV FLAG "HackerSir{Xssss_RevErse_T1me}"
COPY package.json bun.lockb ./
RUN bun install
COPY . .
EXPOSE 3010
CMD ["bun", "start"]