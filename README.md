# 📍 Random Sampling Point Generator

## Author

**Cole Regnier**  
Cornell University  
Gold Lab  
[nr466@cornell.edu](mailto:nr466@cornell.edu)

## Overview

Generate random sampling points inside polygon boundaries defined by KML files with minimum distance spacing per polygon.
Designed for agricultural fieldwork and research sampling.

### What It Does
- Loads KML files and extracts polygon boundaries
- Generates random sampling points within each polygon
- Ensures minimum distance spacing between points
- Filters polygons by KML attributes (name, style, description, etc.)
- Exports results to CSV for analysis

### Quick Start
```bash
# Setup environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate sampling points
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --output data/samples.csv
```

**Note**: The test polygons in `data/Test Polygons.kml` have no real-world meaning and are solely used for testing the application functionality.

## 📚 Documentation

- **[🚀 Quick Start Guide](docs/QUICKSTART.md)** - Get up and running in minutes
- **[📖 User Guide](docs/USER_GUIDE.md)** - Complete usage instructions and examples
- **[🛠️ Tech Stack](docs/TECH_STACK.md)** - Technical architecture and dependencies
- **[🔧 Core Features](docs/FEATURES.md)** - Detailed feature explanations
- **[📊 Test Results](docs/TEST_RESULTS.md)** - Validation and performance data
- **[📁 Project Structure](docs/PROJECT_STRUCTURE.md)** - File organization and development guidelines

## Key Features
- ✅ Load KML files with robust lxml-based parsing
- ✅ Parse polygon boundaries from complex KML structures
- ✅ Generate random points per polygon with minimum distance spacing
- ✅ Automatic meters-to-degrees conversion based on field latitude
- ✅ Export results to CSV: longitude, latitude, sample name, metadata
- ✅ **NEW**: Filter polygons by KML attributes (name, styleUrl, description, extended data)
- ✅ **NEW**: Per-polygon sampling with unique random seeds
- ✅ Comprehensive test suite with working examples

---

## 📌 Contributing

See [Project Structure Guide](docs/PROJECT_STRUCTURE.md) for development guidelines and where to add new features.
