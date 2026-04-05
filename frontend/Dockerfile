FROM node:20-alpine AS deps

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

FROM deps AS development

COPY . .

EXPOSE 80

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "80"]

FROM deps AS build

ARG VITE_API_URL=
ARG VITE_SESSION_EVENTS_WS_URL=/api/v1/sessions/events/ws

ENV VITE_API_URL=${VITE_API_URL}
ENV VITE_SESSION_EVENTS_WS_URL=${VITE_SESSION_EVENTS_WS_URL}

COPY . .

RUN npm run build

FROM nginx:1.27-alpine AS runtime

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
