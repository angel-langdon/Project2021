import DashboardAggregatedData from "./DashboardAggregatedData";
import DashboardModelStats from "./DashboardModelStats";
import MeanIncome from "./MeanIncome";
import MeanVisits from "./MeanVisits";
import DatePicker from "@/components/DatePicker";

const DashboardStats = (props) => {
  return (
    <div className="dashboard-stats-container">
      <MeanVisits {...props} />
      <MeanIncome {...props} />
      <DashboardModelStats {...props} />
      <DashboardAggregatedData {...props} />
      <DatePicker {...props} />
    </div>
  );
};

export default DashboardStats;
