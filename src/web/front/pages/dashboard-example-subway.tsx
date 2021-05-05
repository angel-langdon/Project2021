import Dashboard from "@/components/Dashboard";
import data from "../public/data/subway.json";
import { preprocessPatternsData } from "@/utils/dataUtils.js";

const DashboardExampleSubway = () => {
  const processedData = preprocessPatternsData(data);
  return <Dashboard store="Subway" data={processedData} />;
};
export default DashboardExampleSubway;
