import NavigationBar from "@/components/NavigationBar";
import DefaultHeader from "@/components/DefaultHeader";

export default function ContactUs() {
  return (
    <div>
      <DefaultHeader />
      <div className="page-holder">
        <div className="header-holder contactus">
          <div className="color-overlay" />
          <NavigationBar />
          <div id="top-content" className="container-fluid">
            <div className="container">
              <div className="row">
                <div className="col-xs-12">
                  <h1>Contact us</h1>
                  <h1 className="headline"></h1>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* 
        <div id="text-container" className="container-fluid">
          <div className="container">
            <div className="row">
              <div className="col-md-12">
                <h3>Entre Datos is a company of good, intelligent</h3>
                <p>
                  WLorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Mauris egestas non ante non consequat. Aenean accumsan eros
                  vel elit tristique, non sodales nunc luctus. Etiam vitae odio
                  eget orci finibus auctor ut eget magna.
                </p>
              </div>
            </div>
          </div>
        </div> 
        */}
        <div id="contact-details" className="container-fluid">
          <div className="row">
            <div className="col-md-6 address-holder">
              {/* <h3>Contact us</h3>  */}
              <p>
                If you'd like to chat to our team about how we can help you
                achieve great results, send us your details by email and we'll
                be in touch. Drop a line about your project or describe a
                challenge your company needs help solving. We’d love to discuss
                all the details with you scheduling a meeting as soon as
                possible.
              </p>
              <div className="address">
                <div className="col-xs-1 col-sm-1">
                  <i className="fa fa-envelope-o" aria-hidden="true" />
                </div>
                <div className="col-xs-11 col-sm-5">
                  <div className="address-row">
                    <span>entredatoses@gmail.com</span>
                  </div>
                </div>
                <div className="col-xs-1 col-sm-1">
                  <i className="fa fa-map-marker" aria-hidden="true" />
                </div>
                <div className="col-xs-11 col-sm-5">
                  <div className="address-row">
                    UPV, Valencia, Camí de Vera, s/n, 46009, Spain{" "}
                  </div>
                  <div className="address-row"></div>
                  <div className="address-row"></div>
                </div>
              </div>
            </div>
            <div className="col-md-6 contact-text">
              <div className="div-bg" />
              <h3>Your Data holds the answers,</h3>
              <h3>Let's discover them together!</h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
