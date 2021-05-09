import { Fragment } from "react";

const VisitsKPI = (props) => {
  return (
    <div style={props.style} className="kpi-visits-container">
      <h5 className="kpi-visits-value no-margin">{props.value}</h5>
      <h5 className="kpi-visits-label no-margin">{props.label}</h5>
    </div>
  );
};

const DashboardYesterdayTodayVisits = (props) => {
  return (
    <Fragment>
      <h5 className="dashboard-stats-label" style={{ gridArea: "1/4" }}>
        REAL VISITS
      </h5>
      <h5 className="dashboard-stats-label" style={{ gridArea: "1/5" }}>
        PREDICTED VISITS
      </h5>
      <VisitsKPI
        style={{ gridArea: "2/4/span 2 /5" }}
        label="Yesterday"
        value="10"
      ></VisitsKPI>
    </Fragment>
  );
};
export default DashboardYesterdayTodayVisits;
