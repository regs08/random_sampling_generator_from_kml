# 🛠️ Tech Stack

Technical architecture and dependencies for the Random Sampling Point Generator.

## Component Architecture

| Component    | Libraries       | Purpose |
|--------------|-----------------|---------|
| **Loader**   | lxml            | Parse KML with XPath queries |
| **Boundary** | shapely, pyproj | Handle polygon operations and filtering |
| **Generator**| numpy, shapely  | Create random points with minimum distance |
| **Exporter** | pandas          | Write CSV files with metadata |
| **CLI**      | argparse        | Command-line interface |
| **Tests**    | pytest          | Unit testing framework |

## Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `lxml` | Latest | XML/KML parsing with XPath support |
| `shapely` | Latest | Geometric operations and polygon handling |
| `numpy` | Latest | Numerical operations and random number generation |
| `pandas` | Latest | Data manipulation and CSV export |
| `pyproj` | Latest | Coordinate system transformations |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | Latest | Unit testing framework |
| `black` | Latest | Code formatting |
| `flake8` | Latest | Code linting |

## Architecture Principles

### Modular Design
- **Single Responsibility**: Each module handles one specific aspect
- **Loose Coupling**: Modules communicate through well-defined interfaces
- **High Cohesion**: Related functionality is grouped together

### Component Responsibilities

#### Loader (`loader.py`)
- Parse KML files using lxml and XPath
- Extract polygon coordinates and attributes
- Handle complex KML structures and malformed files
- Extract name, styleUrl, description, and extended data

#### Boundary (`boundary.py`)
- Manage polygon collections and operations
- Handle coordinate transformations
- Implement filtering by KML attributes
- Validate polygon geometry

#### Generator (`generator.py`)
- Generate random points within polygons
- Implement minimum distance constraints
- Use unique random seeds per polygon
- Handle edge cases and retry logic

#### Exporter (`exporter.py`)
- Export sampling points to CSV/GeoJSON
- Handle metadata and sample naming
- Format output for GIS compatibility

#### CLI (`cli.py`)
- Parse command-line arguments
- Coordinate workflow between components
- Provide user-friendly error messages
- Handle logging and output

#### Utils (`utils.py`)
- Coordinate conversion utilities
- Meters-to-degrees conversion based on latitude
- Common helper functions

## Data Flow

```
KML File → Loader → Boundary Handler → Generator → Exporter → CSV/GeoJSON
                ↓
            Filtering (optional)
```

### Step-by-Step Process

1. **Loading**: KML file parsed using lxml with XPath queries
2. **Extraction**: Polygon coordinates and attributes extracted
3. **Filtering**: Optional filtering by KML attributes
4. **Generation**: Random points generated with minimum distance constraints
5. **Export**: Results formatted and written to output file

## Coordinate Systems

### Input
- **KML Format**: WGS84 (EPSG:4326) - longitude, latitude
- **Units**: Decimal degrees

### Processing
- **Internal**: WGS84 (EPSG:4326) for consistency
- **Distance**: Meters converted to degrees based on field latitude

### Output
- **CSV**: WGS84 (EPSG:4326) - longitude, latitude
- **GeoJSON**: WGS84 (EPSG:4326) with proper GeoJSON structure

## Performance Considerations

### Memory Usage
- Polygons loaded into memory for processing
- Large KML files may require significant RAM
- Consider streaming for very large datasets

### Processing Speed
- lxml provides fast XML parsing
- Shapely optimized for geometric operations
- NumPy efficient for random number generation

### Scalability
- Linear scaling with number of polygons
- Minimum distance algorithm complexity: O(n²) per polygon
- Consider parallel processing for large datasets

## Error Handling

### Robust Parsing
- Graceful handling of malformed KML files
- Skip invalid polygons with warnings
- Continue processing even with partial failures

### Validation
- Polygon geometry validation
- Coordinate range checking
- Attribute extraction error handling

### User Feedback
- Clear error messages with context
- Verbose logging for debugging
- Progress indicators for long operations

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock data for isolated testing
- Edge case coverage

### Integration Tests
- End-to-end workflow testing
- Real KML file processing
- Output format validation

### Performance Tests
- Large file processing
- Memory usage monitoring
- Processing time benchmarks 