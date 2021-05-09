import Dashboard from "@/components/dashboard/Dashboard";
import data from "../public/data/subway.json";
import { preprocessPatternsData } from "@/utils/dataUtils.js";

const DashboardExampleSubway = () => {
  const processedData = preprocessPatternsData(data);
  return (
    <Dashboard
      store="Subway"
      data={processedData}
      brandImage="/images/subway_logo.png"
    />
  );
};
export default DashboardExampleSubway;
