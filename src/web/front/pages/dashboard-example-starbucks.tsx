import Dashboard from "@/components/dashboard/Dashboard";
import data from "../public/data/starbucks.json";
import { preprocessPatternsData } from "@/utils/dataUtils.js";

export default function DashboardExampleStarbucks() {
  const processedData = preprocessPatternsData(data);
  return (
    <Dashboard
      store="Starbucks"
      data={processedData}
      brandImage="/images/starbucks-logo.png"
      colors={["rgb(8, 82, 0)", "rgb(189, 183, 0)"]}
    />
  );
}
