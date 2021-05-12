import { getColumn, sum, mean } from "@/utils/dataUtils";
import { rmse, rSquared, mae } from "@/utils/stats";
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
  const incomeWeekends = props.filteredData.filter(
    (store) => store.is_weekend == 1
  );
  const totalIncomeWeekends = sum(getColumn(incomeWeekends, "income_visits"));
  const totalIncome = sum(getColumn(props.filteredData, "income_visits"));
  const meanWorkers = mean(getColumn(props.filteredData, "workforce"));
  return (
    <Fragment>
      <ModelKPI
        style={{ gridArea: "2/5" }}
        label="Total estimated income"
        value={"$ " + totalIncome.toLocaleString()}
        infoText="The total income is estimated with the number of visits and the mean spending by person by brand"
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "3/5" }}
        label="Total weekend/s estimated income"
        value={
          "$ " +
          totalIncomeWeekends.toLocaleString(undefined, {
            maximumFractionDigits: 2,
          })
        }
        infoText="The total weekend income is estimated with the number of visits and the mean spending by person by brand"
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "4/5" }}
        label="Mean estimated workers by day"
        value={Math.round(meanWorkers)}
        infoText="The mean number of workers by day is estimated with the number of visits and with the brand requirements"
        example="Maybe the values for mean workers by day are constant, this is due to the fact that some stores have a minimum of workers"
      ></ModelKPI>
    </Fragment>
  );
};
export default DashboardModelStats;
