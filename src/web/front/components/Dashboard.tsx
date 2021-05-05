import dynamic from "next/dynamic";
import KPIs from "@/components/KPIs";
import { useState } from "react";
const LinePlotVisits = dynamic(() => import("@/components/LinePlotVisits"), {
  ssr: false,
});

interface IProps {
  store: string;
  data: object;
}

const Dashboard = (props: IProps) => {
  // By default we pick the first place key
  const [placekey, setPlacekey] = useState<string>(props.data[0]["placekey"]);
  return (
    <div className="dashboard-container">
      <KPIs {...props} placekey={placekey} />
      <div>
        <LinePlotVisits {...props} placekey={placekey} />
      </div>
    </div>
  );
};

export default Dashboard;
