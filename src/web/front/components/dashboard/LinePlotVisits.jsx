import Plot from "react-plotly.js";
import { getColumn } from "@/utils/dataUtils";

const defaultStyles = {
  display: "flex",
  autosize: true,
  title: "Visits per day",
  xaxis: { title: "Date" },
  yaxis: { title: "Nº of Visits" },
  plot_bgcolor: "rgb(0,0,0,0)",
  legend: {
    x: 0,
    y: 1.2,
    orientation: "h",
    font: {
      color: "#000",
    },
    bgcolor: "#fff",
  },
  font: { color: "#000" },
  paper_bgcolor: "rgb(0,0,0,0)",
};

const LinePlotVisits = (props) => {
  const visits = getColumn(props.filteredData, "visits");
  const dates = getColumn(props.filteredData, "date");
  const predictedVisits = getColumn(props.filteredData, "prediction");
  return (
    <Plot
      data={[
        {
          x: dates,
          y: visits,
          type: "scatter",
          name: "Real visits",
          mode: "lines",
          marker: { color: props.colors[0] },
        },
        {
          x: dates,
          y: predictedVisits,
          type: "scatter",
          name: "Predicted visits",
          mode: "lines",
          marker: { color: props.colors[1] },
        },
      ]}
      config={{ responsive: true }}
      layout={defaultStyles}
      style={{ width: "100%", height: "100%" }}
    />
  );
};
export default LinePlotVisits;
