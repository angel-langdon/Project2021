import Plot from "react-plotly.js";
import { getColumn } from "@/utils/dataUtils";

const defaultStyles = {
  display: "flex",
  autosize: true,
  title: "Visits per day",
  xaxis: { title: "Date" },
  yaxis: { title: "Nº of Visits" },
  plot_bgcolor: "#8595a8",
  font: { color: "#FFF" },
  paper_bgcolor: "#FFF3",
};

const LinePlotVisits = (props) => {
  const visits = getColumn(props.filteredData, "visits");
  const dates = getColumn(props.filteredData, "date");
  const predictedVisits = getColumn(props.filteredData, "prediction");
  const marginLeft = "100 px";
  return (
    <div className="d-flex" style={{ gridArea: "5/3/9/6" }}>
      <div style={{ marginLeft }}></div>
      <Plot
        data={[
          {
            x: dates,
            y: visits,
            type: "scatter",
            name: "Real visits",
            mode: "lines",
            marker: { color: "black" },
          },
          {
            x: dates,
            y: predictedVisits,
            type: "scatter",
            name: "Predicted visits",
            mode: "lines",
            marker: { color: "red" },
          },
        ]}
        config={{ responsive: true }}
        layout={defaultStyles}
        style={{ width: "100%", height: "100%" }}
      />
    </div>
  );
};
export default LinePlotVisits;
