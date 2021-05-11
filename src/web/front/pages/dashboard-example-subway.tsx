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
      colors={["rgb(8, 82, 0)", "rgb(189, 183, 0)"]}
    />
  );
};
export default DashboardExampleSubway;
