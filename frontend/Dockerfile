# Use the official lightweight Nginx image to serve static content
FROM nginx:alpine

# Remove the default Nginx index page
RUN rm /usr/share/nginx/html/index.html

# Copy your entire frontend application into the Nginx web root
# Assuming your main file is 'index.html' and it uses inline JS/CSS
COPY frontend/ /usr/share/nginx/html/

# Standard HTTP port 80 will be used inside the container
EXPOSE 80