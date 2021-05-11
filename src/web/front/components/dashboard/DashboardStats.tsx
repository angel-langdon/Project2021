import DashboardAggregatedData from "./DashboardAggregatedData";
import DashboardModelStats from "./DashboardModelStats";
import MeanIncome from "./MeanIncome";
import MeanVisits from "./MeanVisits";
import DatePicker from "@/components/DatePicker";
import dynamic from "next/dynamic";
const LinePlotVisits = dynamic(
  () => import("@/components/dashboard/LinePlotVisits"),
  { ssr: false }
);

const DashboardStats = (props) => {
  return (
    <div className="dashboard-stats-container">
      <MeanVisits {...props} />
      <MeanIncome {...props} />
      <DashboardModelStats {...props} />
      <DashboardAggregatedData {...props} />
      <DatePicker {...props} />
      <LinePlotVisits {...props} />
    </div>
  );
};

export default DashboardStats;
