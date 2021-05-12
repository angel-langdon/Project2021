import { getColumn, mean } from "@/utils/dataUtils";
import { Fragment } from "react";

const IncomeKPI = (props) => {
  return (
    <div className="kpi-income-container" style={props.style}>
      <span style={{ display: "flex", color: "#FFF" }}>
        <h6 className="no-margin">Mean by</h6>
        <div style={{ width: 10 }}></div>
        <h5 style={{ fontWeight: 800 }} className="no-margin">
          {props.granule}{" "}
        </h5>
      </span>

      <h5 className="no-margin kpi-income-value"> {props.value}</h5>
    </div>
  );
};

const MeanIncome = (props) => {
  const meanDayIncome = mean(getColumn(props.filteredData, "income_visits"));
  const meanWeekIncome = meanDayIncome * 7;
  const meanMonthIncome = meanWeekIncome * 4;

  return (
    <Fragment>
      <h5
        className="dashboard-stats-label"
        style={{ gridArea: "1/3", textAlign: "center" }}
      >
        INCOME
      </h5>
      <div
        className="mean-income-container"
        style={{ gridArea: "2/3/5/3" }}
      ></div>
      <IncomeKPI
        style={{ gridArea: "2/3" }}
        granule="DAY"
        value={meanDayIncome.toLocaleString().slice(0, -1) + " $"}
      />
      <IncomeKPI
        style={{ gridArea: "3/3" }}
        granule="WEEK"
        value={meanWeekIncome.toLocaleString().slice(0, -1) + " $"}
      />
      <IncomeKPI
        style={{ gridArea: "4/3" }}
        granule="MONTH"
        value={meanMonthIncome.toLocaleString().slice(0, -1) + " $"}
      />
    </Fragment>
  );
};
export default MeanIncome;
