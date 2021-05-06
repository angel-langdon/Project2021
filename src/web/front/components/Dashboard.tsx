import dynamic from "next/dynamic";
import KPIs from "@/components/KPIs";
import DefaultHeader from "@/components/DefaultHeader";
import { useState } from "react";
const LinePlotVisits = dynamic(() => import("@/components/LinePlotVisits"), {
  ssr: false,
});
// ? for optional parameters
interface IProps {
  store: string;
  data: Array<any>;
  filteredData?: object;
  placekey?: string;
}

const Dashboard = (props: IProps) => {
  // By default we pick the first place key
  const [placekey, setPlacekey] = useState<string>(props.data[0]["placekey"]);
  const [filteredData, setFilteredData] = useState<Array<object>>(
    props.data.filter((object) => object.placekey == placekey)
  );
  props = { ...props, filteredData: filteredData, placekey: placekey };
  return (
    <div className="dashboard-container">
      <DefaultHeader />
      <div className="row horizontal-kpis-container">
        <KPIs {...props} />
      </div>
      <div className="row">
        <LinePlotVisits {...props} />
      </div>
    </div>
  );
};

export default Dashboard;
