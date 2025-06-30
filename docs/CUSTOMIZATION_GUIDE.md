# Customization Guide

## Overview

This guide explains how to customize and extend the Remote Sensing Crop Performance application to meet specific requirements.

## Table of Contents

1. [Configuration Customization](#configuration-customization)
2. [Adding New Satellite Layers](#adding-new-satellite-layers)
3. [Modifying Crop Types and Yields](#modifying-crop-types-and-yields)
4. [UI Customization](#ui-customization)
5. [NDVI Color Mapping](#ndvi-color-mapping)
6. [Adding New Analysis Types](#adding-new-analysis-types)
7. [Integrating Additional Data Sources](#integrating-additional-data-sources)
8. [Performance Optimization](#performance-optimization)

## Configuration Customization

### Environment-Based Configuration

Create a `config.py` file for environment-specific settings:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Sentinel Hub configuration
    SENTINEL_INSTANCE_ID = os.environ.get('SENTINEL_INSTANCE_ID')
    
    # Image processing settings
    MAX_IMAGE_SIZE = int(os.environ.get('MAX_IMAGE_SIZE', 1024))
    DEFAULT_RESOLUTION = float(os.environ.get('DEFAULT_RESOLUTION', 5.0))
    MIN_RESOLUTION = float(os.environ.get('MIN_RESOLUTION', 0.1))
    MAX_RESOLUTION = float(os.environ.get('MAX_RESOLUTION', 100.0))
    
    # Output settings
    OUTPUT_DIR = os.path.join('static', 'outputs')
    CACHE_DURATION = int(os.environ.get('CACHE_DURATION', 3600))  # seconds
    
    # Map settings
    DEFAULT_LAT = float(os.environ.get('DEFAULT_LAT', 36.8))
    DEFAULT_LON = float(os.environ.get('DEFAULT_LON', 10.1))
    DEFAULT_ZOOM = int(os.environ.get('DEFAULT_ZOOM', 9))

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

Update `app.py` to use the configuration:

```python
from config import config
import os

app.config.from_object(config[os.environ.get('FLASK_ENV', 'default')])
SENTINEL_INSTANCE_ID = app.config['SENTINEL_INSTANCE_ID']
```

## Adding New Satellite Layers

### Step 1: Update WMS_LAYERS Dictionary

In `app.py`, add new layers to the `WMS_LAYERS` dictionary:

```python
WMS_LAYERS = {
    # Existing layers...
    "True Color": "1_TRUE_COLOR",
    "NDVI": "3_NDVI",
    
    # New custom layers
    "Enhanced Vegetation Index": "EVI",
    "Soil Adjusted Vegetation Index": "SAVI",
    "Leaf Area Index": "LAI",
    "Chlorophyll Content": "CHL",
    "Land Surface Temperature": "LST",
}
```

### Step 2: Add Layer-Specific Processing

Create layer-specific processing functions:

```python
def process_evi_layer(evi_array, true_color_img):
    """Process Enhanced Vegetation Index data"""
    # EVI processing logic
    # Similar to NDVI but with different thresholds
    pass

def process_lai_layer(lai_array, true_color_img):
    """Process Leaf Area Index data"""
    # LAI processing logic
    pass
```

### Step 3: Update the Main Processing Function

Modify the `/process_area` endpoint to handle new layers:

```python
@app.route('/process_area', methods=['POST'])
def process_area():
    # ... existing code ...
    
    if layer_name == '3_NDVI':
        # Existing NDVI processing
        pass
    elif layer_name == 'EVI':
        # New EVI processing
        evi_data = process_evi_layer(rgb_img, rgb_img)
        result_data.update(evi_data)
    elif layer_name == 'LAI':
        # New LAI processing
        lai_data = process_lai_layer(rgb_img, rgb_img)
        result_data.update(lai_data)
    
    return jsonify(result_data)
```

## Modifying Crop Types and Yields

### Adding New Crop Types

Update the `CROP_YIELD_DATA` dictionary in `app.py`:

```python
CROP_YIELD_DATA = {
    # Existing crops
    "wheat": {"name": "Wheat", "yield_tons_per_ha": 8.0},
    "corn": {"name": "Corn", "yield_tons_per_ha": 12.0},
    
    # New crops
    "soybeans": {"name": "Soybeans", "yield_tons_per_ha": 3.5},
    "cotton": {"name": "Cotton", "yield_tons_per_ha": 2.8},
    "sugarcane": {"name": "Sugarcane", "yield_tons_per_ha": 75.0},
    "coffee": {"name": "Coffee", "yield_tons_per_ha": 2.2},
    "cocoa": {"name": "Cocoa", "yield_tons_per_ha": 1.8},
}
```

### Regional Yield Variations

Implement region-specific yield data:

```python
REGIONAL_YIELD_DATA = {
    "north_america": {
        "wheat": 7.5,
        "corn": 11.0,
        "soybeans": 3.2,
    },
    "europe": {
        "wheat": 8.5,
        "corn": 9.5,
        "barley": 6.8,
    },
    "africa": {
        "wheat": 6.0,
        "corn": 8.0,
        "millet": 4.5,
    }
}

def get_regional_yield(crop, region="global"):
    """Get yield data based on region"""
    if region in REGIONAL_YIELD_DATA and crop in REGIONAL_YIELD_DATA[region]:
        return REGIONAL_YIELD_DATA[region][crop]
    return CROP_YIELD_DATA.get(crop, {}).get("yield_tons_per_ha", 5.0)
```

### Update Frontend Crop Selection

In `templates/index.html`, update the crop dropdown:

```html
<select id="crop-select">
  <option value="wheat">Wheat</option>
  <option value="corn">Corn</option>
  <option value="soybeans">Soybeans</option>
  <option value="cotton">Cotton</option>
  <option value="sugarcane">Sugarcane</option>
  <option value="coffee">Coffee</option>
  <option value="cocoa">Cocoa</option>
</select>
```

## UI Customization

### Color Scheme Customization

Update CSS variables in `templates/index.html`:

```css
:root {
  /* Custom color scheme */
  --primary-color: #2E7D32;    /* Dark green */
  --secondary-color: #1565C0;  /* Blue */
  --accent-color: #FF6F00;     /* Orange */
  --background-light: #F1F8E9;
  --background-dark: #E8F5E8;
  --text-color-dark: #1B5E20;
  --text-color-light: #FFFFFF;
  --border-color: #C8E6C9;
  --shadow-light: 0 4px 12px rgba(46, 125, 50, 0.15);
}
```

### Custom Logo and Branding

Replace the header section:

```html
<header>
  <div class="header-content">
    <img src="static/images/logo.png" alt="Company Logo" class="logo">
    <h1>Your Company - Crop Performance Analysis</h1>
    <p class="tagline">Precision Agriculture Through Satellite Technology</p>
  </div>
</header>
```

Add corresponding CSS:

```css
.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.logo {
  height: 50px;
  width: auto;
}

.tagline {
  font-size: 0.9rem;
  opacity: 0.9;
  margin: 0;
}
```

### Custom Map Styling

Add custom map controls:

```javascript
// Custom map attribution
map.attributionControl.addAttribution('Powered by Your Company');

// Custom map markers
const customIcon = L.icon({
    iconUrl: 'static/images/custom-marker.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
});

// Custom map styling
const mapStyle = {
    color: '#2E7D32',
    weight: 3,
    opacity: 0.8,
    fillColor: '#66BB6A',
    fillOpacity: 0.2
};
```

## NDVI Color Mapping

### Custom NDVI Color Scheme

Modify the `EVALSCRIPT_COLOR_MAP` in `app.py`:

```python
# Custom color scheme - Blue to Green gradient
CUSTOM_NDVI_COLOR_MAP = [
    (-1.0, -0.5, [0.1, 0.1, 0.8], 'water_deep_blue'),      # Deep blue for water
    (-0.5, 0.0, [0.8, 0.8, 0.9], 'barren_light_blue'),     # Light blue for barren
    (0.0, 0.2, [0.9, 0.9, 0.7], 'sparse_yellow'),          # Yellow for sparse
    (0.2, 0.4, [0.7, 0.9, 0.3], 'moderate_light_green'),   # Light green
    (0.4, 0.6, [0.3, 0.7, 0.1], 'dense_green'),            # Green
    (0.6, 0.8, [0.1, 0.5, 0.05], 'very_dense_dark_green'), # Dark green
    (0.8, 1.0, [0.0, 0.3, 0.0], 'highest_dense_green')     # Darkest green
]
```

### Temperature-Based Color Mapping

Create alternative color schemes:

```python
# Heat map style (red to green)
HEATMAP_COLOR_MAP = [
    (-1.0, 0.0, [0.8, 0.0, 0.0], 'red_low'),      # Red for low values
    (0.0, 0.3, [0.9, 0.5, 0.0], 'orange_low'),    # Orange
    (0.3, 0.6, [0.9, 0.9, 0.0], 'yellow_medium'), # Yellow
    (0.6, 0.8, [0.5, 0.9, 0.0], 'light_green'),   # Light green
    (0.8, 1.0, [0.0, 0.7, 0.0], 'dark_green')     # Dark green
]

def apply_color_scheme(color_scheme_name="default"):
    """Switch between different color schemes"""
    schemes = {
        "default": EVALSCRIPT_COLOR_MAP,
        "custom": CUSTOM_NDVI_COLOR_MAP,
        "heatmap": HEATMAP_COLOR_MAP
    }
    return schemes.get(color_scheme_name, EVALSCRIPT_COLOR_MAP)
```

## Adding New Analysis Types

### Moisture Stress Analysis

Add a new analysis type for moisture stress:

```python
def analyze_moisture_stress(moisture_img, true_color_img):
    """Analyze crop moisture stress"""
    # Convert moisture index to stress levels
    stress_levels = classify_moisture_stress(moisture_img)
    
    # Create stress overlay
    stress_overlay = create_stress_overlay(moisture_img, true_color_img)
    
    # Generate stress histogram
    stress_histogram = generate_stress_histogram(moisture_img)
    
    return {
        'stress_levels': stress_levels,
        'stress_overlay_url': save_image(stress_overlay, 'stress_overlay.png'),
        'stress_histogram_url': save_image(stress_histogram, 'stress_histogram.png')
    }

def classify_moisture_stress(moisture_array):
    """Classify pixels by moisture stress level"""
    classification = {
        'well_watered': 0,
        'mild_stress': 0,
        'moderate_stress': 0,
        'severe_stress': 0
    }
    
    # Implementation based on moisture index thresholds
    # ...
    
    return classification
```

### Disease Detection Analysis

Implement disease detection using spectral indices:

```python
def detect_crop_diseases(spectral_data):
    """Detect potential crop diseases using spectral analysis"""
    # Calculate disease-related indices
    pri = calculate_photochemical_reflectance_index(spectral_data)
    ari = calculate_anthocyanin_reflectance_index(spectral_data)
    
    # Classify disease risk
    disease_risk = classify_disease_risk(pri, ari)
    
    return {
        'disease_risk_map': disease_risk,
        'high_risk_areas': identify_high_risk_areas(disease_risk),
        'recommendation': generate_disease_recommendations(disease_risk)
    }
```

## Integrating Additional Data Sources

### Weather Data Integration

Add weather data from external APIs:

```python
import requests
from datetime import datetime, timedelta

def fetch_weather_data(lat, lon, date_range=7):
    """Fetch weather data for the analysis area"""
    # Example using OpenWeatherMap API
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    
    weather_data = {
        'temperature': [],
        'humidity': [],
        'precipitation': [],
        'dates': []
    }
    
    # Fetch historical weather data
    for i in range(date_range):
        date = datetime.now() - timedelta(days=i)
        # API call implementation
        # ...
    
    return weather_data

def correlate_weather_crop_health(weather_data, ndvi_data):
    """Correlate weather conditions with crop health"""
    # Analysis implementation
    correlation_results = {
        'temperature_correlation': calculate_correlation(weather_data['temperature'], ndvi_data),
        'precipitation_correlation': calculate_correlation(weather_data['precipitation'], ndvi_data),
        'recommendations': generate_weather_recommendations(weather_data, ndvi_data)
    }
    
    return correlation_results
```

### Soil Data Integration

Integrate soil database information:

```python
def fetch_soil_data(bbox):
    """Fetch soil information for the analysis area"""
    # Integration with soil databases (e.g., SoilGrids API)
    soil_data = {
        'ph_level': get_soil_ph(bbox),
        'organic_carbon': get_soil_carbon(bbox),
        'clay_content': get_clay_content(bbox),
        'sand_content': get_sand_content(bbox)
    }
    
    return soil_data

def adjust_yield_for_soil(base_yield, soil_data, crop_type):
    """Adjust yield estimates based on soil conditions"""
    adjustment_factors = {
        'ph_optimal': calculate_ph_adjustment(soil_data['ph_level'], crop_type),
        'carbon_factor': calculate_carbon_adjustment(soil_data['organic_carbon']),
        'texture_factor': calculate_texture_adjustment(soil_data, crop_type)
    }
    
    adjusted_yield = base_yield * adjustment_factors['ph_optimal'] * \
                    adjustment_factors['carbon_factor'] * \
                    adjustment_factors['texture_factor']
    
    return adjusted_yield, adjustment_factors
```

## Performance Optimization

### Caching Implementation

Add Redis caching for expensive operations:

```python
import redis
import pickle
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_key(bbox, layer, resolution):
    """Generate cache key for analysis results"""
    data = f"{bbox}_{layer}_{resolution}"
    return hashlib.md5(data.encode()).hexdigest()

def cached_analysis(bbox, layer, resolution):
    """Check cache before performing analysis"""
    key = cache_key(bbox, layer, resolution)
    
    # Try to get from cache
    cached_result = redis_client.get(key)
    if cached_result:
        return pickle.loads(cached_result)
    
    # Perform analysis if not cached
    result = perform_analysis(bbox, layer, resolution)
    
    # Cache the result (expire after 1 hour)
    redis_client.setex(key, 3600, pickle.dumps(result))
    
    return result
```

### Asynchronous Processing

Implement background processing for large areas:

```python
from celery import Celery
from flask import current_app

celery = Celery('crop_analysis')

@celery.task
def async_analysis(bbox, layer, resolution, crop_type):
    """Perform analysis asynchronously"""
    try:
        result = perform_detailed_analysis(bbox, layer, resolution, crop_type)
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@app.route('/async_process_area', methods=['POST'])
def async_process_area():
    """Start asynchronous analysis"""
    data = request.get_json()
    
    # Validate input
    if not validate_input(data):
        return jsonify({'success': False, 'error': 'Invalid input'})
    
    # Start background task
    task = async_analysis.delay(
        data['bbox'], 
        data['layer'], 
        data['resolution'], 
        data['crop']
    )
    
    return jsonify({
        'success': True, 
        'task_id': task.id,
        'status': 'processing'
    })

@app.route('/task_status/<task_id>')
def task_status(task_id):
    """Check task status"""
    task = async_analysis.AsyncResult(task_id)
    
    if task.ready():
        result = task.get()
        return jsonify({
            'status': 'completed',
            'result': result
        })
    else:
        return jsonify({
            'status': 'processing',
            'progress': task.info.get('progress', 0) if task.info else 0
        })
```

### Database Integration

Add PostgreSQL with PostGIS for spatial data:

```python
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'
    
    id = Column(Integer, primary_key=True)
    bbox = Column(Geometry('POLYGON'))
    layer_type = Column(String(50))
    resolution = Column(Float)
    crop_type = Column(String(30))
    total_area = Column(Float)
    vegetated_area = Column(Float)
    estimated_yield = Column(Float)
    analysis_date = Column(DateTime)
    ndvi_avg = Column(Float)
    ndvi_std = Column(Float)

def save_analysis_result(bbox, analysis_data):
    """Save analysis results to database"""
    result = AnalysisResult(
        bbox=f"POLYGON(({bbox[1]} {bbox[0]}, {bbox[3]} {bbox[0]}, {bbox[3]} {bbox[2]}, {bbox[1]} {bbox[2]}, {bbox[1]} {bbox[0]}))",
        layer_type=analysis_data['layer_used'],
        resolution=analysis_data['resolution'],
        crop_type=analysis_data['crop'],
        total_area=analysis_data['total_area_hectares'],
        vegetated_area=analysis_data['vegetated_area_hectares'],
        estimated_yield=analysis_data['estimated_yield_tons'],
        analysis_date=datetime.now(),
        ndvi_avg=analysis_data.get('ndvi_average'),
        ndvi_std=analysis_data.get('ndvi_std')
    )
    
    # Save to database
    session.add(result)
    session.commit()
    
    return result.id
```

## Testing Customizations

### Unit Tests for Custom Functions

Create `tests/test_customizations.py`:

```python
import unittest
import numpy as np
from app import classify_moisture_stress, adjust_yield_for_soil

class TestCustomizations(unittest.TestCase):
    
    def test_moisture_stress_classification(self):
        """Test moisture stress classification"""
        # Create test moisture data
        test_data = np.random.rand(100, 100)
        
        # Run classification
        result = classify_moisture_stress(test_data)
        
        # Verify result structure
        self.assertIn('well_watered', result)
        self.assertIn('severe_stress', result)
        self.assertIsInstance(result['well_watered'], int)
    
    def test_soil_yield_adjustment(self):
        """Test soil-based yield adjustment"""
        base_yield = 100.0
        soil_data = {
            'ph_level': 6.5,
            'organic_carbon': 2.0,
            'clay_content': 25.0,
            'sand_content': 45.0
        }
        
        adjusted_yield, factors = adjust_yield_for_soil(base_yield, soil_data, 'wheat')
        
        # Verify adjustment
        self.assertIsInstance(adjusted_yield, float)
        self.assertIsInstance(factors, dict)
        self.assertGreater(adjusted_yield, 0)

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

Create `tests/test_integration.py`:

```python
import unittest
import json
from app import app

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_custom_crop_analysis(self):
        """Test analysis with custom crop types"""
        test_data = {
            'bbox': [36.7, 10.0, 36.9, 10.2],
            'resolution': 10.0,
            'layer': '3_NDVI',
            'crop': 'soybeans'  # Custom crop type
        }
        
        response = self.app.post('/process_area',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertTrue(result['success'])
        self.assertEqual(result['crop'], 'Soybeans')

if __name__ == '__main__':
    unittest.main()
```

## Deployment Considerations

### Environment Configuration

Create environment-specific configuration files:

```bash
# .env.development
FLASK_ENV=development
SENTINEL_INSTANCE_ID=your_dev_instance_id
MAX_IMAGE_SIZE=512
REDIS_URL=redis://localhost:6379

# .env.production
FLASK_ENV=production
SENTINEL_INSTANCE_ID=your_prod_instance_id
MAX_IMAGE_SIZE=1024
REDIS_URL=redis://prod-redis:6379
DATABASE_URL=postgresql://user:pass@prod-db:5432/crop_analysis
```

### Docker Configuration for Custom Features

Update `Dockerfile` for additional dependencies:

```dockerfile
FROM python:3.9-slim

# Install system dependencies for custom features
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy custom configuration
COPY config.py .
COPY .env.production .env

# Copy application code
COPY . .

# Create directories for outputs and logs
RUN mkdir -p static/outputs logs

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

This customization guide provides a comprehensive foundation for extending the application with custom features, new data sources, and enhanced functionality while maintaining code quality and performance.
