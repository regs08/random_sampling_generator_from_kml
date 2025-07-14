# 🔧 Core Features

Detailed explanations of the Random Sampling Point Generator's core capabilities.

## Per-Polygon Sampling

### How It Works
Each polygon in the KML file gets exactly the specified number of sampling points, regardless of polygon size or shape.

### Key Benefits
- **Consistent Coverage**: Every polygon receives equal attention
- **Predictable Output**: Know exactly how many points you'll get
- **Flexible Analysis**: Compare results across different polygon types

### Implementation Details
- Unique random seed per polygon ensures different point distributions
- Minimum distance constraints applied within each polygon
- Invalid polygons are skipped with warnings

### Example
```bash
# Generate 5 points per polygon
python -m random_sampling.cli --file data/vineyard.kml --n_points 5 --output samples.csv
# Result: 10 polygons → 50 total points (5 per polygon)
```

## Minimum Distance Spacing

### Purpose
Prevents clustering of sampling points by ensuring a minimum distance between all points within each polygon.

### Default Behavior
- **Default Distance**: 5 meters between points
- **Automatic Conversion**: Meters converted to degrees based on field latitude
- **Per-Polygon**: Distance constraints apply within each polygon, not across polygons

### Technical Implementation
```python
# Conversion formula (simplified)
degrees_per_meter = 1 / (111320 * cos(latitude_radians))
min_distance_degrees = min_distance_meters * degrees_per_meter
```

### Customization
```bash
# Use 10-meter spacing
--min_distance_meters 10

# Use 2-meter spacing for high-density sampling
--min_distance_meters 2
```

### Benefits
- **Prevents Clustering**: Ensures even distribution of points
- **Maintains Quality**: Avoids redundant sampling in small areas
- **Flexible**: Adjustable based on field requirements

## KML Attribute Extraction

### Supported Attributes
The system extracts and makes available for filtering:

| Attribute | Source | Description |
|-----------|--------|-------------|
| `name` | KML Placemark name | Human-readable polygon identifier |
| `styleUrl` | KML style reference | Visual styling information |
| `description` | KML description | Detailed polygon information |
| `data_Name` | KML ExtendedData | Custom data fields |

### Extraction Process
1. **Parse KML Structure**: Navigate complex nested elements
2. **Extract Coordinates**: Convert KML coordinate format to polygon geometry
3. **Extract Attributes**: Parse name, style, description, and extended data
4. **Validate**: Ensure polygon geometry is valid
5. **Store**: Associate attributes with polygon objects

### Example KML Structure
```xml
<Placemark>
  <name>Chardonnay Block A</name>
  <styleUrl>#poly-3949AB-2000-76</styleUrl>
  <description>VGB - Chardonnay variety</description>
  <ExtendedData>
    <Data name="FieldType">
      <value>Vineyard</value>
    </Data>
  </ExtendedData>
  <Polygon>
    <coordinates>-77.046,42.870 -77.045,42.871 ...</coordinates>
  </Polygon>
</Placemark>
```

### Robust Parsing
- **Error Handling**: Gracefully handles malformed KML files
- **Flexible Structure**: Supports various KML file formats
- **Missing Data**: Continues processing even with missing attributes

## CSV Export

### Output Format
The system generates clean, GIS-compatible CSV files with:

| Column | Description | Example |
|--------|-------------|---------|
| `longitude` | X coordinate in decimal degrees | `-77.046123` |
| `latitude` | Y coordinate in decimal degrees | `42.870456` |
| `sample_name` | Intelligent identifier reflecting command arguments | `SAMPLE_TRIANGLE_P3_0001` |
| `point_id` | Sequential point identifier | `1` |
| `metadata_*` | Custom metadata columns | `Study2024` |

### Intelligent Sample Naming

Sample names automatically reflect the command arguments used, making them descriptive and traceable:

**Naming Pattern**: `{PREFIX}_{FILTER}_{POINTS}_{DISTANCE}_{SEQUENTIAL_NUMBER}`

**Examples**:
- `SAMPLE_P5_0001` - Basic sampling with 5 points
- `SAMPLE_TRIANGLE_P3_0001` - Triangle filter with 3 points  
- `TEST_RECTANGLE_P4_D10M_0001` - Rectangle filter, 4 points, 10m distance, TEST prefix
- `SAMPLE_TRIANGLE_P2_0001` - Name filter (Triangle Farm) with 2 points

**Benefits**:
- **Descriptive**: Names immediately tell you what parameters were used
- **Sortable**: Names sort logically by filter, then by sequence
- **Traceable**: Easy to identify which samples came from which command
- **Flexible**: Adapts to different filter types and custom settings

### Metadata Support
Add custom metadata to track sampling context:

```bash
--metadata "project=Study2024" --metadata "researcher=John" --metadata "date=2024-01-15"
```

### GIS Compatibility
- **Coordinate System**: WGS84 (EPSG:4326)
- **Format**: Standard CSV with headers
- **Software**: Compatible with QGIS, ArcGIS, R, Python

### Customization
```bash
# Custom sample prefix
--sample_prefix "FIELD"

# Output format options
--format csv      # Default CSV format
--format geojson  # GeoJSON format for web mapping
```

## Random Seed Management

### Per-Polygon Seeds
Each polygon gets a unique random seed to ensure:
- **Different Distributions**: Points don't cluster in similar patterns
- **Reproducibility**: Same seed produces same results
- **Variety**: Natural variation in point placement

### Seed Generation
```python
# Automatic seed generation (simplified)
base_seed = user_seed or random.randint(1, 1000000)
polygon_seed = base_seed + polygon_index
```

### Custom Seeds
```bash
# Use specific seed for reproducibility
--seed 12345

# Different seeds for different runs
--seed 12345  # First run
--seed 67890  # Second run
```

## Filtering System

### Attribute-Based Filtering
Filter polygons by any extracted KML attribute:

```bash
# Filter by name
--apply_to_group "name=Chardonnay"

# Filter by style
--apply_to_group "styleUrl=poly-3949AB-2000-76"

# Filter by description
--apply_to_group "description=vgb"

# Filter by extended data
--apply_to_group "data_FieldType=Vineyard"
```

### Filtering Behavior
- **Case-Insensitive**: Matches regardless of case
- **Partial Matching**: Finds polygons containing specified text
- **Multiple Matches**: Multiple polygons can match same filter
- **Per-Polygon Sampling**: Each matching polygon gets specified points

### Use Cases
- **Variety Studies**: Sample only specific grape varieties
- **Style Analysis**: Sample polygons with same visual style
- **Description Filtering**: Sample based on text descriptions
- **Custom Data**: Sample based on extended KML data

## Error Handling and Validation

### Polygon Validation
- **Geometry Check**: Ensures polygons are valid geometric shapes
- **Coordinate Validation**: Checks coordinate ranges and format
- **Size Limits**: Handles very small or very large polygons

### Robust Processing
- **Skip Invalid**: Continues processing even with bad polygons
- **Warning Messages**: Informs user about skipped polygons
- **Partial Results**: Returns results for valid polygons only

### User Feedback
- **Progress Indicators**: Shows processing status
- **Error Context**: Provides helpful error messages
- **Verbose Logging**: Detailed information for debugging

## Performance Optimizations

### Efficient Algorithms
- **Spatial Indexing**: Fast point-in-polygon tests
- **Optimized Distance**: Efficient minimum distance calculations
- **Memory Management**: Minimal memory footprint

### Scalability
- **Linear Scaling**: Performance scales with polygon count
- **Large Files**: Handles KML files with hundreds of polygons
- **Resource Efficient**: Minimal CPU and memory usage

### Future Enhancements
- **Parallel Processing**: Multi-core polygon processing
- **Streaming**: Handle very large files without loading into memory
- **Caching**: Cache parsed KML data for repeated use 