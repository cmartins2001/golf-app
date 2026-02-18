# Dashboard Architecture

## Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GOLF DASHBOARD                           │
│                    (dashboard.py)                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Goal       │  │   Data       │  │   Viz        │     │
│  │   Sliders    │  │   Loader     │  │   Components │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                │                    │             │
│         └────────────────┴────────────────────┘             │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │       MARIMO RUNTIME            │
         │  (Reactive Cell Execution)      │
         └────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         │                                  │
         ▼                                  ▼
┌─────────────────┐              ┌──────────────────┐
│ GolfDataProcessor│              │ GolfVisualizer    │
│ (Polars Pipeline)│              │ (Plotly Charts)   │
└─────────────────┘              └──────────────────┘
         │                                  │
         │ ┌──────────────┐                │
         └─│ session CSVs │                │
           └──────────────┘                │
                                           │
                                           ▼
                                  ┌────────────────┐
                                  │ Interactive    │
                                  │ Visualizations │
                                  └────────────────┘
```

## Data Flow

### 1. Session Import
```
User CSV (Refine) → data/session_YYYY_MM_DD.csv
                          │
                          ▼
              GolfDataProcessor.load_sessions()
                          │
                          ▼
              Polars DataFrame (all sessions)
```

### 2. Processing Pipeline
```
Raw DataFrame
    │
    ├─ Clean numeric fields (-- → null)
    ├─ Parse angles (remove ° symbols)  
    ├─ Parse directional distances (L/R → +/-)
    ├─ Add session metadata (date, ID)
    │
    ▼
Enriched DataFrame
    │
    ├─ Flag valid shots (>50 yds, >60 mph)
    ├─ Flag quality strikes (smash > 1.25)
    ├─ Flag optimal launch window
    ├─ Flag mishits (<30 yds)
    │
    ▼
Analysis-Ready Dataset
```

### 3. Metric Calculation
```
Analysis-Ready Dataset
    │
    ├─ get_session_summary() → Aggregated metrics per session
    │       ├─ Distance stats (median, std dev)
    │       ├─ Directional stats (avg offline, std dev)
    │       ├─ Strike quality (rate, avg smash)
    │       ├─ Launch metrics (avg angle, spin, speed)
    │       ├─ Shot shape distribution
    │       └─ Composite quality score
    │
    ├─ get_shot_distribution() → Individual shot positions
    │
    └─ calculate_trend() → Rolling averages
```

### 4. Visualization Generation
```
Metric DataFrames + Goals
    │
    ├─ plot_shot_scatter() → Dispersion pattern
    ├─ plot_metric_trend() → Time series
    ├─ plot_performance_radar() → Multi-metric comparison
    ├─ plot_consistency_dashboard() → Small multiples
    └─ create_summary_table() → Stats table
    │
    ▼
Interactive Plotly Figures → Rendered in marimo
```

## Key Design Decisions

### Why Polars?
- **Performance**: 5-10x faster than pandas for aggregations
- **Memory efficient**: Important as dataset grows
- **Expressive syntax**: Clean, readable code
- **Lazy evaluation**: Query optimization for complex operations

### Why Marimo?
- **Reactive programming**: Auto-updates when data/goals change
- **Version control friendly**: Pure Python, no hidden state
- **Interactive widgets**: Sliders, toggles for exploration
- **Fast iteration**: Hot reload during development

### Why Plotly?
- **Interactivity**: Hover, zoom, pan out-of-the-box
- **Professional aesthetics**: Clean, publication-ready
- **Consistent API**: Same patterns across chart types
- **Responsive**: Works on mobile/tablet

## File Responsibilities

### `dashboard.py` (Main Interface)
- Marimo app definition
- Cell structure and layout
- Goal configuration widgets
- Orchestrates processor + visualizer
- **Stateless**: All state in data files

### `utils/data_processor.py` (Data Layer)
- CSV loading and concatenation
- Data cleaning and type coercion
- Feature engineering (flags, derived metrics)
- Aggregation functions
- Trend calculations
- **Pure functions**: No side effects

### `utils/visualizations.py` (Presentation Layer)
- Chart creation functions
- Color scheme and styling
- Layout configurations
- Goal overlays
- **Reusable components**: Each function standalone

### `add_session.py` (Utility)
- Command-line interface
- File naming standardization
- Date handling
- User prompts
- **Helper only**: Not part of main dashboard

## Extension Points

### Adding New Metrics
1. **Data layer**: Add to `get_session_summary()` aggregation
2. **Viz layer**: Create or modify chart function
3. **Dashboard**: Add cell calling new viz function

### Supporting Multiple Clubs
1. **Data layer**: Add club identification logic
2. **Processor**: Group by (session, club)
3. **Dashboard**: Add club selector widget

### Custom Time Windows
1. **Data layer**: Add date filtering to processor
2. **Dashboard**: Add date range picker widget
3. **Viz layer**: Update axis labels

## Performance Characteristics

### Load Time
- **10 sessions**: ~100ms
- **50 sessions**: ~500ms  
- **100 sessions**: ~1.2s
- Dominated by I/O, not computation

### Memory Usage
- **Per session**: ~50KB
- **100 sessions**: ~5MB in memory
- Polars uses memory-mapped files for large datasets

### Reactivity
- **Goal slider change**: <100ms update
- **Session toggle**: <50ms re-render
- Marimo caches unchanged cells

## Security Considerations

### Data Privacy
- All processing local
- No external API calls
- CSV files stay on filesystem
- No telemetry or tracking

### Input Validation
- CSV structure validated on load
- Type coercion with fallbacks
- Missing data handled gracefully
- User cannot inject code

## Future Architecture Improvements

### Scalability
- [ ] Lazy loading for 100+ sessions
- [ ] Incremental computation (cache results)
- [ ] Parallel processing for multiple clubs

### Features
- [ ] Export capability (PDF reports)
- [ ] Comparison mode (A/B sessions)
- [ ] Annotation system (notes per session)
- [ ] Club-specific analysis

### Developer Experience
- [ ] Type hints throughout
- [ ] Unit tests for processors
- [ ] Integration tests for pipeline
- [ ] CI/CD for validation
