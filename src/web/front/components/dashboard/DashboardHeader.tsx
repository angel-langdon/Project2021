import DashboardSearcher from "./DashboardSearcher";

const DashboardHeader = (props) => {
  return (
    <div className="dashboard-header">
      <div className="d-flex justify-content-between">
        <div className="row photo-and-text">
          <div className="brand-image-container d-flex flex-column justify-content-center ">
            <img src={props.brandImage} className="brand-image"></img>
          </div>
          <div className="col dashboard-header-info">
            <h4 className="title">{props.filteredData[0].brands}</h4>
            <h6 className="street">{props.filteredData[0].street_address}</h6>
            <h6 className="zip-code">
              Postal code: {props.filteredData[0].postal_code}
            </h6>
          </div>
        </div>
        <div className="d-flex flex-column justify-content-center">
          <DashboardSearcher {...props} />
        </div>
      </div>
    </div>
  );
};

export default DashboardHeader;
