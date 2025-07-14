# 🚀 Quick Start Guide

Get up and running with the Random Sampling Point Generator in minutes.

## Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

## Installation

```bash
# Clone the repository
git clone https://github.com/regs08/random_sampling_generator_from_kml.git
cd random_sampling_generator_from_kml

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Examples

### 1. Basic Sampling
Generate 5 random points in each polygon:
```bash
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --output samples.csv
```

### 2. Filter by Group
Sample only triangle polygons:
```bash
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 3 --apply_to_group "description=triangle" --output triangle_samples.csv
```

Sample only rectangle polygons:
```bash
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 3 --apply_to_group "description=rectangle" --output rectangle_samples.csv
```

### 3. Filter by Name
Sample a specific polygon by name:
```bash
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 4 --apply_to_group "name=Triangle Farm" --output triangle_farm.csv
```

### 4. Custom Settings
Generate points with custom spacing and metadata:
```bash
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --min_distance_meters 10 --sample_prefix "TEST" --metadata "project=Demo" --output custom_samples.csv
```

## Test Data

The `data/Test Polygons.kml` file contains:
- **4 test polygons** with no real-world meaning
- **Triangle group**: 2 polygons with `description="triangle"`
- **Rectangle group**: 2 polygons with `description="rectangle"`
- **Different styles**: Black and blue polygon styles for testing

## Output

The tool generates CSV files with:
- `longitude,latitude`: Coordinates in decimal degrees
- `sample_name`: Intelligent identifier reflecting command arguments
- `point_id`: Sequential point identifier
- Additional metadata columns (if specified)

### Intelligent Sample Naming

Sample names automatically reflect the command arguments used:

**Basic sampling (5 points)**:
```csv
sample_name,longitude,latitude,point_id
SAMPLE_P5_0001,-77.034215,42.836205,1
SAMPLE_P5_0002,-77.032971,42.836686,2
```

**Triangle filter (3 points)**:
```csv
sample_name,longitude,latitude,point_id
SAMPLE_TRIANGLE_P3_0001,-77.031614,42.834642,1
SAMPLE_TRIANGLE_P3_0002,-77.032509,42.834086,2
```

**Rectangle filter with custom settings (4 points, 10m distance, TEST prefix)**:
```csv
sample_name,longitude,latitude,point_id
TEST_RECTANGLE_P4_D10M_0001,-77.024034,42.836818,1
TEST_RECTANGLE_P4_D10M_0002,-77.022575,42.836581,2
```

**Naming Pattern**: `{PREFIX}_{FILTER}_{POINTS}_{DISTANCE}_{SEQUENTIAL_NUMBER}`
- **PREFIX**: Base prefix (SAMPLE) or custom prefix
- **FILTER**: Filter group (TRIANGLE, RECTANGLE) or first word of name
- **POINTS**: Point count if not default (P3, P5)
- **DISTANCE**: Distance if not default (D10M for 10 meters)
- **SEQUENTIAL**: Sequential numbering (0001, 0002, etc.)

## Next Steps

- Read the [User Guide](USER_GUIDE.md) for detailed usage
- Check [Test Results](TEST_RESULTS.md) for validation data
- Explore [Core Features](FEATURES.md) for advanced functionality 