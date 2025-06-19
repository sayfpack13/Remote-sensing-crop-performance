# Remote Sensing Crop Performance

## Project Overview

This web application provides an interactive platform for analyzing crop health and estimating yield using satellite imagery. Leveraging WMS (Web Map Service) layers from Sentinel Hub, users can define an area of interest on a map, select different satellite layers (e.g., True Color, NDVI), and obtain detailed analysis including NDVI classification, a histogram of vegetation indices, and estimated crop yield based on various crop types. The modern, responsive interface allows for seamless exploration of geospatial agricultural data.

## Features

* **Interactive Map:** Explore satellite imagery using a Leaflet-based map interface.
* **WMS Layer Preview:** Switch between various Sentinel Hub WMS layers (True Color, NDVI, False Color, Moisture Index, etc.) directly on the map for live visualization.
* **Area of Interest Selection:** Draw a rectangular area on the map to define the region for analysis.
* **Configurable Analysis:**
    * Select the specific satellite layer for in-depth analysis (e.g., NDVI for vegetation health).
    * Adjust the desired image resolution (meters per pixel).
    * Choose a crop type for tailored yield estimations.
* **Comprehensive Output:**
    * Display of the analyzed satellite image.
    * NDVI overlay highlighting dense vegetation.
    * NDVI histogram showing vegetation distribution.
    * Categorized pixel classification (Water, Barren, Sparse, Dense vegetation).
    * Calculated total and vegetated area in hectares.
    * Estimated crop yield in tons, based on the selected crop type and vegetated area.
* **Modern User Interface:** A clean, responsive design with intuitive controls and visual enhancements using Font Awesome icons.
* **Loading Indicator:** Provides feedback during analysis processing.

## Technologies Used

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, JavaScript
* **Mapping Library:** Leaflet.js
* **Map Drawing Tool:** Leaflet.draw
* **Satellite Data:** Sentinel Hub WMS API
* **Image Processing:** PIL (Pillow), OpenCV (cv2)
* **Data Visualization:** Matplotlib

## How to Run Locally

To get this project up and running on your local machine, follow these steps:

### Prerequisites

* Python 3.x
* Pip (Python package installer)
* A **Sentinel Hub Instance ID**. You can get one by registering at [Sentinel Hub](https://www.sentinel-hub.com/). Replace `'d7482dab-6310-4b9e-a829-b380b4ae9f7e'` in `app.py` with your own Instance ID.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourGitHubUsername/remote-sensing-crop-performance.git](https://github.com/YourGitHubUsername/remote-sensing-crop-performance.git)
    cd remote-sensing-crop-performance
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install Flask numpy requests Pillow opencv-python matplotlib
    ```

4.  **Set your Sentinel Hub Instance ID:**
    Open `app.py` and replace the placeholder with your actual Sentinel Hub Instance ID:
    ```python
    SENTINEL_INSTANCE_ID = 'YOUR_SENTINEL_HUB_INSTANCE_ID_HERE'
    ```

### Running the Application

1.  **Set Flask environment variable:**
    ```bash
    export FLASK_APP=app.py
    # On Windows: set FLASK_APP=app.py
    ```

2.  **Run the Flask application:**
    ```bash
    flask run
    ```

3.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1.  **Map Interaction:**
    * Use the zoom controls or scroll to navigate the map.
    * Select different **Map Layers** from the dropdown menu located in the top-right corner of the map to preview various satellite data layers.

2.  **Define Area of Interest:**
    * Click the **rectangle icon** (draw tool) on the top-left of the map.
    * Draw a rectangle on the map to define the area you want to analyze. You can edit or delete this rectangle using the edit tools.

3.  **Configure Analysis:**
    * In the control panel (header), choose the **Analysis Layer** (e.g., NDVI for vegetation analysis).
    * Set the desired **Resolution** for the analysis.
    * Select the **Crop Type** relevant to your analysis area for yield estimation.

4.  **Analyze & View Results:**
    * Click the **"Analyze Area"** button.
    * The application will fetch and process the satellite data. A loading spinner will appear during this process.
    * Once complete, the results (analyzed images, histogram, legend, and yield statistics) will be displayed in the output section below the map.

5.  **Reset:**
    * Click the **"Reset Map"** button to clear the drawn area, output, and reset map layers to their defaults.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is open-source and available under the [MIT License](LICENSE.md).