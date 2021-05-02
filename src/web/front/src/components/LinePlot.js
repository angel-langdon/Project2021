import Plot from 'react-plotly.js'

function LinePlot() {
    const plot = <Plot
        data={[
          {
            x: [1, 2, 3],
            y: [2, 6, 3],
            type: 'scatter',
            mode: 'lines',
            marker: {color: 'red'},
          }
        ]}
        layout={{width: 400, height: 640,
             title: 'Line plot'} }
      />

    return plot}
export default LinePlot

