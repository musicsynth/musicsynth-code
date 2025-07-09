# MusicSynth Production Deployment Guide

## Overview
MusicSynth is a production-ready Streamlit application that converts sheet music into visual piano roll animations with secure Supabase authentication.

## Prerequisites

### 1. Supabase Setup
1. Create a Supabase account at [https://supabase.com](https://supabase.com)
2. Create a new project
3. Go to **Settings** → **API**
4. Copy your **Project URL** and **anon/public key**

### 2. Environment Variables
Create a `.env` file in your project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
STREAMLIT_SERVER_ENVIRONMENT=production
```

## Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Build and Run with Docker
```bash
# Build the Docker image
docker build -t musicsynth .

# Run the container
docker run -p 8501:8501 --env-file .env musicsynth
```

#### Using Docker Compose
```bash
# Production deployment
docker-compose up -d

# Development with hot reload
docker-compose --profile dev up -d musicsynth-dev
```

### Option 2: Local Development

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Run the Application
```bash
streamlit run app.py
```

### Option 3: Streamlit Cloud

1. Push your code to GitHub
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Deploy from your GitHub repository
4. Add environment variables in the Streamlit Cloud dashboard

### Option 4: VPS/Server Deployment

#### Using systemd (Linux)
1. Create a service file: `/etc/systemd/system/musicsynth.service`

```ini
[Unit]
Description=MusicSynth Streamlit App
After=network.target

[Service]
Type=simple
User=musicsynth
WorkingDirectory=/home/musicsynth/MusicSynth
Environment=PATH=/home/musicsynth/MusicSynth/venv/bin
EnvironmentFile=/home/musicsynth/MusicSynth/.env
ExecStart=/home/musicsynth/MusicSynth/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Enable and start the service:
```bash
sudo systemctl enable musicsynth
sudo systemctl start musicsynth
```

#### Using Nginx (Reverse Proxy)
Create `/etc/nginx/sites-available/musicsynth`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Security Considerations

### 1. Environment Variables
- Never commit `.env` files to version control
- Use secure methods to store production secrets
- Rotate Supabase keys regularly

### 2. File Permissions
- Ensure proper directory permissions for `temp/` and `xml_files/`
- Use non-root user in production containers

### 3. Network Security
- Use HTTPS in production
- Configure firewall rules
- Implement rate limiting

## Performance Optimization

### 1. Resource Limits
```bash
# Docker resource limits
docker run --memory="2g" --cpus="1.5" -p 8501:8501 musicsynth
```

### 2. Caching
- Configure Streamlit caching for file processing
- Use CDN for static assets

### 3. Monitoring
- Use Docker health checks
- Monitor application logs
- Set up alerts for failures

## Backup and Recovery

### 1. User Data
- Supabase handles user authentication data
- Set up regular database backups

### 2. Application Data
- Backup `xml_files/` directory
- Monitor `temp/` directory size

## Troubleshooting

### Common Issues

1. **Configuration Error**: Check environment variables
2. **Port already in use**: Change port or kill existing process
3. **Permission denied**: Check file permissions
4. **Memory issues**: Increase container memory limits

### Logs and Debugging

```bash
# View Docker logs
docker logs musicsynth

# Monitor application logs
docker-compose logs -f musicsynth
```

## Scaling

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Deploy multiple containers
- Implement session affinity

### Vertical Scaling
- Increase container resources
- Optimize Python code
- Use faster storage

## Maintenance

### Regular Tasks
- Monitor disk usage in `temp/` directory
- Update dependencies regularly
- Check Supabase usage limits
- Review application logs

### Updates
```bash
# Update application
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

## Support

For issues and questions:
1. Check the logs first
2. Review configuration settings
3. Ensure all dependencies are installed
4. Verify Supabase connectivity

## Production Checklist

- [ ] Supabase project configured
- [ ] Environment variables set
- [ ] SSL/TLS certificate installed
- [ ] Firewall configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Documentation updated
- [ ] Testing completed 