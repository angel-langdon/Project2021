import dynamic from "next/dynamic";
import KPIs from "@/components/KPIs";
const LinePlotVisits = dynamic(() => import("@/components/LinePlotVisits"), {
  ssr: false,
});

interface IProps {
  store: string;
  data: object;
}

const Dashboard = (props: IProps) => {
  return (
    <div className="dashboard-container">
      <KPIs {...props} />
      <LinePlotVisits {...props} />
    </div>
  );
};

export default Dashboard;
