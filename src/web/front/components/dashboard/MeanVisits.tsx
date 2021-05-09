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

  return (
    <div className="d-flex mean-visits-container justify-content-start">
      <div className="d-flex flex-column">
        <h5>MEAN VISITS</h5>
        <MeanKPI label="Day" value={meanDailyVisits} />
        <MeanKPI label="Week" value={meanWeekVisits} />
        <MeanKPI label="Month" value={meanMonthVisits} />
      </div>
    </div>
  );
};
export default MeanVisits;
