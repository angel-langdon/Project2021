import Plot from "react-plotly.js";

const LinePlot = () => {
  return (
    <Plot
      data={[
        {
          x: [1, 2, 3],
          y: [2, 6, 3],
          type: "scatter",
          mode: "lines",
          marker: { color: "red" },
        }
      ]}
      layout={{ width: 320, height: 240, title: "A Fancy Plot" }}
    />
  );
};
export default LinePlot;
