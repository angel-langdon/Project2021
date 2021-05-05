import Plot from "react-plotly.js";

const defaultStyles = {
  display: "flex",
  title: "A Fancy Plot",
  plot_bgcolor: "black",
  font: { color: "#FFF" },
  paper_bgcolor: "#FFF3",
};

const LinePlotVisits = (props) => {
  return (
    <Plot
      data={[
        {
          x: [1, 2, 3],
          y: [2, 6, 3],
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
