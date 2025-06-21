# Build stage
FROM python:3.10-alpine AS builder

# Install build dependencies
RUN apk update && apk add --no-cache \
    git \
    build-base \
    linux-headers

# Install Python dependencies
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel==0.45.1
RUN pip wheel --no-cache-dir --wheel-dir=/build/wheels -r requirements.txt

# Runtime stage
FROM python:3.10-alpine

# Set timezone
ENV TZ=Asia/Kolkata

# Install runtime dependencies only
RUN apk update && apk add --no-cache tzdata

# Copy wheels from builder stage
WORKDIR /app
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy application code
COPY . .

CMD ["python3", "-m", "Bot"]