import Plot from "react-plotly.js";
import { getColumn } from "@/utils/dataUtils";
import { defaultStyles } from "@/components/dashboard/LinePlotVisits";

let customStyles = Object.create(defaultStyles);
customStyles["yaxis"] = { title: "Estimated Income $", showgrid: false };
customStyles["title"] = "Estimated income per day";

const LinePlotIncome = (props) => {
  const visits = getColumn(props.filteredData, "income_visits");
  const dates = getColumn(props.filteredData, "date");
  return (
    <Plot
      data={[
        {
          x: dates,
          y: visits,
          type: "scatter",
          name: "Estimated Income",
          mode: "lines",
          marker: { color: "green" },
        },
      ]}
      config={{ responsive: true }}
      layout={customStyles}
      style={{ width: "100%", height: "100%" }}
    />
  );
};
export default LinePlotIncome;
