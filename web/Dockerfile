FROM nginx:alpine
# Current context: website/ folder
# Copy everything inside website/ to the serving directory
COPY . /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
