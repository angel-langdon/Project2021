import { ModelKPI } from "@/components/dashboard/DashboardModelStats";
import { Fragment } from "react";

const DashboardAggregatedData = (props) => {
  return (
    <Fragment>
      <h5 className="dashboard-stats-label" style={{ gridArea: "1 / 4" }}>
        AGGREGATED DATA
      </h5>

      <ModelKPI
        style={{ gridArea: "2/4" }}
        label="Maximum day visits"
        value="10"
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "3/4" }}
        label="Total weekend visits"
        value="10"
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "4/4" }}
        label="Total visits"
        value="10"
      ></ModelKPI>
    </Fragment>
  );
};
export default DashboardAggregatedData;
