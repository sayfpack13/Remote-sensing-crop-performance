# Installation and Setup Guide

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 1GB free space
- **Internet**: Stable connection for satellite data access

### Required Accounts
- **Sentinel Hub Account**: Free account at [sentinel-hub.com](https://www.sentinel-hub.com/)
  - Sign up for a free account
  - Create a new configuration
  - Note your Instance ID

## Installation Methods

### Method 1: Standard Installation

#### Step 1: Clone the Repository
```bash
# Using HTTPS
git clone https://github.com/YourUsername/remote-sensing-crop-performance.git
cd remote-sensing-crop-performance

# Or using SSH
git clone git@github.com:YourUsername/remote-sensing-crop-performance.git
cd remote-sensing-crop-performance
```

#### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install Flask==2.3.3 numpy==1.24.3 requests==2.31.0 Pillow==10.0.0 opencv-python==4.8.0.76 matplotlib==3.7.2
```

#### Step 4: Configure Sentinel Hub
1. Open `app.py` in a text editor
2. Replace the placeholder Instance ID:
```python
# Replace this with your actual instance ID
SENTINEL_INSTANCE_ID = 'YOUR_SENTINEL_HUB_INSTANCE_ID_HERE'
```

#### Step 5: Run the Application
```bash
# Set Flask environment variables
export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development

# Run the application
flask run
```

### Method 2: Using Docker (Optional)

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p static/outputs

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

#### Step 2: Build and Run
```bash
# Build the Docker image
docker build -t crop-performance-app .

# Run the container
docker run -p 5000:5000 -e SENTINEL_INSTANCE_ID=YOUR_INSTANCE_ID crop-performance-app
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:
```bash
SENTINEL_INSTANCE_ID=your_sentinel_hub_instance_id
FLASK_ENV=development
FLASK_DEBUG=True
MAX_IMAGE_SIZE=1024
DEFAULT_RESOLUTION=5.0
```

### Configuration File

Create `config.py` for advanced configuration:
```python
import os

class Config:
    SENTINEL_INSTANCE_ID = os.environ.get('SENTINEL_INSTANCE_ID') or 'your-default-id'
    MAX_IMAGE_SIZE = int(os.environ.get('MAX_IMAGE_SIZE', 1024))
    DEFAULT_RESOLUTION = float(os.environ.get('DEFAULT_RESOLUTION', 5.0))
    OUTPUT_DIR = os.path.join('static', 'outputs')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
```

## Verification

### Step 1: Check Installation
```bash
# Verify Python version
python --version

# Verify packages
pip list | grep Flask
pip list | grep numpy
pip list | grep opencv-python
```

### Step 2: Test Application
1. Start the application: `flask run`
2. Open browser to `http://127.0.0.1:5000`
3. Verify the map loads correctly
4. Test drawing a rectangle on the map
5. Try analyzing a small area (start with True Color layer)

### Step 3: Test Sentinel Hub Connection
Navigate to a test area and try downloading a satellite image. If you see a 403 error, verify your Sentinel Hub Instance ID.

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'cv2'"
**Solution:**
```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

#### Issue: "Sentinel Hub API returns 403 Forbidden"
**Solutions:**
1. Verify your Sentinel Hub Instance ID is correct
2. Check if your Sentinel Hub account is active
3. Ensure you haven't exceeded your monthly quotas

#### Issue: "Permission denied" when creating output directory
**Solution:**
```bash
# Create directory manually with proper permissions
mkdir -p static/outputs
chmod 755 static/outputs
```

#### Issue: matplotlib/GUI errors on headless servers
**Solution:** Ensure matplotlib is using the 'Agg' backend (already configured in app.py)

#### Issue: Memory errors with large areas
**Solutions:**
1. Reduce the selected area size
2. Increase resolution value (lower quality)
3. Increase system RAM

### Platform-Specific Issues

#### Windows
- Use `venv\Scripts\activate` instead of `source venv/bin/activate`
- Use `set` instead of `export` for environment variables
- Ensure Python is added to PATH

#### macOS
- Install Xcode command line tools: `xcode-select --install`
- Use `python3` and `pip3` if default Python is 2.x

#### Linux
- Install system dependencies:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-dev python3-pip
  ```

## Performance Optimization

### For Development
```python
# In app.py, adjust these settings
MAX_PIXELS = 512  # Reduce for faster processing
DEFAULT_RESOLUTION = 10  # Higher values = lower quality but faster
```

### For Production
```python
# Recommended production settings
MAX_PIXELS = 1024
DEFAULT_RESOLUTION = 2
DEBUG = False
```

## Security Setup

### Environment Security
1. Never commit API keys to version control
2. Use environment variables for sensitive data
3. Set proper file permissions on the project directory

### Network Security
1. Run behind a reverse proxy (nginx) in production
2. Use HTTPS in production
3. Implement rate limiting if needed

## Next Steps

After successful installation:

1. **Read the User Guide**: `docs/USER_GUIDE.md`
2. **Review API Documentation**: `docs/API_DOCUMENTATION.md`
3. **Understand the Architecture**: `docs/TECHNICAL_ARCHITECTURE.md`
4. **Explore Customization**: `docs/CUSTOMIZATION_GUIDE.md`

## Getting Help

If you encounter issues not covered in this guide:

1. Check the GitHub Issues page
2. Review the troubleshooting section
3. Ensure all dependencies are correctly installed
4. Verify your Sentinel Hub account status

## Uninstallation

To remove the application:

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
rm -rf remote-sensing-crop-performance

# Remove virtual environment (if created outside project)
rm -rf venv
```
