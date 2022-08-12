FROM node:18-alpine3.15
WORKDIR /app
ARG api_url
ENV PATH /app/node_modules/.bin:$PATH
COPY . ./
RUN npm install --silent
RUN npm install react-scripts -g --silent
ENV REACT_APP_API_URL=$api_url
RUN npm run build
RUN npm install -g serve
CMD ["serve", "-s", "build"]