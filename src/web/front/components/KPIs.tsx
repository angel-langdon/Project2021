import KPI from "@/components/KPI";
import { getColumn, sum, mean } from "@/utils/dataUtils";
const KPIs = (props) => {
  const visits: Array<number> = getColumn(props.filteredData, "visits");
  const predictedVisits: Array<number> = getColumn(
    props.filteredData,
    "prediction"
  );
  const monthlyVisits = sum(visits);
  const monthlyPredictedVisits = sum(predictedVisits);
  const meanDayVisits = Math.round(mean(visits));
  const meanWeekVisits = Math.round(meanDayVisits * 7);
  return (
    <div className="container">
      <div className="row">
        <KPI number={monthlyVisits} unit="" description="Monthly Visits" />
        <KPI
          number={monthlyPredictedVisits}
          unit=""
          description="Monthly Predicted Visits"
        />
        <KPI number={meanDayVisits} unit="" description="Mean Visits by day" />
        <KPI
          number={meanWeekVisits}
          unit=""
          description="Mean Visits by week"
        />
      </div>
    </div>
  );
};

export default KPIs;
