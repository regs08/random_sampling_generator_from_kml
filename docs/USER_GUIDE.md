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
# Filter by grape variety name
--apply_to_group "name=Chardonnay"

# Filter by style (same color/style polygons)
--apply_to_group "styleUrl=poly-3949AB-2000-76"

# Filter by description content
--apply_to_group "description=vgb"
--apply_to_group "description=vgs"

# Filter by extended data
--apply_to_group "data_Name=Arandell"
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
python -m random_sampling.cli --file data/field.kml --n_points 5 --output samples.csv

# Generate 10 points per polygon with 10-meter spacing
python -m random_sampling.cli --file data/field.kml --n_points 10 --min_distance_meters 10 --output samples.csv
```

### Filtered Sampling

```bash
# Sample only Chardonnay polygons
python -m random_sampling.cli --file data/vineyard.kml --n_points 3 --apply_to_group "name=Chardonnay" --output chardonnay.csv

# Sample polygons with specific style
python -m random_sampling.cli --file data/vineyard.kml --n_points 5 --apply_to_group "styleUrl=poly-3949AB-2000-76" --output red_style.csv

# Sample polygons with "vgb" in description
python -m random_sampling.cli --file data/vineyard.kml --n_points 2 --apply_to_group "description=vgb" --output vgb_samples.csv
```

### Advanced Options

```bash
# Use custom sample prefix and add metadata
python -m random_sampling.cli --file data/field.kml --n_points 5 --sample_prefix "FIELD" --metadata "project=Study2024" --metadata "researcher=John" --output field_samples.csv

# Set random seed for reproducible results
python -m random_sampling.cli --file data/field.kml --n_points 5 --seed 12345 --output reproducible_samples.csv

# Enable verbose logging
python -m random_sampling.cli --file data/field.kml --n_points 5 --verbose --output samples.csv

# Generate GeoJSON instead of CSV
python -m random_sampling.cli --file data/field.kml --n_points 5 --format geojson --output samples.geojson
```

## Output Format

### CSV Output
The default CSV output contains:
- `longitude`: X coordinate in decimal degrees
- `latitude`: Y coordinate in decimal degrees
- `sample_name`: Unique identifier (e.g., SAMPLE_1, SAMPLE_2)
- `polygon_index`: Index of the source polygon
- Additional metadata columns (if specified)

### Example CSV Output
```csv
longitude,latitude,sample_name,polygon_index,project,researcher
-77.046123,42.870456,SAMPLE_1,0,Study2024,John
-77.045789,42.870789,SAMPLE_2,0,Study2024,John
-77.046456,42.871123,SAMPLE_3,1,Study2024,John
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