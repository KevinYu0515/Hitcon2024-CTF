FROM node:17-alpine
RUN apk update && apk upgrade && apk add chromium 

WORKDIR /app
ENV FLAG "HackerSir{Xssss_RevErse_T1me}"
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 3010
CMD ["npm", "start"]