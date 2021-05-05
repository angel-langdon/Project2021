import dynamic from "next/dynamic";
import KPIs from "@/components/KPIs";
const LinePlotVisits = dynamic(() => import("@/components/LinePlotVisits"), {
  ssr: false,
});
const data = 1;

function Dashboard() {
  return (
    <div className="dashboard-container">
      <KPIs data={data} />
      <LinePlotVisits data={data} />
    </div>
  );
}

export default Dashboard;
