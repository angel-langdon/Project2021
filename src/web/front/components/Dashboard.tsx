import dynamic from "next/dynamic";
import KPIs from "@/components/KPIs";
import { useState } from "react";
const LinePlotVisits = dynamic(() => import("@/components/LinePlotVisits"), {
  ssr: false,
});

interface IProps {
  store: string;
  data: object;
  filteredData: object;
  placekey: string;
}

const Dashboard = (props: IProps) => {
  // By default we pick the first place key
  const [placekey, setPlacekey] = useState<string>(props.data[0]["placekey"]);
  const [filteredData, setFilteredData] = useState(
    props.data.filter((object) => object.placekey == placekey)
  );
  props = { ...props, filteredData: filteredData, placekey: placekey };
  return (
    <div className="dashboard-container">
      <KPIs {...props} />
      <div>
        <LinePlotVisits {...props} />
      </div>
    </div>
  );
};

export default Dashboard;
