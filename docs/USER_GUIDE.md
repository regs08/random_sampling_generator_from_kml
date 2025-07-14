# 📖 User Guide

Complete usage instructions and examples for the Random Sampling Point Generator.

## Command Reference

```bash
python -m random_sampling.cli --file <kml_file> --n_points <points_per_polygon> --output <csv_file>
```

### Required Parameters

| Parameter | Short | Description | Example |
|-----------|-------|-------------|---------|
| `--file` | `-f` | Path to input KML file | `--file data/field.kml` |
| `--n_points` | `-n` | Number of sampling points per polygon | `--n_points 5` |
| `--output` | `-o` | Path to output CSV file | `--output samples.csv` |

### Optional Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--min_distance_meters` | | Minimum distance between points in meters | `5.0` |
| `--apply_to_group` | | Filter polygons by KML attribute | None |
| `--seed` | `-s` | Random seed for reproducibility | Auto-generated |
| `--sample_prefix` | | Prefix for sample names | `SAMPLE` |
| `--metadata` | | Additional metadata (key=value format) | None |
| `--format` | | Output format (csv, geojson) | `csv` |
| `--summary` | | Path to save summary report | None |
| `--verbose` | `-v` | Enable verbose logging | False |
| `--quiet` | `-q` | Suppress logging output | False |

## KML Attribute Filtering

The `--apply_to_group` parameter allows filtering polygons by KML attributes.

### Available Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Polygon name | `"Chardonnay"`, `"Arandell"` |
| `styleUrl` | Style reference | `"poly-3949AB-2000-76"` |
| `description` | Description text | `"vgb"`, `"vgs"` |
| `data_Name` | Extended data field | `"FieldType"`, `"Crop"` |

### Filtering Examples

```bash
# Filter by polygon name
--apply_to_group "name=Triangle Farm"

# Filter by style (same color/style polygons)
--apply_to_group "styleUrl=poly-000000-1200-77"

# Filter by description content
--apply_to_group "description=triangle"
--apply_to_group "description=rectangle"

# Filter by extended data
--apply_to_group "data_Name=FieldType"
```

### Filtering Behavior

- **Case-insensitive**: Matches regardless of case
- **Partial matching**: Finds polygons containing the specified text
- **Multiple matches**: Multiple polygons can match the same filter
- **Per-polygon sampling**: Each matching polygon gets the specified number of points

## Usage Examples

### Basic Sampling

```bash
# Generate 5 points per polygon with default 5-meter spacing
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --output samples.csv

# Generate 10 points per polygon with 10-meter spacing
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 10 --min_distance_meters 10 --output samples.csv
```

### Filtered Sampling

```bash
# Sample only Triangle Farm polygons
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 3 --apply_to_group "name=Triangle Farm" --output triangle_farm.csv

# Sample polygons with specific style
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --apply_to_group "styleUrl=poly-000000-1200-77" --output black_style.csv

# Sample polygons with "triangle" in description
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 2 --apply_to_group "description=triangle" --output triangle_samples.csv
```

### Advanced Options

```bash
# Use custom sample prefix and add metadata
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --sample_prefix "TEST" --metadata "project=Study2024" --metadata "researcher=John" --output test_samples.csv

# Set random seed for reproducible results
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --seed 12345 --output reproducible_samples.csv

# Enable verbose logging
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --verbose --output samples.csv

# Generate GeoJSON instead of CSV
python -m random_sampling.cli --file "data/Test Polygons.kml" --n_points 5 --format geojson --output samples.geojson
```

## Output Format

### CSV Output
The default CSV output contains:
- `longitude`: X coordinate in decimal degrees
- `latitude`: Y coordinate in decimal degrees
- `sample_name`: Intelligent identifier reflecting command arguments
- `point_id`: Sequential point identifier
- Additional metadata columns (if specified)

### Intelligent Sample Naming

Sample names automatically reflect the command arguments used, making them descriptive and traceable:

**Naming Pattern**: `{PREFIX}_{FILTER}_{POINTS}_{DISTANCE}_{SEQUENTIAL_NUMBER}`

**Examples**:
- `SAMPLE_P5_0001` - Basic sampling with 5 points
- `SAMPLE_TRIANGLE_P3_0001` - Triangle filter with 3 points
- `TEST_RECTANGLE_P4_D10M_0001` - Rectangle filter, 4 points, 10m distance, TEST prefix
- `SAMPLE_TRIANGLE_P2_0001` - Name filter (Triangle Farm) with 2 points

### Example CSV Output
```csv
longitude,latitude,sample_name,point_id,metadata_project,metadata_researcher
-77.046123,42.870456,SAMPLE_TRIANGLE_P3_0001,1,Study2024,John
-77.045789,42.870789,SAMPLE_TRIANGLE_P3_0002,2,Study2024,John
-77.046456,42.871123,SAMPLE_TRIANGLE_P3_0003,3,Study2024,John
```

## Troubleshooting

### Common Issues

1. **"Input file not found"**
   - Check the file path is correct
   - Ensure the file exists in the specified location

2. **"No valid polygons found"**
   - Verify the KML file contains polygon elements
   - Check that polygons have valid geometry

3. **"Invalid filter format"**
   - Use `field=value` format (e.g., `name=Chardonnay`)
   - Don't use colons (`:`) - use equals (`=`)

4. **"No polygons match filter"**
   - Check the attribute value exists in your KML file
   - Verify the field name is correct (name, styleUrl, description, data_Name)

### Getting Help

- Use `--verbose` flag for detailed logging
- Check the [Test Results](TEST_RESULTS.md) for working examples
- Review the [Core Features](FEATURES.md) for technical details 