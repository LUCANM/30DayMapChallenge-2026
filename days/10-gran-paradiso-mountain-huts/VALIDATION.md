# Validation record

Reviewed locally on 9 November 2026, Windows, Python 3.12.14, QGIS 3.40.11-Bratislava. These checks apply to this portfolio revision, not to unreviewed files in the original archive.

## Completed checks

- Supplied ZIP: all member CRCs passed; extraction paths were checked to remain inside the review folder.
- Offline Python renderer: executed successfully in a new isolated environment using the packages recorded in `requirements.txt`. The renderer was also run from another working directory against a relocated copy.
- Both public scripts compiled successfully. The QGIS builder executed in the installed QGIS Python environment, separately from the poster environment.
- Poster: PNG fully decoded at 3200 × 3000 pixels; web preview decoded at 1280 × 1200. Web preview inspected visually for map, labels, legend, and credits.
- Data: 36 alpine-hut records, 13 wilderness-hut records, and one summit. Every point's OSM ID/type and coordinates reconciled to the supplied source response. Public tag fields checked against the stated allowlist.
- Elevation: 606 rows × 637 columns, all finite values, EPSG:32632, 75 × 75 m cells; minimum about 342.63 m, maximum about 3979.45 m. Relief image dimensions match the elevation grid.
- QGIS: generated through native PyQGIS, saved, reopened, and rendered with five valid layers. The existing saved project was copied to a different folder, then reopened and rendered there without rebuilding. Native QGIS preview visually inspected. All five file sources use relative paths and exist.
- QGIS attachment ZIP: CRC passed. Its SQLite style database contains empty style tables, not external data or credentials.
- Privacy review: inspected included code and data; removed OSM contributor account metadata and all tags outside `name`, `tourism`, `natural`, and `ele`. Removed local QGIS save-user fields and used the public account name in project author metadata. Targeted scan found no local account paths, private-key headers, or common AWS/GitHub token patterns in reviewed public text files. This is a targeted review, not a guarantee against every possible secret format.
- Sources: checked official OSM copyright, AWS Terrain Tiles listing, and upstream Tilezen attribution. Credits distinguish inherited provenance from independently tested behavior.

## Changes from the supplied archive

The archive contained no finished poster or QGIS project despite references to them in its README. Both were generated for this portfolio. The Python renderer now resolves the portfolio folder structure, reads UTF-8 explicitly, writes both map sizes, and includes the OSM copyright/license URLs on the poster. The original map styling and feature positions were retained.

The older `Build_Source.py` was excluded from the public runnable scripts: it requires raw terrain tiles, an unrelated QGIS template, and machine-specific paths that were not supplied. `Fetch_Source.py` was also excluded from the supported offline workflow; it has an initial-directory creation bug and retrieves changing live data. The original archive remains unchanged outside the publication package. The original query and processing method are recorded in `CREDITS.md`; this package reproduces the poster from the supplied processed terrain, not a fresh terrain download.

## Practical limits

The installed QGIS interface was not opened interactively; project loading and rendering were tested through native PyQGIS. Other operating systems and QGIS releases were not tested. Exact upstream terrain lineage and the original download date cannot be independently established from the archive. No additional open license for original code/artwork was selected. No GitHub repository was created or upload verified because browser access timed out.
