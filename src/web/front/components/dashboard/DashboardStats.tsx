import DashboardYesterdayTodayVisits from "./DashboardYesterdayTodayVisits";
import MeanIncome from "./MeanIncome";
import MeanVisits from "./MeanVisits";

const DashboardStats = (props) => {
  return (
    <div className="dashboard-stats-container">
      <MeanVisits {...props} />
      <MeanIncome {...props} />
      <DashboardYesterdayTodayVisits {...props} />
    </div>
  );
};

export default DashboardStats;
