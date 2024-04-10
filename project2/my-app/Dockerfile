# Stage 1: Build the application
FROM node:18-alpine AS builder

# Set the working directory in the Docker container
WORKDIR /app

# Copy the package.json and package-lock.json files into the working directory
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of your application code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Setup the production environment
FROM node:18-alpine AS runner

WORKDIR /app

# Copy over the built artifacts from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]