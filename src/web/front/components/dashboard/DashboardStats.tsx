import MeanVisits from "./MeanVisits";

const DashboardStats = (props) => {
  return (
    <div className="col dashboard-stats">
      <MeanVisits {...props} />
    </div>
  );
};

export default DashboardStats;
