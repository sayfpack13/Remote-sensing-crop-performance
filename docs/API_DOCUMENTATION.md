# API Documentation

## Overview

This document provides comprehensive documentation for the Remote Sensing Crop Performance API endpoints and their functionality.

## Base URL

```
http://127.0.0.1:5000
```

## Endpoints

### 1. GET `/`

**Description:** Serves the main application interface.

**Response:** HTML page with the interactive map and controls.

**Template:** `templates/index.html`

**Context Variables:**
- `wms_layers`: Dictionary of available WMS layer names and their corresponding layer IDs

---

### 2. POST `/process_area`

**Description:** Processes a selected area on the map for crop analysis.

#### Request Body

```json
{
  "bbox": [min_lat, min_lon, max_lat, max_lon],
  "resolution": 5.0,
  "layer": "3_NDVI",
  "crop": "wheat"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `bbox` | Array[Float] | Yes | Bounding box coordinates [min_lat, min_lon, max_lat, max_lon] |
| `resolution` | Float | No | Image resolution in meters per pixel (default: 5.0) |
| `layer` | String | No | WMS layer ID for analysis (default: "1_TRUE_COLOR") |
| `crop` | String | No | Crop type for yield estimation (default: "wheat") |

#### Supported Crop Types

- `wheat` - Wheat (8.0 tons/ha)
- `corn` - Corn (12.0 tons/ha)
- `barley` - Barley (6.5 tons/ha)
- `rice` - Rice (7.5 tons/ha)
- `oats` - Oats (5.0 tons/ha)
- `rye` - Rye (6.0 tons/ha)

#### Supported WMS Layers

| Layer Name | Layer ID | Description |
|------------|----------|-------------|
| True Color | 1_TRUE_COLOR | Natural color RGB composite |
| False Color | 2_FALSE_COLOR | False color infrared composite |
| False Color Urban | 4-FALSE-COLOR-URBAN | Urban-optimized false color |
| NDVI | 3_NDVI | Normalized Difference Vegetation Index |
| Moisture Index | 5-MOISTURE-INDEX1 | Soil and vegetation moisture |
| NDSI (Snow) | 8-NDSI | Normalized Difference Snow Index |
| NDWI (Water) | 7-NDWI | Normalized Difference Water Index |
| SWIR | 6-SWIR | Short Wave Infrared |

#### Response

##### Success Response (200)

```json
{
  "success": true,
  "layer_used": "3_NDVI",
  "true_color_url": "/static/outputs/true_color.png",
  "overlay_url": "/static/outputs/ndvi_overlay.png",
  "histogram_url": "/static/outputs/ndvi_histogram.png",
  "legend_url": "/static/outputs/ndvi_legend.png",
  "classification": {
    "water_pixels": 1234,
    "barren_pixels": 5678,
    "sparse_pixels": 9012,
    "dense_pixels": 3456,
    "unclassified_pixels": 789
  },
  "total_area_hectares": 150.75,
  "vegetated_area_hectares": 125.50,
  "avg_yield_tons_per_ha": 8.0,
  "estimated_yield_tons": 1004.0,
  "crop": "Wheat",
  "resolution": 5.0
}
```

##### Error Response (400/500)

```json
{
  "success": false,
  "error": "Error description"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | Boolean | Indicates if the request was successful |
| `layer_used` | String | The WMS layer ID that was analyzed |
| `true_color_url` | String | URL to the true color satellite image |
| `overlay_url` | String | URL to the NDVI overlay image (NDVI layer only) |
| `histogram_url` | String | URL to the NDVI histogram (NDVI layer only) |
| `legend_url` | String | URL to the NDVI legend (NDVI layer only) |
| `classification` | Object | Pixel classification counts (NDVI layer only) |
| `total_area_hectares` | Float | Total area of the selected region in hectares |
| `vegetated_area_hectares` | Float | Area covered by vegetation in hectares |
| `avg_yield_tons_per_ha` | Float | Average yield per hectare for the selected crop |
| `estimated_yield_tons` | Float | Estimated total yield in tons |
| `crop` | String | Human-readable crop name |
| `resolution` | Float | Actual resolution used for the analysis |

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful request
- `400 Bad Request` - Invalid request parameters (e.g., invalid bounding box)
- `500 Internal Server Error` - Server-side errors (e.g., Sentinel Hub API issues)

Common error scenarios:

1. **Invalid Bounding Box**: When bbox parameter is missing or contains invalid coordinates
2. **Sentinel Hub API Error**: When the external Sentinel Hub service is unavailable
3. **Image Processing Error**: When there's an issue processing the satellite imagery

## Rate Limiting

No explicit rate limiting is implemented, but requests are limited by:
- Sentinel Hub API rate limits
- Server processing capacity for image analysis

## Notes

- All generated images are cached in the `static/outputs/` directory
- Image URLs include timestamp parameters to prevent browser caching
- NDVI-specific outputs (overlay, histogram, legend, classification) are only generated when analyzing the NDVI layer
