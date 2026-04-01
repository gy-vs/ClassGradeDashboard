FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install --registry=https://registry.npmmirror.com

COPY . .

EXPOSE 8080

CMD ["npm", "run", "dev"]
