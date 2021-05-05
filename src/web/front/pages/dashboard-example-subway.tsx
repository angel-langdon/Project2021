import Dashboard from "@/components/Dashboard";
import data from "../public/data/subway.json";

const DashboardExampleSubway = () => {
  return <Dashboard store="Subway" data={data} />;
};
export default DashboardExampleSubway;
