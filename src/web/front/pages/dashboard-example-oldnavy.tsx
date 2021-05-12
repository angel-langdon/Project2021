import Dashboard from "@/components/dashboard/Dashboard";
import data from "../public/data/old_navy.json";
import { preprocessPatternsData } from "@/utils/dataUtils.js";

export default function DashboardExampleOldNavy() {
  const processedData = preprocessPatternsData(data);
  return (
    <Dashboard
      store="Old Navy"
      data={processedData}
      brandImage="/images/old-navy-logo.png"
      colors={["#002B50", "#FF5C23"]}
    />
  );
}
