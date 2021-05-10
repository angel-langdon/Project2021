import { Fragment } from "react";

export const ModelKPI = (props) => {
  return (
    <div style={props.style} className="kpi-model-container">
      <h4 className="kpi-model-value no-margin">{props.value}</h4>
      <div style={{ height: 5 }}></div>
      <h6 className="kpi-model-label no-margin">{props.label}</h6>
    </div>
  );
};

const DashboardModelStats = (props) => {
  return (
    <Fragment>
      <h5 className="dashboard-stats-label " style={{ gridArea: "1/5/1/6" }}>
        MODEL METRICS
      </h5>
      <ModelKPI style={{ gridArea: "3/5" }} label="RMSE" value="10"></ModelKPI>
      <ModelKPI style={{ gridArea: "4/5" }} label="MAE" value="10"></ModelKPI>
      <ModelKPI style={{ gridArea: "2/5" }} label="R2" value="10"></ModelKPI>
    </Fragment>
  );
};
export default DashboardModelStats;
