import dynamic from "next/dynamic";
const LinePlot = dynamic(() => import("@/components/LinePlot"), {
  ssr: false,
});

function Dashboard() {
  return (
    <div className="dashboard-container">
      <LinePlot />
    </div>
  );
}

export default Dashboard;
