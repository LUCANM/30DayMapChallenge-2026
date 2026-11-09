# Data credits and permissions

## OpenStreetMap huts and summit

© OpenStreetMap contributors. OSM-derived JSON and GeoJSON data are offered under the [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/). See [OpenStreetMap copyright and attribution](https://www.openstreetmap.org/copyright).

The snapshot was supplied with this project. Its `osm3s.timestamp_osm_base` is `2026-10-02T05:59:14Z`. Original notes report retrieval on 2 October 2026 through [Overpass API](https://overpass-api.de/). No fresh data query was performed for this portfolio.

Original query, recorded for provenance:

```text
[out:json][timeout:30];(nwr[tourism~"^(alpine_hut|wilderness_hut)$"](45.35,7.05,45.75,7.65);node[natural=peak][name="Gran Paradiso"](45.35,7.05,45.75,7.65););out center meta;
```

Public JSON retains feature identifiers, timestamps, coordinates or bounding-box centres, and the selected tags `name`, `tourism`, `natural`, and `ele`. Contributor user names, user IDs, changesets, and unrelated tags such as email addresses, telephone numbers, websites, and social accounts are omitted. The GeoJSON `tags_json` fields use the same tag allowlist. This is a modified extract, not the complete original response. Positions and the 49 hut records have not been changed.

Node positions are original OSM coordinates; way/relation points are derived Overpass bounding-box centres. Each GeoJSON feature retains an OSM URL. No endorsement by OSM contributors is implied.

## Terrain

Source: [AWS / Mapzen Terrain Tiles](https://registry.opendata.aws/terrain-tiles/), Terrarium zoom 11. The source endpoint is `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png`. Tile coordinates and the study bounding box are in `data/Terrain_tiles.json`.

Source terms and attribution: [Tilezen / Joerd attribution](https://github.com/tilezen/joerd/blob/master/docs/attribution.md). The supplied attribution document is preserved in [Terrain_Attribution.md](Terrain_Attribution.md); it describes the worldwide dataset, not a claim that every listed provider contributed to this map. Source-specific licenses continue to apply.

Regional credit: Europe terrain data produced using Copernicus data and information funded by the European Union — EU-DEM layers. Global SRTM and GMTED2010 terrain data courtesy of the U.S. Geological Survey. The original project reports these sources; exact per-pixel source lineage was not supplied and has not been independently reconstructed.

The inherited workflow decoded Terrarium RGB elevation as `R*256 + G + B/256 - 32768` metres, bilinearly resampled to a 75 m UTM 32N grid, and generated coloured hillshade. `elevation.tif` is numeric elevation; `relief.png` plus its world file and projection file is the artistic georeferenced relief. This portfolio uses those supplied rasters without recalculating elevation.

## Code, artwork, and fonts

The code and artwork are supplied project materials, revised for portability and publication review. No new open license has been granted for original code or artwork. This does not alter OSM or terrain terms. The Python renderer uses Matplotlib's bundled DejaVu fonts; no separate font files are redistributed.

Credit checks used the linked OSM copyright page, AWS dataset listing, and Tilezen attribution page. Retain these credits when sharing the map or its datasets.
