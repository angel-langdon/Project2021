export default function MapSearcher(props) {
  return (
    <div
      className="map-parent"
      onClick={() => props.setMapVisibility("none")}
      style={{ display: props.mapVisibility }}
    >
      <div className="map-searcher-container"></div>
    </div>
  );
}
