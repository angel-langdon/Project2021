import KPI from "@/components/dashboard/KPI";
import { getColumn, sum, mean } from "@/utils/dataUtils";
const KPIsTop = (props) => {
  const visits: Array<number> = getColumn(props.filteredData, "visits");
  const predictedVisits: Array<number> = getColumn(
    props.filteredData,
    "prediction"
  );
  const monthlyVisits: number = sum(visits);
  const monthlyPredictedVisits: number = sum(predictedVisits);
  const meanDayVisits: number = Math.round(mean(visits));
  const meanWeekVisits: number = Math.round(meanDayVisits * 7);
  const kpiClassName: string = "col";
  return (
    <div className="container">
      <div className="row">
        <KPI
          number={monthlyVisits}
          unit=""
          description="Monthly Visits"
          className={kpiClassName}
        />
        <KPI
          number={monthlyPredictedVisits}
          unit=""
          description="Monthly Predicted Visits"
          className={kpiClassName}
        />
        <KPI
          number={meanDayVisits}
          unit=""
          description="Mean Visits by day"
          className={kpiClassName}
        />
        <KPI
          number={meanWeekVisits}
          unit=""
          description="Mean Visits by week"
          className={kpiClassName}
        />
      </div>
    </div>
  );
};
export default KPIsTop;
