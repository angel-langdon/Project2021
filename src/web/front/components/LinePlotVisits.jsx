import Plot from "react-plotly.js";

const defaultStyles = {
  display: "flex",
  autosize: true,
  title: "Visits per day",
  xaxis: { title: "Date" },
  yaxis: { title: "Nº of Visits" },

  plot_bgcolor: "black",
  font: { color: "#FFF" },
  paper_bgcolor: "#FFF3",
};

function getColumn(arr, column) {
  return arr.map((object) => object[column]);
}

const LinePlotVisits = (props) => {
  const filteredData = props.data.filter(
    (object) => object.placekey == props.placekey
  );
  const visits = getColumn(filteredData, "visits");
  const dates = getColumn(filteredData, "date");
  console.log(dates);
  return (
    <Plot
      data={[
        {
          x: dates,
          y: visits,
          type: "scatter",
          mode: "lines",
          marker: { color: "red" },
        },
      ]}
      layout={defaultStyles}
    />
  );
};
export default LinePlotVisits;
