import Dashboard from "@/components/dashboard/Dashboard";
import data from "../public/data/walmart.json";
import { preprocessPatternsData } from "@/utils/dataUtils.js";

export default function DashboardExampleWalmart() {
  const processedData = preprocessPatternsData(data);
  return (
    <Dashboard
      store="Old Navy"
      data={processedData}
      brandImage={require("../public/images/walmart-logo.png")}
      colors={["#0056B4", "#FFAA3D"]}
    />
  );
}
