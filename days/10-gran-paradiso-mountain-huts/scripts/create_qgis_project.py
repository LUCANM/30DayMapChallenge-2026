"""Create and reopen a portable project. Run with QGIS's Python interpreter."""
from pathlib import Path
import os
import xml.etree.ElementTree as ET

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from qgis.core import (
    QgsApplication, QgsProject, QgsCoordinateReferenceSystem, QgsVectorLayer,
    QgsRasterLayer, QgsMarkerSymbol, QgsSingleSymbolRenderer, QgsRectangle,
    Qgis, QgsMapSettings, QgsMapRendererParallelJob, QgsReferencedRectangle,
)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import QSize


def main():
    root = Path(__file__).resolve().parents[1]
    app = QgsApplication([], False)
    app.initQgis()
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem('EPSG:32632'))
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    project.setTitle('Gran Paradiso — Mountain Huts | Day 10, 2026')
    layers = []
    for filename, title, color, shape, count in [
        ('peak.geojson', 'Gran Paradiso summit', '#f5eee1', 'triangle', 1),
        ('alpine_hut.geojson', 'Alpine huts (36)', '#f5bb72', 'circle', 36),
        ('wilderness_hut.geojson', 'Wilderness huts (13)', '#8ce1e2', 'diamond', 13),
    ]:
        layer = QgsVectorLayer(str(root/'data'/filename), title, 'ogr')
        if not layer.isValid() or layer.featureCount() != count:
            raise RuntimeError('Invalid layer or unexpected count: ' + filename)
        symbol = QgsMarkerSymbol.createSimple({
            'name': shape, 'color': color, 'size': '2.5',
            'outline_color': '#101b30', 'outline_width': '0.25',
        })
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))
        project.addMapLayer(layer, False)
        project.layerTreeRoot().addLayer(layer)
        layers.append(layer)
    relief = QgsRasterLayer(str(root/'data/relief.png'), 'Terrain relief', 'gdal')
    elevation = QgsRasterLayer(str(root/'data/elevation.tif'), 'Elevation (metres)', 'gdal')
    for layer in (relief, elevation):
        if not layer.isValid():
            raise RuntimeError('Invalid raster: ' + layer.name())
        project.addMapLayer(layer, False)
        project.layerTreeRoot().addLayer(layer)
    project.layerTreeRoot().findLayer(elevation.id()).setItemVisibilityChecked(False)
    layers.append(relief)
    extent = QgsRectangle(elevation.extent())
    project.viewSettings().setDefaultViewExtent(
        QgsReferencedRectangle(extent, project.crs())
    )
    project.setBackgroundColor(QColor('#101b30'))
    target = root/'qgis/Gran_Paradiso_Day10.qgs'
    target.parent.mkdir(exist_ok=True)
    if not project.write(str(target)):
        raise RuntimeError('Could not write project: ' + project.error())
    # QGIS adds the local operating-system user to saved projects.
    xml = ET.parse(target)
    for key in ('saveUser', 'saveUserFull'):
        xml.getroot().attrib.pop(key, None)
    author = xml.find('projectMetadata/author')
    if author is not None:
        author.text = 'LUCANM'
    xml.write(target, encoding='utf-8', xml_declaration=True)
    project.clear()
    if not project.read(str(target)):
        raise RuntimeError('Could not reopen project')
    if len(project.mapLayers()) != 5 or not all(l.isValid() for l in project.mapLayers().values()):
        raise RuntimeError('Reopened project has invalid layers')
    settings = QgsMapSettings()
    settings.setLayers(project.layerTreeRoot().checkedLayers())
    settings.setDestinationCrs(project.crs())
    settings.setExtent(extent)
    settings.setOutputSize(QSize(1400, 1100))
    settings.setBackgroundColor(QColor('#101b30'))
    job = QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()
    if job.errors():
        raise RuntimeError(str(job.errors()))
    if not job.renderedImage().save(str(root/'maps/qgis-preview.png')):
        raise RuntimeError('Could not save native QGIS preview')
    print('PASS: project written, reopened, 5 valid layers, native QGIS render')
    # QGIS providers are owned by the application until process shutdown.


if __name__ == '__main__':
    main()
