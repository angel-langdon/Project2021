import { getColumn, mean } from "@/utils/dataUtils";
import { Fragment } from "react";

const MeanKPI = (props) => {
  return (
    <div className="mean-kpi" style={props.style}>
      <h6 className="mean-kpi-label">{props.label}</h6>
      <h3 className="mean-kpi-value">{props.value}</h3>
    </div>
  );
};
const MeanVisits = (props) => {
  const meanDailyVisits = Math.round(
    mean(getColumn(props.filteredData, "visits"))
  );
  const meanMonthVisits = Math.round(meanDailyVisits * 31);
  const meanWeekVisits = Math.round(meanDailyVisits * 7);
  const meanDailyEstimatedVisits = Math.round(
    mean(getColumn(props.filteredData, "prediction"))
  );
  const meanMonthEstimatedVisits = Math.round(meanDailyEstimatedVisits * 31);
  const meanWeekEstimatedVisits = Math.round(meanDailyEstimatedVisits * 7);

  return (
    <Fragment>
      <h5
        className="dashboard-stats-label"
        style={{ gridArea: "1/1", textAlign: "center" }}
      >
        MEAN VISITS
      </h5>
      <h5
        className="dashboard-stats-label"
        style={{ gridArea: "1/2", textAlign: "center" }}
      >
        MEAN PREDICTED VISITS
      </h5>
      <MeanKPI
        label="Day"
        value={meanDailyVisits}
        style={{ gridArea: "2/1" }}
      />
      <MeanKPI
        label="Week"
        value={meanWeekVisits}
        style={{ gridArea: "3/1" }}
      />
      <MeanKPI
        label="Month"
        value={meanMonthVisits}
        style={{ gridArea: "4/1" }}
      />
      <MeanKPI
        label="Day"
        value={meanDailyEstimatedVisits}
        style={{ gridArea: "2/2" }}
      />
      <MeanKPI
        label="Week"
        value={meanWeekEstimatedVisits}
        style={{ gridArea: "3/2" }}
      />
      <MeanKPI
        label="Month"
        value={meanMonthEstimatedVisits}
        style={{ gridArea: "4/2" }}
      />
      )
    </Fragment>
  );
};
export default MeanVisits;
