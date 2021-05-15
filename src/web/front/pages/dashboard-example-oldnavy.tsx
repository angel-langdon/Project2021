import Dashboard from "@/components/dashboard/Dashboard";
import data from "../public/data/old_navy.json";
import { preprocessPatternsData } from "@/utils/dataUtils.js";
import logo from "../public/images/old-navy-logo.png";

export default function DashboardExampleOldNavy() {
  const processedData = preprocessPatternsData(data);
  return (
    <Dashboard
      store="Old Navy"
      data={processedData}
      brandImage={logo}
      colors={["#002B50", "#FF5C23"]}
    />
  );
}
