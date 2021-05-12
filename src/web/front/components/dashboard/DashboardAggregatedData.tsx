import { ModelKPI } from "@/components/dashboard/DashboardModelStats";
import { getColumn, sum } from "@/utils/dataUtils";
import { Fragment } from "react";

const DashboardAggregatedData = (props) => {
  const storesWithout0s = props.filteredData.filter(
    (store) => store.visits > 0
  );
  const visitsWithout0s = getColumn(storesWithout0s, "visits");
  const maxVisits = Math.max(...visitsWithout0s);
  const minVisits = Math.min(...visitsWithout0s);
  const weekendDaysStores = props.filteredData.filter(
    (store) => store.is_weekend == 1
  );
  const weekendVisits = sum(getColumn(weekendDaysStores, "visits"));
  const totalVisits = sum(visitsWithout0s);

  return (
    <Fragment>
      <h5
        className="dashboard-stats-label"
        style={{ gridArea: "1/ 4/1/6", textAlign: "center" }}
      >
        AGGREGATED DATA
      </h5>
      <div style={{ gridArea: "2/4" }} className="min-max-visits d-flex">
        <ModelKPI label="Maximum day visits" value={maxVisits}></ModelKPI>
        <div style={{ width: 10 }}></div>
        <ModelKPI label="Minimum day visits" value={minVisits}></ModelKPI>
      </div>
      <ModelKPI
        style={{ gridArea: "3/4" }}
        label="Total weekend visits"
        value={weekendVisits}
      ></ModelKPI>
      <ModelKPI
        style={{ gridArea: "4/4" }}
        label="Total visits"
        value={totalVisits}
      ></ModelKPI>
    </Fragment>
  );
};
export default DashboardAggregatedData;
