FROM node:22-slim

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY . .

RUN mkdir -p /app/node_modules/.vite-temp \
    && chmod -R 777 /app/node_modules

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]