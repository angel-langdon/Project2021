import { getColumn } from "@/utils/dataUtils";
import { rmse, rSquared, mae } from "@/utils/stats";
import { Fragment } from "react";

export const ModelKPI = (props) => {
  return (
    <div style={props.style} className="kpi-model-container">
      <h4 className="kpi-model-value no-margin">{props.value}</h4>
      <div style={{ height: 5 }}></div>
      <div className="d-flex justify-content-between" style={{ width: "100%" }}>
        <h6 className="kpi-model-label no-margin">{props.label}</h6>
        {props.infoText == undefined ? null : (
          <img
            className="model-stat-info"
            src="/images/info.svg"
            style={{ maxWidth: 20 }}
          ></img>
        )}
      </div>
    </div>
  );
};

const DashboardModelStats = (props) => {
  const visits = getColumn(props.data, "visits");
  const predictedVisits = getColumn(props.data, "prediction");
  const storeVisits = getColumn(props.filteredData, "visits");
  const storePredictedVisits = getColumn(props.filteredData, "prediction");
  return (
    <Fragment>
      <h5 className="dashboard-stats-label " style={{ gridArea: "1/5/1/6" }}>
        MODEL METRICS
      </h5>
      <ModelKPI
        style={{ gridArea: "2/5" }}
        label="Global model R2"
        value={Math.abs(rSquared(predictedVisits, visits)).toFixed(2)}
        infoText="asdasda"
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "3/5" }}
        label="Store specific RMSE"
        value={rmse(storePredictedVisits, storeVisits).toFixed(2)}
        infoText="asdasda"
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "4/5" }}
        label="Store specific MAE"
        value={mae(storePredictedVisits, storeVisits).toFixed(2)}
        infoText="asdasda"
      ></ModelKPI>
    </Fragment>
  );
};
export default DashboardModelStats;
