import MeanVisits from "./MeanVisits";

const DashboardStats = (props) => {
  return (
    <div className="col dashboard-stats">
      <div className="d-flex dashboard-stats-1-row">
        <MeanVisits {...props} />
        <div style={{ width: 20 }} />

        <MeanVisits {...props} />
      </div>
    </div>
  );
};

export default DashboardStats;
