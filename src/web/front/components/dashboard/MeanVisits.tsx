import { getColumn, mean } from "@/utils/dataUtils";

const MeanKPI = (props) => {
  return (
    <div className="d-flex flex-column mean-kpi justify-content-center">
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
    <div className="d-flex mean-visits-container justify-content-start">
      <div className="d-flex flex-column">
        <div className="d-flex visits-mean-row justify-content-between">
          <h5 className="visits-mean-label">MEAN VISITS</h5>
          <h5 className="visits-mean-label">MEAN ESTIMATED VISITS</h5>
        </div>
        <div className="d-flex visits-mean-row-justify-content-between">
          <div className="d-flex flex-column visits-mean-column">
            <MeanKPI label="Day" value={meanDailyVisits} />
            <MeanKPI label="Week" value={meanWeekVisits} />
            <MeanKPI label="Month" value={meanMonthVisits} />
          </div>
          <div className="d-flex flex-column visits-mean-column">
            <MeanKPI label="Day" value={meanDailyEstimatedVisits} />
            <MeanKPI label="Week" value={meanWeekEstimatedVisits} />
            <MeanKPI label="Month" value={meanMonthEstimatedVisits} />
          </div>
        </div>
      </div>
    </div>
  );
};
export default MeanVisits;
