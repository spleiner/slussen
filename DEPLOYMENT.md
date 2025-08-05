# Deployment Guide

This guide covers different ways to deploy the SLussen application for production use.

## Table of Contents

- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Other Hosting Options](#other-hosting-options)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Streamlit Cloud Deployment

The easiest way to deploy SLussen is using Streamlit Cloud (free tier available).

### Prerequisites

- GitHub account
- Repository forked from [spleiner/slussen](https://github.com/spleiner/slussen)

### Step-by-Step Deployment

1. **Fork the Repository**
   ```bash
   # Go to https://github.com/spleiner/slussen
   # Click "Fork" to create your own copy
   ```

2. **Access Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy the App**
   - Click "New app"
   - Select your forked repository
   - Set the main file path: `slussen.py`
   - Choose a custom URL (optional)
   - Click "Deploy"

4. **Monitor Deployment**
   - Deployment typically takes 2-3 minutes
   - View logs for any errors
   - Access your app at the provided URL

### Streamlit Cloud Features

- **Automatic Updates**: Redeploys on git push
- **Free Tier**: Includes reasonable usage limits
- **Custom Domains**: Available on paid plans
- **Resource Management**: Automatic scaling

### Streamlit Cloud Limitations

- **Resource Limits**: CPU and memory restrictions on free tier
- **Sleep Mode**: Apps sleep after inactivity (free tier)
- **Concurrent Users**: Limited on free tier

## Local Deployment

For development or private use, deploy locally.

### Development Server

```bash
# Clone the repository
git clone https://github.com/spleiner/slussen.git
cd slussen

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run slussen.py
```

**Access**: `http://localhost:8501`

### Production-like Local Setup

For more robust local deployment:

```bash
# Install with production dependencies
pip install -r requirements.txt gunicorn

# Run with specific configuration
streamlit run slussen.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.maxUploadSize 1
```

### Environment Variables

```bash
# Optional: Set custom configuration
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

streamlit run slussen.py
```

## Docker Deployment

Deploy using Docker for containerized environments.

### Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY slussen.py .
COPY README.md .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "slussen.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

### Build and Run

```bash
# Build the Docker image
docker build -t slussen:latest .

# Run the container
docker run -p 8501:8501 slussen:latest

# Run with custom configuration
docker run -p 8501:8501 \
  -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
  slussen:latest
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  slussen:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
      - STREAMLIT_SERVER_ENABLE_CORS=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Run with:
```bash
docker-compose up -d
```

## Other Hosting Options

### Heroku

1. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

2. **Add Buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Create Procfile**
   ```
   web: streamlit run slussen.py --server.port=$PORT --server.address=0.0.0.0
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Google Cloud Run

1. **Build and Push Image**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/slussen
   ```

2. **Deploy**
   ```bash
   gcloud run deploy slussen \
     --image gcr.io/PROJECT_ID/slussen \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu or Amazon Linux
   - Configure security groups (port 8501)

2. **Setup Application**
   ```bash
   # Connect to instance
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Install dependencies
   sudo apt update
   sudo apt install python3 python3-pip git
   
   # Clone and setup
   git clone https://github.com/spleiner/slussen.git
   cd slussen
   pip3 install -r requirements.txt
   
   # Run application
   streamlit run slussen.py --server.address 0.0.0.0
   ```

3. **Setup Service (Optional)**
   Create systemd service for automatic startup:
   ```ini
   # /etc/systemd/system/slussen.service
   [Unit]
   Description=SLussen Streamlit App
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/slussen
   ExecStart=/usr/local/bin/streamlit run slussen.py --server.address 0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

## Configuration

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
maxUploadSize = 1
enableCORS = false

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#0068c9"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[logger]
level = "info"
```

### Environment Variables

Commonly used environment variables:

```bash
# Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Application configuration (if added in future)
SL_API_TIMEOUT=10
CACHE_TTL=60
MAX_RETRIES=3
```

### Reverse Proxy Setup

For production deployment behind nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Monitoring

### Health Checks

Basic health check endpoint:
```
GET /_stcore/health
```

Returns 200 OK when application is running.

### Application Monitoring

Monitor these metrics:

- **Response Time**: API call duration
- **Error Rate**: Failed API requests
- **Cache Hit Rate**: Streamlit cache effectiveness
- **User Sessions**: Active users
- **Memory Usage**: Application memory consumption

### Log Analysis

Key log patterns to monitor:

```bash
# API errors
grep "Error fetching" /var/log/slussen.log

# Performance issues
grep "timeout" /var/log/slussen.log

# User activity
grep "GET /" /var/log/nginx/access.log
```

### Alerts

Setup alerts for:
- Application down (health check fails)
- High error rate (>5% API failures)
- High response time (>30 seconds)
- Memory usage (>80% of allocated)

## Troubleshooting

### Common Deployment Issues

**Issue**: Port already in use
```bash
# Solution: Find and kill process or use different port
lsof -ti:8501 | xargs kill -9
# or
streamlit run slussen.py --server.port 8502
```

**Issue**: Permission denied
```bash
# Solution: Check file permissions
chmod +x slussen.py
# or run with appropriate user
sudo -u www-data streamlit run slussen.py
```

**Issue**: Missing dependencies
```bash
# Solution: Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

### Performance Issues

**Issue**: Slow startup
- **Cause**: Large dependency installation
- **Solution**: Use Docker layers, cache dependencies

**Issue**: High memory usage
- **Cause**: Streamlit cache accumulation
- **Solution**: Reduce cache TTL, restart application periodically

**Issue**: API timeouts
- **Cause**: Network latency, SL API issues
- **Solution**: Increase timeout, implement better retry logic

### Network Issues

**Issue**: Cannot reach SL APIs
- **Check**: Firewall rules, DNS resolution
- **Solution**: Whitelist SL domains, check network configuration

**Issue**: CORS errors (development)
- **Solution**: Add `--server.enableCORS=false` flag

### SSL/HTTPS Issues

For production deployments with HTTPS:

```bash
# Generate SSL certificate (Let's Encrypt)
sudo certbot --nginx -d your-domain.com

# Configure nginx for HTTPS
# Update proxy configuration to use SSL
```

## Scaling Considerations

### Horizontal Scaling

- **Load Balancer**: Distribute traffic across multiple instances
- **Session Affinity**: Not required (stateless application)
- **Shared Cache**: Consider Redis for shared caching

### Vertical Scaling

- **Memory**: 512MB minimum, 1GB recommended
- **CPU**: 1 vCPU sufficient for moderate traffic
- **Network**: Ensure good connectivity to SL APIs

### Cost Optimization

- **Streamlit Cloud**: Free tier for personal use
- **Cloud Providers**: Use spot instances, auto-scaling
- **Resource Monitoring**: Right-size based on actual usage

## Security Best Practices

### Application Security

- Keep dependencies updated
- Use HTTPS in production
- Implement rate limiting if needed
- Monitor for unusual traffic patterns

### Infrastructure Security

- Regular security updates
- Firewall configuration
- Access logging
- Backup strategies (minimal for this stateless app)

### API Security

- No API keys required for SL APIs
- Respect rate limits through caching
- Monitor for API changes or deprecations

For additional help with deployment, consult the [Contributing Guidelines](CONTRIBUTING.md) or create an issue on GitHub.