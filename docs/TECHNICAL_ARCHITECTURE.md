# Technical Architecture Documentation

## Overview

This document provides a detailed technical overview of the Remote Sensing Crop Performance application architecture, components, and implementation details.



## Technology Stack

### Backend
- **Framework**: Flask 2.x
- **Language**: Python 3.x
- **Image Processing**: 
  - PIL (Pillow) - Image manipulation
  - OpenCV (cv2) - Computer vision operations
  - NumPy - Numerical computations
- **Visualization**: Matplotlib - Chart and legend generation
- **HTTP Client**: Requests - API communication

### Frontend
- **Mapping**: Leaflet.js - Interactive maps
- **Drawing Tools**: Leaflet.draw - Area selection
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

### External Services
- **Satellite Data**: Sentinel Hub WMS API
- **Base Maps**: OpenStreetMap tiles

## Component Architecture

### 1. Flask Application (`app.py`)

#### Core Components

##### Configuration Constants
```python
SENTINEL_INSTANCE_ID = 'd7482dab-6310-4b9e-a829-b380b4ae9f7e'
WMS_LAYERS = {...}  # Available satellite layers
CROP_YIELD_DATA = {...}  # Crop yield coefficients
EVALSCRIPT_COLOR_MAP = [...]  # NDVI color mapping
```

##### Utility Functions

**`haversine(lat1, lon1, lat2, lon2)`**
- Calculates distance between geographic coordinates
- Used for area calculations
- Returns distance in meters

**`get_image_dimensions_for_bbox(bbox, resolution_meters, max_pixels)`**
- Calculates optimal image dimensions for a bounding box
- Enforces maximum pixel limits to prevent memory issues
- Maintains aspect ratio

**`download_wms_image(bbox, layer_id, resolution_meters, width_px, height_px)`**
- Downloads satellite imagery from Sentinel Hub WMS API
- Handles different resolution specifications
- Returns numpy array in RGB format

##### Image Processing Functions

**`classify_ndvi(ndvi_array)`**
- Classifies NDVI pixels into vegetation categories
- Uses predefined NDVI thresholds
- Returns pixel counts for each category

**`create_ndvi_overlay(ndvi_array, true_color_img)`**
- Creates colored NDVI overlay on true color image
- Uses weighted blending (70% original, 30% overlay)
- Applies consistent color mapping

**`generate_legend()`**
- Creates NDVI legend with color ramp
- Uses matplotlib LinearSegmentedColormap
- Includes labeled NDVI thresholds

### 2. Frontend Architecture (`templates/index.html`)

#### Map Component
```javascript
// Map initialization
const map = L.map("map").setView([36.8, 10.1], 9);

// WMS layer management
let currentWMSLayer = L.tileLayer.wms(sentinelHubWMSBaseUrl, {
  layers: '1_TRUE_COLOR',
  format: 'image/png',
  transparent: true,
  attribution: "Sentinel Hub"
}).addTo(map);
```

#### Drawing Controls
```javascript
const drawControl = new L.Control.Draw({
  draw: { rectangle: true, polygon: false, polyline: false, circle: false, marker: false },
  edit: { featureGroup: drawnItems, remove: true }
});
```

#### Custom Map Layer Control
- Custom Leaflet control for layer switching
- Positioned in top-right corner
- Updates WMS layer in real-time

## Data Flow

### 1. User Interaction Flow
```
User draws rectangle → Select analysis parameters → Click "Analyze Area"
        ↓
Extract bounding box coordinates → Validate inputs
        ↓
Send POST request to /process_area endpoint
        ↓
Display loading spinner → Process on backend → Show results
```

### 2. Backend Processing Flow
```
Receive request → Validate parameters → Calculate image dimensions
        ↓
Download satellite imagery from Sentinel Hub
        ↓
Process NDVI data (if applicable) → Generate overlay/histogram/legend
        ↓
Calculate area and yield estimates → Return response with URLs
```

### 3. NDVI Processing Pipeline
```
Raw NDVI image (0-255 grayscale) → Scale to [-1, 1] range
        ↓
Apply color mapping based on NDVI thresholds
        ↓
Classify pixels (water/barren/sparse/dense vegetation)
        ↓
Generate overlay, histogram, and legend → Calculate statistics
```

## File Structure

```
remote-sensing-crop-performance/
├── app.py                      # Main Flask application
├── templates/
│   └── index.html             # Frontend interface
├── static/
│   └── outputs/               # Generated analysis outputs
│       ├── true_color.png     # Downloaded satellite image
│       ├── ndvi_overlay.png   # NDVI colored overlay
│       ├── ndvi_histogram.png # NDVI distribution chart
│       └── ndvi_legend.png    # NDVI color legend
├── docs/                      # Documentation files
└── __pycache__/              # Python bytecode cache
```

## Image Processing Details

### NDVI Color Mapping
The application uses a precise color mapping system based on NDVI values:

| NDVI Range | Color | Vegetation Type |
|------------|-------|----------------|
| -1.0 to -0.5 | Black | Water/Very Low |
| -0.5 to 0.0 | Light Gray | Barren |
| 0.0 to 0.1 | Yellow-Green | Sparse |
| 0.1 to 0.4 | Green gradients | Moderate |
| 0.4 to 1.0 | Dark Green | Dense |

### Area Calculations
1. **Haversine Formula**: Calculates real-world distances from coordinates
2. **Pixel Scaling**: Maps pixel counts to real area using resolution
3. **Vegetation Area**: Sums sparse and dense vegetation pixels

### Yield Estimation
```python
vegetated_area_hectares = total_area_hectares * (vegetated_pixels / total_pixels)
estimated_yield = vegetated_area_hectares * crop_yield_per_hectare
```

## Performance Considerations

### Image Size Limits
- Maximum 1024 pixels on any dimension
- Automatic scaling for large areas
- Memory-efficient processing with NumPy

### Caching Strategy
- Generated images saved to disk
- Timestamped URLs prevent browser caching
- No server-side caching implemented

### API Rate Limiting
- Dependent on Sentinel Hub quotas
- No application-level rate limiting
- Single-threaded processing

## Security Considerations

### Input Validation
- Bounding box coordinate validation
- Resolution parameter bounds checking
- Layer ID whitelisting

### External API Security
- Sentinel Hub Instance ID required
- No authentication credentials in frontend
- HTTPS endpoints for external calls

### File System Security
- Outputs restricted to `static/outputs/` directory
- No user-controlled file paths
- Automatic directory creation with proper permissions

## Error Handling

### Backend Error Categories
1. **Validation Errors**: Invalid input parameters
2. **API Errors**: Sentinel Hub service issues
3. **Processing Errors**: Image manipulation failures
4. **File System Errors**: Storage/permission issues

### Frontend Error Handling
- Network request error catching
- User-friendly error messages
- Loading state management
- Graceful degradation

## Scalability Considerations

### Current Limitations
- Single-threaded processing
- In-memory image processing
- Local file storage
- No database persistence

### Potential Improvements
- Async processing with task queues
- Cloud storage integration
- Database for analysis history
- Horizontal scaling with load balancing
- Caching layer (Redis/Memcached)

## Monitoring and Logging

### Current Implementation
- Flask debug mode for development
- Basic exception handling
- Console output for errors

### Recommended Additions
- Structured logging (JSON format)
- Performance metrics collection
- Error tracking (Sentry)
- Health check endpoints
- Request/response logging
