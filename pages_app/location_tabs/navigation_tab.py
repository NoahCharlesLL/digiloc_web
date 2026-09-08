import streamlit as st
import json
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval
from utils.data import save_drawings

PRESET_COLORS = [
    "#980000", "#FF0000", "#FF9900", "#FFFF00", "#00FF00", "#FFFFFF",
    "#FF00FF", "#9900FF", "#0000FF", "#4A86E8", "#00FFFF", "#000000",
    "#d9a441", "#8d9f44", "#4b905b", "#0e7a6d", "#14616d", "#2f4858"
]

MARKER_TYPES = [
    ("toilet", "🚻"), ("wifi", "📶"), ("power", "🔌"),
    ("parking", "🅿️"), ("food", "🍴"), ("custom", "📍"),
]

MAP_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css"/>
<style>
  html, body { margin:0; padding:0; height:100%; background:#1A1A1A; font-family:'Segoe UI',sans-serif; }
  #map { position:absolute; top:0; left:0; right:280px; bottom:0; }
  #panel {
    position:absolute; top:0; right:0; width:280px; height:100%;
    background:#232323; color:#F2F2F2; box-sizing:border-box; padding:14px;
    overflow-y:auto; border-left:2px solid #5A5A5A; display:none;
  }
  #panel * { box-sizing:border-box; }
  #panel input[type=text] {
    width:100%; background:#1A1A1A; color:#F2F2F2; border:2px solid #5A5A5A;
    padding:6px; margin-bottom:10px; font-size:13px;
  }
  .swatch-grid { display:grid; grid-template-columns:repeat(6,1fr); gap:4px; margin-bottom:10px; }
  .swatch { width:100%; height:24px; border:2px solid #5A5A5A; cursor:pointer; }
  .swatch.selected { border-color:#D9A441; }
  .marker-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin-bottom:10px; }
  .marker-btn {
    background:#1A1A1A; border:2px solid #5A5A5A; color:#F2F2F2;
    padding:8px 0; cursor:pointer; text-align:center; font-size:18px;
  }
  .marker-btn.selected { border-color:#D9A441; background:#2a2416; }
  .action-btn {
    width:100%; border:2px solid #5A5A5A; background:#1A1A1A; color:#F2F2F2;
    padding:8px; margin-top:6px; cursor:pointer; font-size:13px;
  }
  .action-btn.primary { background:#D9A441; color:#1A1A1A; border-color:#D9A441; font-weight:700; }
  label { font-size:11px; text-transform:uppercase; letter-spacing:1px; color:#8C8C8C; }
</style>
</head>
<body>
<div id="map"></div>
<button class="action-btn primary" id="editModeBtn" style="position:absolute; bottom:10px; right:14px; width:252px; z-index:1000;">✏️ Edit</button>
<div id="panel">
  <label>Label</label>
  <input type="text" id="labelInput" value="New area"/>

  <div id="markerSection" style="display:none;">
    <label>Marker Type</label>
    <div class="marker-grid" id="markerGrid"></div>
  </div>

  <div id="colorSection">
    <label>Color</label>
    <div class="swatch-grid" id="swatchGrid"></div>
    <input type="text" id="hexInput" value="#D9A441"/>
  </div>

  <button class="action-btn" id="cancelBtn">Cancel</button>
  <button class="action-btn primary" id="confirmBtn">Confirm</button>
</div>
<button class="action-btn primary" id="exportBtn" style="position:absolute; bottom:56px; right:14px; width:252px; z-index:1000; display:none;">💾 Save</button>
<button class="action-btn" id="cancelAllBtn" style="position:absolute; bottom:10px; right:14px; width:252px; z-index:1000; display:none;">✖ Cancel Edit</button>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js"></script>
<script>
var LAT = __LAT__, LNG = __LNG__;
var PRESETS = __PRESETS__;
var MARKER_TYPES = __MARKER_TYPES__;
var savedShapes = __SAVED_SHAPES__;
var LOC_ID = "__LOC_ID__";

var map = L.map('map').setView([LAT, LNG], 16);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:20}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

function iconFor(type, color) {
if (type === 'custom') {
  return L.divIcon({
    html: '<div style="width:20px;height:20px;border-radius:50%;background:'+color+';border:2px solid #fff;box-shadow:0 0 2px #000;"></div>',
    className: '', iconSize:[24,24], iconAnchor:[12,12]
  });
}
  var emoji = {toilet:"🚻", wifi:"📶", power:"🔌", parking:"🅿️", food:"🍴", custom:"📍"}[type] || "📍";
  return L.divIcon({
    html: '<div style="font-size:22px; filter:drop-shadow(0 0 2px #000);">'+emoji+'</div>',
    className: '', iconSize:[24,24], iconAnchor:[12,12]
  });
}

savedShapes.forEach(function(s) {
  var layer;
  if (s.kind === "marker") {
    layer = L.marker(s.center, {icon: iconFor(s.markerType, s.color)});
  } else if (s.kind === "circle") {
    layer = L.circle(s.center, {radius: s.radius, color: s.color, fillColor: s.color, fillOpacity:0.3});
  } else if (s.kind === "polygon") {
    layer = L.polygon(s.points, {color: s.color, fillColor: s.color, fillOpacity:0.3});
  } else if (s.kind === "line") {
    layer = L.polyline(s.points, {color: s.color});
  }
  if (layer) {
    layer.shapeData = s;
    if (s.label) layer.bindTooltip(s.label, {permanent:true});
    drawnItems.addLayer(layer);
  }
});
map.whenReady(function() {
  setTimeout(updateLabelVisibility, 0);
});

var drawControl = new L.Control.Draw({
  edit: { featureGroup: drawnItems },
  draw: { circlemarker: false }
});
var editing = false;
var originalShapesJSON = JSON.stringify(savedShapes);
var ZOOM_LABEL_THRESHOLD = 15;

function updateLabelVisibility() {
  var show = map.getZoom() >= ZOOM_LABEL_THRESHOLD;
  drawnItems.eachLayer(function(l) {
    var tooltip = l.getTooltip();
    if (!tooltip) return;
    if (show) {
      if (!map.hasLayer(tooltip)) l.openTooltip();
    } else {
      l.closeTooltip();
    }
  });
}

map.on('zoomend', updateLabelVisibility);

function rebuildFromJSON(json) {
  drawnItems.clearLayers();
  JSON.parse(json).forEach(function(s) {
    var layer;
    if (s.kind === "marker") layer = L.marker(s.center, {icon: iconFor(s.markerType, s.color)});
    else if (s.kind === "circle") layer = L.circle(s.center, {radius: s.radius, color: s.color, fillColor: s.color, fillOpacity:0.3});
    else if (s.kind === "polygon") layer = L.polygon(s.points, {color: s.color, fillColor: s.color, fillOpacity:0.3});
    else if (s.kind === "line") layer = L.polyline(s.points, {color: s.color});
    if (layer) {
      layer.shapeData = s;
      if (s.label) layer.bindTooltip(s.label, {permanent:true});
      drawnItems.addLayer(layer);
    }
  });
}

document.getElementById('editModeBtn').onclick = function() {
  editing = true;
  map.addControl(drawControl);
  document.getElementById('editModeBtn').style.display = 'none';
  document.getElementById('exportBtn').style.display = 'block';
  document.getElementById('cancelAllBtn').style.display = 'block';
};

document.getElementById('cancelAllBtn').onclick = function() {
  rebuildFromJSON(originalShapesJSON);
  editing = false;
  map.removeControl(drawControl);
  document.getElementById('editModeBtn').style.display = 'block';
  document.getElementById('exportBtn').style.display = 'none';
  document.getElementById('cancelAllBtn').style.display = 'none';
  panel.style.display = 'none';
  currentLayer = null;
};

var panel = document.getElementById('panel');
var labelInput = document.getElementById('labelInput');
var hexInput = document.getElementById('hexInput');
var swatchGrid = document.getElementById('swatchGrid');
var markerGrid = document.getElementById('markerGrid');
var markerSection = document.getElementById('markerSection');
var colorSection = document.getElementById('colorSection');

var currentLayer = null;
var currentColor = "#D9A441";
var currentMarkerType = "custom";
var isMarker = false;

PRESETS.forEach(function(hex) {
  var sw = document.createElement('div');
  sw.className = 'swatch';
  sw.style.background = hex;
  sw.dataset.hex = hex;
  sw.onclick = function() {
    currentColor = hex;
    hexInput.value = hex;
    highlightSwatch(hex);
    applyLiveStyle();
  };
  swatchGrid.appendChild(sw);
});

function highlightSwatch(hex) {
  document.querySelectorAll('.swatch').forEach(function(el) {
    el.classList.toggle('selected', el.dataset.hex === hex);
  });
}

MARKER_TYPES.forEach(function(pair) {
  var type = pair[0], emoji = pair[1];
  var btn = document.createElement('div');
  btn.className = 'marker-btn';
  btn.textContent = emoji;
  btn.dataset.type = type;
  btn.onclick = function() {
    currentMarkerType = type;
    document.querySelectorAll('.marker-btn').forEach(function(b){ b.classList.remove('selected'); });
    btn.classList.add('selected');
    colorSection.style.display = (type === 'custom') ? 'block' : 'none';
    applyLiveStyle();
  };
  markerGrid.appendChild(btn);
});

hexInput.addEventListener('input', function() {
  currentColor = hexInput.value;
  highlightSwatch(currentColor);
  applyLiveStyle();
});

function applyLiveStyle() {
  if (!currentLayer) return;
  if (isMarker) {
    currentLayer.setIcon(iconFor(currentMarkerType, currentColor));
  } else if (currentLayer.setStyle) {
    currentLayer.setStyle({color: currentColor, fillColor: currentColor});
  }
}

map.on(L.Draw.Event.CREATED, function(e) {
  var layer = e.layer;
  drawnItems.addLayer(layer);
  openPanel(layer, e.layerType, true);
});

drawnItems.on('click', function(e) {
  var layerType = 'polygon';
  if (e.layer instanceof L.Marker) layerType = 'marker';
  else if (e.layer instanceof L.Circle) layerType = 'circle';
  else if (e.layer instanceof L.Polyline) layerType = 'line';
  openPanel(e.layer, layerType, false);
});

function openPanel(layer, layerType, isNew) {
  currentLayer = layer;
  isMarker = (layerType === 'marker');
  panel.style.display = 'block';
  markerSection.style.display = isMarker ? 'block' : 'none';
  colorSection.style.display = isMarker ? 'none' : 'block';

  var existing = layer.shapeData;
  labelInput.value = existing ? existing.label : (isMarker ? "New marker" : "New area");
  currentColor = existing ? existing.color : "#D9A441";
  currentMarkerType = existing ? (existing.markerType || "custom") : "custom";
  hexInput.value = currentColor;
  highlightSwatch(currentColor);

  document.querySelectorAll('.marker-btn').forEach(function(b) {
    b.classList.toggle('selected', b.dataset.type === currentMarkerType);
  });
  if (isMarker && currentMarkerType === 'custom') colorSection.style.display = 'block';

  layer._isNewShape = isNew;
}

document.getElementById('cancelBtn').onclick = function() {
  if (currentLayer) {
    if (currentLayer._isNewShape) drawnItems.removeLayer(currentLayer);
    panel.style.display = 'none';
    currentLayer = null;
  }
};

document.getElementById('confirmBtn').onclick = function() {
  if (!currentLayer) return;
  var kind = isMarker ? 'marker' : (currentLayer instanceof L.Circle ? 'circle' :
             (currentLayer instanceof L.Polygon ? 'polygon' : 'line'));

  var data = { kind: kind, label: labelInput.value, color: currentColor };

  if (kind === 'marker') {
    data.center = [currentLayer.getLatLng().lat, currentLayer.getLatLng().lng];
    data.markerType = currentMarkerType;
    currentLayer.setIcon(iconFor(currentMarkerType, currentColor));
  } else if (kind === 'circle') {
    data.center = [currentLayer.getLatLng().lat, currentLayer.getLatLng().lng];
    data.radius = currentLayer.getRadius();
    currentLayer.setStyle({color: currentColor, fillColor: currentColor});
  } else {
    data.points = currentLayer.getLatLngs()[0] ? currentLayer.getLatLngs()[0].map(function(p){return [p.lat,p.lng];})
                  : currentLayer.getLatLngs().map(function(p){return [p.lat,p.lng];});
    currentLayer.setStyle({color: currentColor, fillColor: currentColor});
  }

  currentLayer.shapeData = data;
  currentLayer.bindTooltip(data.label, {permanent:true});

  panel.style.display = 'none';
  currentLayer = null;
};

document.getElementById('exportBtn').onclick = function() {
  if (currentLayer) {
  document.getElementById('confirmBtn').click();
  }
  var shapes = [];
  drawnItems.eachLayer(function(l) {
    if (l.shapeData) shapes.push(l.shapeData);
  });
  localStorage.setItem('nav_shapes_' + LOC_ID, JSON.stringify(shapes));
  window.parent.location.reload();
};
</script>
</body>
</html>
"""


def render(loc, area_drawings):
    st.markdown("**Draw areas/markers on the map. Configure name/color, click Confirm, then click Save.**")

    saved = area_drawings.get(loc["id"], [])
    loc_id = str(loc["id"])

    html = MAP_HTML_TEMPLATE
    html = html.replace("__LAT__", str(loc["lat"]))
    html = html.replace("__LNG__", str(loc["lng"]))
    html = html.replace("__PRESETS__", json.dumps(PRESET_COLORS))
    html = html.replace("__MARKER_TYPES__", json.dumps(MARKER_TYPES))
    html = html.replace("__SAVED_SHAPES__", json.dumps(saved))
    html = html.replace("__LOC_ID__", loc_id)

    components.html(html, height=650, scrolling=False)

    stored = streamlit_js_eval(
        js_expressions=f"localStorage.getItem('nav_shapes_{loc_id}')",
        key=f"read_shapes_{loc_id}"
    )
    if stored:
        try:
            shapes = json.loads(stored)
            if shapes != saved:
                area_drawings[loc["id"]] = shapes
                save_drawings(area_drawings)
                streamlit_js_eval(
                    js_expressions=f"localStorage.removeItem('nav_shapes_{loc_id}')",
                    key=f"clear_shapes_{loc_id}"
                )
                st.success(f"Saved {len(shapes)} shape(s)!")
                st.rerun()
        except Exception as e:
            st.error(f"Couldn't parse JSON: {e}")