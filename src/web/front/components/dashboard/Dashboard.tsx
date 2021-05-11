import dynamic from "next/dynamic";
import DefaultHeader from "@/components/DefaultHeader";
import { useEffect, useState } from "react";
import React from "react";
import DashboardHeader from "./DashboardHeader";
import DashboardStats from "@/components/dashboard/DashboardStats";
import { getColumn, uniqueValues } from "@/utils/dataUtils";
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
  dates?: Array<Date>;
  uniqueDates?: Set<Date>;
  minMaxDates?: Array<Date>;
  setFilteredData?: any;
  setDates: any;
  setPlacekey?: any;
}

const Dashboard = (props: IProps) => {
  // By default we pick the first place key
  const [placekey, setPlacekey] = useState<string>(props.data[0]["placekey"]);
  const [filteredData, setFilteredData] = useState<Array<object>>(
    props.data.filter((object) => object.placekey == placekey)
  );
  const uniqueStores: Array<object> = uniqueValues(props.data, "placekey");
  const uniqueDates: Set<Date> = new Set(getColumn(filteredData, "date"));
  let sortedDates = Array.from(uniqueDates);
  sortedDates.sort();
  const [dates, setDates] = useState([
    sortedDates[0],
    sortedDates[sortedDates.length - 1],
  ]);
  const [minMaxDates, setMinMaxDates] = useState([
    sortedDates[0],
    sortedDates[sortedDates.length - 1],
  ]);

  props = {
    ...props,
    filteredData: filteredData,
    placekey: placekey,
    uniqueStores: uniqueStores,
    dates: dates,
    uniqueDates: uniqueDates,
    minMaxDates: minMaxDates,
    setPlacekey: setPlacekey,
    setDates: setDates,
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
