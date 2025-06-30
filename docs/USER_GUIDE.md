# User Guide

## Getting Started

Welcome to the Remote Sensing Crop Performance application! This guide will walk you through using the application to analyze crop health and estimate yields using satellite imagery.

## Interface Overview

### Header Section
- **Title**: "Remote Sensing Crop Performance"
- Contains the main application branding

### Control Panel
Located below the header, contains the following controls:

#### 1. Analysis Layer
- **Purpose**: Select which satellite data layer to analyze
- **Options**:
  - **True Color**: Natural color RGB composite (good for visual inspection)
  - **False Color**: False color infrared (highlights vegetation)
  - **False Color Urban**: Optimized for urban areas
  - **NDVI**: Vegetation health index (recommended for crop analysis)
  - **Moisture Index**: Soil and vegetation moisture levels
  - **NDSI (Snow)**: Snow cover detection
  - **NDWI (Water)**: Water body detection
  - **SWIR**: Short Wave Infrared

#### 2. Resolution
- **Purpose**: Set the image resolution for analysis
- **Range**: 0.1 to 100 meters per pixel
- **Default**: 5 meters per pixel
- **Note**: Lower values = higher resolution but longer processing time

#### 3. Crop Type
- **Purpose**: Select crop type for yield estimation
- **Options**: Wheat, Corn, Barley, Rice, Oats, Rye
- **Impact**: Affects the yield calculation (tons per hectare)

#### 4. Action Buttons
- **Analyze Area**: Process the selected area
- **Reset Map**: Clear selections and return to default view

### Map Section

#### Map Controls (Top-Left)
- **Zoom In/Out**: `+` and `-` buttons
- **Rectangle Tool**: Draw analysis areas
- **Edit Tool**: Modify drawn rectangles
- **Delete Tool**: Remove drawn rectangles

#### Map Layer Selector (Top-Right)
- **Purpose**: Change the background satellite layer for visual preview
- **Note**: This is separate from the Analysis Layer setting

### Results Section
Appears below the map after analysis, showing:
- Satellite images
- Analysis overlays
- Statistical information
- Yield estimates

## Step-by-Step Usage

### Step 1: Navigate the Map

1. **Initial View**: The map opens centered on Manouba, Tunisia
2. **Navigation**:
   - **Zoom**: Use mouse wheel or `+`/`-` buttons
   - **Pan**: Click and drag to move around
   - **Layer Preview**: Use the dropdown in the top-right to preview different satellite layers

### Step 2: Select Analysis Parameters

1. **Choose Analysis Layer**:
   - For vegetation analysis: Select "NDVI"
   - For visual inspection: Select "True Color"
   - For moisture analysis: Select "Moisture Index"

2. **Set Resolution**:
   - **High detail (slow)**: 1-2 meters per pixel
   - **Balanced (recommended)**: 5-10 meters per pixel
   - **Fast processing**: 15-20 meters per pixel

3. **Select Crop Type**:
   - Choose the crop that best matches your analysis area
   - This affects the final yield calculation

### Step 3: Define Area of Interest

1. **Activate Drawing Tool**:
   - Click the rectangle icon (📦) in the top-left corner
   - Your cursor will change to a crosshair

2. **Draw Rectangle**:
   - Click and drag on the map to create a rectangle
   - The rectangle represents your analysis area

3. **Edit if Needed**:
   - Use the edit tool (✏️) to modify the rectangle
   - Use the delete tool (🗑️) to remove and redraw

**Tips for Area Selection**:
- Start with smaller areas (1-10 km²) for faster processing
- Ensure the area contains the crop fields you want to analyze
- Avoid areas with significant cloud cover

### Step 4: Run Analysis

1. **Click "Analyze Area"**:
   - A loading spinner will appear
   - Processing time depends on area size and resolution

2. **Wait for Results**:
   - Small areas (< 1 km²): 10-30 seconds
   - Medium areas (1-5 km²): 30-60 seconds
   - Large areas (5-20 km²): 1-3 minutes

### Step 5: Interpret Results

#### For All Layers
You'll see:
- **Satellite Image**: The downloaded imagery for your selected area

#### For NDVI Analysis
Additional outputs include:

##### 1. Dense Vegetation Overlay
- **Purpose**: Shows vegetation health visually
- **Colors**:
  - **Dark Green**: Healthy, dense vegetation
  - **Light Green**: Moderate vegetation
  - **Yellow/Brown**: Sparse vegetation
  - **Gray**: Barren land
  - **Black**: Water bodies

##### 2. NDVI Histogram
- **X-axis**: NDVI values (-1 to +1)
- **Y-axis**: Number of pixels
- **Interpretation**:
  - **Left side (negative)**: Water and barren areas
  - **Center (0 to 0.3)**: Sparse to moderate vegetation
  - **Right side (0.3+)**: Dense, healthy vegetation

##### 3. Color Legend
- **Purpose**: Reference for interpreting overlay colors
- **Scale**: Maps NDVI values to colors used in the overlay

##### 4. Crop Yield Estimate
Statistical information including:
- **Crop Type**: Selected crop
- **Total Area**: Total analyzed area in hectares
- **Vegetated Area**: Area covered by vegetation
- **Average Yield**: Expected yield per hectare for selected crop
- **Estimated Total Yield**: Calculated total yield in tons

## Understanding NDVI Values

### NDVI Basics
- **Range**: -1 to +1
- **Calculation**: (Near Infrared - Red) / (Near Infrared + Red)
- **Purpose**: Measures vegetation health and density

### NDVI Interpretation
| NDVI Range | Vegetation Type | Description |
|------------|----------------|-------------|
| -1.0 to -0.1 | Water/No vegetation | Water bodies, concrete, bare soil |
| -0.1 to 0.1 | Barren | Very sparse or no vegetation |
| 0.1 to 0.3 | Sparse vegetation | Grasslands, sparse crops |
| 0.3 to 0.6 | Moderate vegetation | Healthy crops, forests |
| 0.6 to 1.0 | Dense vegetation | Very healthy, dense vegetation |

## Best Practices

### Area Selection
1. **Start Small**: Begin with areas < 5 km² to familiarize yourself with the interface
2. **Cloud-Free Areas**: Choose areas with minimal cloud cover
3. **Homogeneous Crops**: Select areas with uniform crop types for more accurate estimates
4. **Seasonal Timing**: Consider the growing season of your target crop

### Analysis Settings
1. **Resolution Selection**:
   - **Detailed Analysis**: Use 1-5 meters per pixel
   - **Regional Overview**: Use 10-20 meters per pixel
   - **Quick Assessment**: Use 20+ meters per pixel

2. **Layer Selection**:
   - **Crop Health**: Use NDVI
   - **Water Stress**: Use Moisture Index
   - **Visual Assessment**: Use True Color
   - **Vegetation Structure**: Use False Color

### Interpreting Results
1. **Cross-Reference**: Compare NDVI overlay with true color image
2. **Histogram Analysis**: Look for bimodal distributions (vegetation vs. non-vegetation)
3. **Seasonal Considerations**: NDVI values vary by growth stage
4. **Field Validation**: Ground-truth results when possible

## Troubleshooting

### Common Issues

#### No Results Displayed
**Possible Causes**:
- Area too large (reduce size or increase resolution value)
- Network connectivity issues
- Sentinel Hub API limits exceeded

**Solutions**:
1. Try a smaller area
2. Check internet connection
3. Wait and retry (API limits reset daily)

#### Poor Image Quality
**Possible Causes**:
- High resolution value
- Cloud cover in the area
- Atmospheric conditions

**Solutions**:
1. Lower the resolution value (higher quality)
2. Select a different area or time period
3. Try different satellite layers

#### Unrealistic Yield Estimates
**Possible Causes**:
- Wrong crop type selected
- Area includes non-agricultural land
- NDVI analysis on non-vegetated areas

**Solutions**:
1. Verify crop type selection
2. Draw more precise boundaries around crop fields
3. Exclude roads, buildings, and water bodies

### Error Messages

#### "Please draw an area on the map first"
- **Cause**: No rectangle drawn on the map
- **Solution**: Use the rectangle tool to draw an analysis area

#### "Invalid bounding box"
- **Cause**: Drawing coordinates are invalid
- **Solution**: Redraw the rectangle and ensure it's within valid geographic bounds

#### "Error fetching data from Sentinel Hub"
- **Cause**: External API issue or network problem
- **Solution**: Check internet connection and retry after a few minutes

## Advanced Features

### Comparing Different Time Periods
1. Analyze the same area multiple times
2. Save/screenshot results for comparison
3. Note seasonal changes in NDVI values

### Multi-Layer Analysis
1. Analyze the same area with different layers
2. Compare True Color, NDVI, and Moisture Index
3. Cross-validate findings across layers

### Yield Optimization
1. Identify areas with low NDVI values
2. Correlate with field management practices
3. Plan targeted interventions for improvement

## Limitations

### Technical Limitations
- Maximum processing area: ~50 km² (depending on resolution)
- Image resolution: Limited by Sentinel satellite capabilities
- Processing time: Depends on area size and server load

### Data Limitations
- **Cloud Cover**: Can obscure ground features
- **Temporal Resolution**: Snapshot in time, not continuous monitoring
- **Atmospheric Effects**: Can affect spectral values

### Analysis Limitations
- **Yield Estimates**: Based on general crop coefficients, not field-specific data
- **Crop Type Detection**: Manual selection required
- **Mixed Pixels**: Large pixels may contain multiple land cover types

## Tips for Accurate Analysis

1. **Season Selection**: Analyze during peak growing season for best results
2. **Weather Conditions**: Choose clear, cloud-free days
3. **Field Knowledge**: Combine satellite analysis with ground observations
4. **Multiple Analyses**: Compare results across different dates
5. **Validation**: Cross-check estimates with actual yield data when available

## Contact and Support

For technical issues or questions about satellite data interpretation, consult:
- Application documentation
- Sentinel Hub documentation
- Remote sensing textbooks and resources
- Agricultural extension services for crop-specific guidance
