import matplotlib.colors
from flask import Flask, render_template, request, jsonify, url_for
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import cv2
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm

app = Flask(__name__)

# Replace this with your actual instance ID
SENTINEL_INSTANCE_ID = 'd7482dab-6310-4b9e-a829-b380b4ae9f7e'



# Available WMS Layers from Sentinel Hub
WMS_LAYERS = {
    "True Color": "1_TRUE_COLOR",
    "False Color": "2_FALSE_COLOR",
    "False Color Urban": "4-FALSE-COLOR-URBAN",
    "NDVI": "3_NDVI",
    "Moisture Index": "5-MOISTURE-INDEX1",
    "NDSI (Snow)": "8-NDSI",
    "NDWI (Water)": "7-NDWI",
    "SWIR": "6-SWIR"
}

# Crop yield per hectare (tons/ha)
CROP_YIELD_DATA = {
    "wheat": {"name": "Wheat", "yield_tons_per_ha": 8.0},
    "corn": {"name": "Corn", "yield_tons_per_ha": 12.0},
    "barley": {"name": "Barley", "yield_tons_per_ha": 6.5},
    "rice": {"name": "Rice", "yield_tons_per_ha": 7.5},
    "oats": {"name": "Oats", "yield_tons_per_ha": 5.0},
    "rye": {"name": "Rye", "yield_tons_per_ha": 6.0}
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def get_image_dimensions_for_bbox(bbox, resolution_meters=2, max_pixels=1024):
    min_lat, min_lon, max_lat, max_lon = bbox
    width_m = haversine(min_lat, min_lon, min_lat, max_lon)
    height_m = haversine(min_lat, min_lon, max_lat, min_lon)
    width_px = int(width_m / resolution_meters)
    height_px = int(height_m / resolution_meters)
    if max(width_px, height_px) > max_pixels:
        scale = max_pixels / max(width_px, height_px)
        width_px = int(width_px * scale)
        height_px = int(height_px * scale)
    return max(1, width_px), max(1, height_px)

def download_wms_image(bbox, layer_id, resolution_meters=None, width_px=None, height_px=None):
    url = f"https://services.sentinel-hub.com/ogc/wms/{SENTINEL_INSTANCE_ID}"
    params = {
        'SERVICE': 'WMS',
        'REQUEST': 'GetMap',
        'LAYERS': layer_id,
        'FORMAT': 'image/png', # Always request PNG as we are interpreting its colors or values
        'CRS': 'EPSG:4326',
        'BBOX': ','.join(map(str, bbox)),
        'MAXCC': 20,
        'ATMOSPHERIC_CORRECTION': 'TRUE'
    }

    if width_px and height_px:
        params['WIDTH'] = width_px
        params['HEIGHT'] = height_px
    else:
        params['RESX'] = f'{resolution_meters}m'
        params['RESY'] = f'{resolution_meters}m'

    response = requests.get(url, params=params)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGB") # Convert to RGB to ensure 3 bands
    return np.array(img)

# Define the precise color ranges and hex codes from the user's provided website information
# Each entry: (lower_bound_NDVI, upper_bound_NDVI, [R,G,B]_normalized, simplified_category_name)
EVALSCRIPT_COLOR_MAP = [
    (-1.0, -0.5, [0.05, 0.05, 0.05], 'water_or_very_low_veg'), # Blackish for Water/Very Low
    (-0.5, 0.0, [234/255, 234/255, 234/255], 'barren_light_gray'), # Light gray for Barren
    (0.0, 0.1, [204/255, 198/255, 130/255], 'sparse_yellow_green'),  # Yellow-green for Sparse
    (0.1, 0.2, [145/255, 191/255, 81/255], 'mod_light_green'),      # Light green for Moderate
    (0.2, 0.3, [112/255, 163/255, 63/255], 'mod_medium_green'),     # Medium green for Moderate
    (0.3, 0.4, [79/255, 137/255, 45/255], 'mod_darker_green'),     # Darker green for Moderate
    (0.4, 0.5, [48/255, 109/255, 28/255], 'dense_dark_green'),     # Dark green for Dense
    (0.5, 0.6, [15/255, 84/255, 10/255], 'very_dense_dark_green'),# Very dark green for Very Dense
    (0.6, 1.0, [0/255, 68/255, 0/255], 'highest_dense_green')   # Deepest green for Highest Dense
]

def get_ndvi_category_and_color(ndvi_value):
    """
    Given a numerical NDVI value, returns its category name and normalized RGB color
    based on the EVALSCRIPT_COLOR_MAP.
    """
    for lower, upper, color, name in EVALSCRIPT_COLOR_MAP:
        if lower <= ndvi_value <= upper:
            return name, color
    return 'unclassified', [0.0, 0.0, 0.0] # Default for out of range or unclassified

def to_255_rgb(color_norm):
    """Converts a normalized RGB color (0-1 range) to 0-255 RGB tuple."""
    return [int(c * 255) for c in color_norm]

def classify_ndvi(ndvi_array):
    """
    Classifies NDVI pixels into broader categories (water, barren, sparse, dense)
    based on numerical NDVI values and the EVALSCRIPT_COLOR_MAP.
    """
    classification_counts = {
        'water_pixels': 0,
        'barren_pixels': 0,
        'sparse_pixels': 0,
        'dense_pixels': 0,
        'unclassified_pixels': 0,
    }

    # Flatten the array to iterate over individual NDVI values efficiently
    flat_ndvi = ndvi_array.flatten()

    for ndvi_value in flat_ndvi:
        category_name, _ = get_ndvi_category_and_color(ndvi_value)
        
        # Aggregate into broader categories
        if 'water_or_very_low_veg' in category_name:
            classification_counts['water_pixels'] += 1
        elif 'barren' in category_name:
            classification_counts['barren_pixels'] += 1
        elif 'sparse' in category_name or 'mod_' in category_name:
            # Sparse includes sparse and all moderate categories
            classification_counts['sparse_pixels'] += 1
        elif 'dense' in category_name or 'highest_dense' in category_name:
            # Dense includes all dense categories
            classification_counts['dense_pixels'] += 1
        else:
            classification_counts['unclassified_pixels'] += 1

    return classification_counts

def create_ndvi_overlay(ndvi_array, true_color_img):
    """
    Creates a colored NDVI overlay using the exact color ramp from EVALSCRIPT_COLOR_MAP.
    The colors are applied based on the numerical NDVI values, ensuring consistency.
    """
    # Ensure overlay has same dimensions and type as true_color_img
    overlay = np.zeros_like(true_color_img, dtype=np.uint8)
    
    # Apply colors based on numerical NDVI values
    for r in range(ndvi_array.shape[0]):
        for c in range(ndvi_array.shape[1]):
            ndvi_value = ndvi_array[r, c]
            _, color_norm = get_ndvi_category_and_color(ndvi_value)
            # Convert RGB (normalized) to BGR (for OpenCV) and assign
            overlay[r, c] = np.array(to_255_rgb(color_norm)[::-1], dtype=np.uint8)

    # Combine the original image with the overlay
    combined = cv2.addWeighted(true_color_img, 0.7, overlay, 0.3, 0) # Adjust alpha values for transparency
    return combined

def generate_legend():
    """
    Generates an NDVI legend based on the Evalscript's color map,
    including key NDVI thresholds and their corresponding colors.
    The colormap is constructed to precisely reflect the color bands defined.
    """
    fig, ax = plt.subplots(figsize=(8, 1))
    fig.subplots_adjust(bottom=0.5)

    min_ndvi = -1.0
    max_ndvi = 1.0

    # Create a list of (normalized_value, color) pairs for the LinearSegmentedColormap
    # This ensures that the color transitions happen exactly at the defined NDVI thresholds
    segmented_colors_data = []
    for i, (lower, upper, color_norm, _) in enumerate(EVALSCRIPT_COLOR_MAP):
        # Normalize the NDVI values to the [0, 1] range for the colormap
        norm_lower = (lower - min_ndvi) / (max_ndvi - min_ndvi)
        norm_upper = (upper - min_ndvi) / (max_ndvi - min_ndvi)
        
        # Add the lower bound of the segment with its color
        segmented_colors_data.append((norm_lower, color_norm))
        # Add the upper bound of the segment with its color to ensure the color holds across the segment
        segmented_colors_data.append((norm_upper, color_norm))
    
    # Sort by the normalized NDVI value to ensure correct order for colormap creation
    segmented_colors_data.sort(key=lambda x: x[0])

    # Remove duplicates, keeping the last occurrence for a given normalized value
    # This handles cases where one segment ends and another begins at the same point
    unique_segmented_colors_data = []
    seen_nodes = {}
    for norm_val, color_rgb in segmented_colors_data:
        seen_nodes[norm_val] = color_rgb # This will overwrite for duplicates, keeping the last (correct) color
    
    # Reconstruct the list in sorted order from the dictionary
    for norm_val in sorted(seen_nodes.keys()):
        unique_segmented_colors_data.append((norm_val, seen_nodes[norm_val]))

    # Create the custom colormap
    custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "custom_ndvi", unique_segmented_colors_data
    )

    norm = plt.Normalize(vmin=min_ndvi, vmax=max_ndvi)

    cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=custom_cmap),
                      cax=ax, orientation='horizontal',
                      ticklocation='bottom')
    cb.set_label('NDVI Value (from Evalscript)')
    
    # Set ticks to key NDVI thresholds from the Evalscript for clarity
    tick_positions = [-0.5, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    tick_labels = [
        '<-0.5 (Water/Very Low)',
        '0.0 (Barren)',
        '0.1 (Sparse)',
        '0.2 (Mod. Light)',
        '0.3 (Mod. Medium)',
        '0.4 (Mod. Dark)',
        '0.5 (Dense)',
        '>=0.6 (Highest Dense)'
    ]
    
    cb.set_ticks(tick_positions)
    cb.set_ticklabels(tick_labels)

    path = 'static/outputs/ndvi_legend.png'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path

@app.route('/')
def index():
    return render_template('index.html', wms_layers=WMS_LAYERS)

@app.route('/process_area', methods=['POST'])
def process_area():
    data = request.get_json()
    bbox = data.get('bbox')
    resolution = float(data.get('resolution', 5))
    layer_name = data.get('layer', '1_TRUE_COLOR')
    crop_type = data.get('crop', 'wheat')

    if not bbox or len(bbox) != 4:
        return jsonify({'success': False, 'error': 'Invalid bounding box'}), 400

    try:
        min_lat, min_lon, max_lat, max_lon = bbox
        width_px, height_px = get_image_dimensions_for_bbox(bbox, resolution, 1024)

        result_data = {'success': True, 'layer_used': layer_name}
        os.makedirs('static/outputs', exist_ok=True)
        true_color_path = 'static/outputs/true_color.png'

        rgb_img = download_wms_image(bbox, layer_name, resolution, width_px, height_px)
        cv2.imwrite(true_color_path, cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR))
        result_data['true_color_url'] = url_for('static', filename='outputs/true_color.png')

        if layer_name == '3_NDVI':
            # Download raw NDVI values from the '3_NDVI-L1C' layer (single band, 0-255)
            # This is specifically for numerical processing and histogram generation.
            ndvi_raw_img = download_wms_image(bbox, '3_NDVI-L1C', resolution, width_px, height_px)
            
            # Ensure ndvi_raw_img is single channel for scaling if it's RGB but represents grayscale.
            if ndvi_raw_img.ndim == 3:
                # Take the first channel, assuming it contains the grayscale NDVI data
                ndvi = ndvi_raw_img[:, :, 0].astype(float) 
            else: # Already single channel
                ndvi = ndvi_raw_img.astype(float)
            
            # Reverting the scaling to map 0 (dark) to +1 (high NDVI) and 255 (light) to -1 (low NDVI).
            # This aligns with the user's observation that high vegetation (darker pixels) should yield positive NDVI.
            ndvi = 1 - (ndvi / 255.0) * 2
            ndvi = np.clip(ndvi, -1, 1) # Ensure values are within the valid NDVI range

            # Classification based on numerical NDVI values
            classification = classify_ndvi(ndvi)

            # Create overlay based on numerical NDVI values
            overlay_img = create_ndvi_overlay(ndvi, rgb_img)
            overlay_path = 'static/outputs/ndvi_overlay.png'
            cv2.imwrite(overlay_path, cv2.cvtColor(overlay_img, cv2.COLOR_RGB2BGR))

            width_m_actual = haversine(min_lat, min_lon, min_lat, max_lon)
            height_m_actual = haversine(min_lat, min_lon, max_lat, min_lon)
            total_area_m2 = width_m_actual * height_m_actual
            total_area_hectares = round(total_area_m2 / 10_000, 2)

            # Vegetated area calculation sums pixels classified as sparse or dense
            vegetated_pixels = classification['sparse_pixels'] + classification['dense_pixels']
            total_image_pixels = ndvi.size # Use the size of the numerical NDVI array
            vegetated_area_hectares = round(total_area_hectares * (vegetated_pixels / total_image_pixels), 2)

            crop_info = CROP_YIELD_DATA.get(crop_type.lower(), CROP_YIELD_DATA['wheat'])
            estimated_yield_tons = round(vegetated_area_hectares * crop_info["yield_tons_per_ha"], 2)

            plt.figure(figsize=(8, 6))
            plt.hist(ndvi.flatten(), bins=20, range=[-1, 1], color='#2a9d8f')
            plt.title("NDVI Distribution")
            plt.xlabel("NDVI Value")
            plt.ylabel("Number of Pixels")
            hist_path = 'static/outputs/ndvi_histogram.png'
            plt.savefig(hist_path, dpi=150)
            plt.close()

            legend_path = generate_legend()

            result_data.update({
                'overlay_url': url_for('static', filename='outputs/ndvi_overlay.png'),
                'histogram_url': url_for('static', filename='outputs/ndvi_histogram.png'),
                'legend_url': url_for('static', filename='outputs/ndvi_legend.png'),
                'classification': classification,
                'total_area_hectares': total_area_hectares,
                'vegetated_area_hectares': vegetated_area_hectares,
                'avg_yield_tons_per_ha': crop_info["yield_tons_per_ha"],
                'estimated_yield_tons': estimated_yield_tons,
                'crop': crop_info['name'],
                'resolution': resolution
            })

        return jsonify(result_data)

    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f"Error fetching data from Sentinel Hub: {e}"}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=False)