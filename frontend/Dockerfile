# Frontend Dockerfile
FROM node:22-alpine

# Set timezone
ENV TZ=Europe/Rome

WORKDIR /app

# Copy and install dependencies
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

# Copy the code
COPY . .

# Expose the port
EXPOSE 3000

# Start Next.js
CMD ["npm", "run", "dev"]
