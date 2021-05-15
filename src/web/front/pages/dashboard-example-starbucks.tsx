import Dashboard from "@/components/dashboard/Dashboard";
import data from "../public/data/starbucks.json";
import { preprocessPatternsData } from "@/utils/dataUtils.js";

export default function DashboardExampleStarbucks() {
  const processedData = preprocessPatternsData(data);
  return (
    <Dashboard
      store="Starbucks"
      data={processedData}
      brandImage={require("../public/images/starbucks-logo.png")}
      colors={["#008A3D", "#000"]}
    />
  );
}
