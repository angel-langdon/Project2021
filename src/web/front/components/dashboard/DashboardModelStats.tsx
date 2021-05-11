import { getColumn } from "@/utils/dataUtils";
import { mape, rSquared, mae } from "@/utils/stats";
import { Fragment, useState } from "react";
import CardStatsInfo from "../CardStatsInfo";

export const ModelKPI = (props) => {
  const [visibility, setVisibility] = useState<string>("none");
  return (
    <div style={props.style} className="kpi-model-container">
      <h4 className="kpi-model-value no-margin">{props.value}</h4>
      <div style={{ height: 5 }}></div>
      <div className="d-flex justify-content-between" style={{ width: "100%" }}>
        <h6 className="kpi-model-label no-margin">{props.label}</h6>
        {props.infoText == undefined ? null : (
          <Fragment>
            <img
              className="model-stat-info"
              src="/images/info.svg"
              style={{ maxWidth: 20 }}
              onClick={() => setVisibility("flex")}
            ></img>

            <CardStatsInfo
              visibility={visibility}
              setVisibility={setVisibility}
              indicator={props.label}
              textInfo={props.infoText}
              example={props.example}
            />
          </Fragment>
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
  const globalR2 = Math.abs(rSquared(predictedVisits, visits)).toFixed(2);
  const MAE = mae(storePredictedVisits, storeVisits).toFixed(2);
  const MAPE = mape(storePredictedVisits, storeVisits).toFixed(2);
  return (
    <Fragment>
      <h5 className="dashboard-stats-label " style={{ gridArea: "1/5/1/6" }}>
        MODEL METRICS
      </h5>
      <ModelKPI
        style={{ gridArea: "2/5" }}
        label="Global model R2"
        value={globalR2}
        infoText="asdasda"
        example="example"
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "3/5" }}
        label="Store specific MAE"
        value={MAE}
        infoText="The MAE is the mean absolute error, that is the mean absolute difference between the predicted value and the real one."
        example={
          "We have a MAE of " +
          MAE +
          " so this means, that for the date range selected the mean visits distance from the predicted and real value is " +
          MAE +
          " visits"
        }
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "4/5" }}
        label="Store specific MAPE"
        value={MAPE}
        infoText="The MAPE is the "
        example={
          "We have a MAE of " +
          MAE +
          " so this means, that for the date range selected the mean visits distance from the predicted and real value is " +
          MAE +
          " visits"
        }
      ></ModelKPI>
    </Fragment>
  );
};
export default DashboardModelStats;
