import dynamic from "next/dynamic";
import KPIsTop from "@/components/dashboard/KPIsTop";
import DefaultHeader from "@/components/DefaultHeader";
import { useState } from "react";
import React from "react";
import KPIsPlotVisits from "./KPIsPlotVisits";
import DashboardHeader from "./DashboardHeader";
import DashboardStats from "@/components/dashboard/DashboardStats";
import { uniqueValues } from "@/utils/dataUtils";
const LinePlotVisits = dynamic(
  () => import("@/components/dashboard/LinePlotVisits"),
  { ssr: false }
);

// ? for optional parameters
interface IProps {
  store: string;
  data: Array<any>;
  filteredData?: object;
  brandImage: string;
  placekey?: string;
  uniqueStores?: Array<any>;
  setFilteredData?: any;
}

const Dashboard = (props: IProps) => {
  // By default we pick the first place key
  const [placekey, setPlacekey] = useState<string>(props.data[0]["placekey"]);
  const [filteredData, setFilteredData] = useState<Array<object>>(
    props.data.filter((object) => object.placekey == placekey)
  );
  const uniqueStores: Array<object> = uniqueValues(props.data, "placekey");
  props = {
    ...props,
    filteredData: filteredData,
    placekey: placekey,
    uniqueStores: uniqueStores,
    setFilteredData: setFilteredData,
  };
  return (
    <div className="dashboard-container">
      <DefaultHeader />
      <DashboardHeader {...props} />
      <DashboardStats {...props} />
    </div>
  );
};

export default Dashboard;
