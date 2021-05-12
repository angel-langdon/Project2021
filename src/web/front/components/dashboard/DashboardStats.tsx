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
const LinePlotIncome = dynamic(
  () => import("@/components/dashboard/LinePlotIncome"),
  { ssr: false }
);

const DashboardStats = (props) => {
  return (
    <div className="dashboard-stats-container">
      <MeanVisits {...props} />
      <MeanIncome {...props} />
      <DashboardModelStats {...props} />
      <DashboardAggregatedData {...props} />
      <div className="d-flex" style={{ gridArea: "5/1/8/6" }}>
        <DatePicker {...props} />
        <div style={{ width: 10 }}></div>
        <LinePlotVisits {...props} />
      </div>
      <div className="d-flex" style={{ gridArea: "8/1/12/6" }}>
        <LinePlotIncome {...props} />
      </div>
    </div>
  );
};

export default DashboardStats;
