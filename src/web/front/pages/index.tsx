import Footer from "@/components/Footer";
import NavigationBar from "@/components/NavigationBar";
import DefaultHeader from "@/components/DefaultHeader";
import Link from "next/link";
import SuccessStoriesList from "@/components/SuccessStoriesList";

export default function Home() {
  return (
    <div>
      <DefaultHeader />
      <div id="case-study-popup">
        <div className="popup-content-holder">
          <div id="closebtn" />
          <div className="popup-content">
            <div className="container-fluid">
              <div className="row">
                <div className="col-md-7 p-image">
                  <div className="image-holder">
                    <div className="project-slider">
                      <div>
                        <img src={require("../public/images/pro1.jpg")} />
                      </div>
                      <div>
                        <img src={require("../public/images/pro2.jpg")} />
                      </div>
                      <div>
                        <img src={require("../public/images/pro3.jpg")} />
                      </div>
                    </div>
                  </div>
                </div>
                <div className="col-md-5 p-details">
                  <div className="details-holder">
                    <h3 className="project-title">Pharmancie</h3>
                    <p className="info-text">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Morbi ut vehicula ante. Donec turpis est, pulvinar sed
                      ipsum sed, hendrerit blandit mauris. Cras egestas eget
                      augue vel pulvinar.
                    </p>
                    <h3>Skills</h3>
                    <p className="skills">
                      Auctor lobortis
                      <br />
                      Vel scelerisque
                      <br />
                      Posuere imperdie
                    </p>
                    <h3>Date Completed</h3>
                    <p className="datecompleted">June 01, 2016</p>
                    <div className="dw-button">
                      <div className="dw-button-bg" />
                      <a className="dw-button-link" href="#" target="_blank">
                        View project’s site
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="page-holder">
        <div className="header-holder">
          <div className="color-overlay" />
          <NavigationBar />
          <div id="top-content" className="container-fluid">
            <div className="container">
              <div className="row row1">
                <div className="col-xs-12">
                  <div className="big-title">
                    <div className="textover text-animate-in-out">
                      We're EntreDatos.
                    </div>
                    <div className="textover text-animate-in-out text-animate-in-out-delay1">
                      {" "}
                      Data Scientists.{" "}
                    </div>
                    <div className="textover text-animate-in-out text-animate-in-out-delay2">
                      {" "}
                      Model creators.
                    </div>
                  </div>
                  <h1 className="headline">
                    {" "}
                    Empower your business with Data Science and AI technology.
                  </h1>
                </div>
              </div>
              <div className="row row2">
                <div className="col-xs-12 ">
                  <div className="dw-button">
                    <div className="dw-button-bg" />
                    <Link href="/success-stories">
                      <a className="dw-button-link">Success stories</a>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div id="info1" className="container-fluid">
          <div className="container">
            <div className="row">
              <div className="col-xs-12 col-md-5 info-text-holder">
                <div>
                  <div className="top-line" />
                </div>
                <h3>We are based in Spain, Valencia</h3>
                <p> </p>
                <p>
                  We are a young team formed by six students who founded
                  EntreDatos in response to growing market demand. Our main goal
                  is to transform complex data sets into tangible solutions,
                  which requires science, commitment, desire and a little bit of
                  creativity😉.
                </p>
              </div>
              <div className="col-xs-12 col-md-7">
                <div className="offices-slider">
                  <div>
                    <img src={require("../public/images/office1.jpg")} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div id="info2" className="container-fluid">
          <div className="container">
            <div className="row">
              <div className="col-xs-12 col-md-4">
                <div className="info-box">
                  <h4>Who</h4>
                  <p>
                    A group of six students about to finish DataScience Degree
                    at the Polytechnic University of Valencia looking forward to
                    expanding their knowledge with new challenge.
                  </p>
                </div>
              </div>
              <div className="col-xs-12 col-md-4">
                <div className="info-box">
                  <h4>Why</h4>
                  <p>
                    To provide tangible solutions to our clients by extracting
                    knowledge from their data.
                  </p>
                </div>
              </div>
              <div className="col-xs-12 col-md-4">
                <div className="info-box">
                  <h4>What</h4>
                  <p>
                    Machine Learning, Prediction Modeling, Analytics and
                    Consulting services.
                  </p>
                  <p>
                    As Charles Babbage said: “Errors using inadequate data are
                    much less than those using no data at all.”
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div id="recent-studies" className="container-fluid">
          <div className="container">
            <div className="row">
              <div className="col-xs-12">
                <h3>Recent Success stories</h3>
              </div>
            </div>
            <div className="row">
              <div className="projects-list">
                <SuccessStoriesList />
              </div>
            </div>
          </div>
        </div>

        <div id="services" className="container-fluid">
          <div className="container">
            <div className="row">
              <div className="col-xs-12 title-holder">
                <h3>Our Services</h3>
              </div>
            </div>
            <div className="row">
              <div className="col-xs-12 col-sm-6 col-md-4">
                <div className="service-box">
                  <div className="service-box-bg" />
                  <div className="service-title">
                    <i className="fa fa-line-chart" /> Conductive Exploratory
                    Data Analysis (EDA)
                  </div>
                  <p>
                    Our first step in cooperation with businesses of any size,
                    is EDA, before passing to the model building and training
                    process. Our clients can retrieve valuable dashboards and
                    data-based recommendations as a result of EDA..
                  </p>
                </div>
              </div>
              <div className="col-xs-12 col-sm-6 col-md-4">
                <div className="service-box">
                  <div className="service-box-bg" />
                  {/* el antes ponía eso: <i class="dw dw-icon2">*/}
                  <div className="service-title">
                    <i className="fa fa-line-chart" /> Predictive Analytics
                  </div>
                  <p>
                    {" "}
                    Anticipate customer behavior and outcomes and steer your
                    business in the right direction. We offer the best-fit
                    approach for processing the provided data in order to built
                    efficient models..
                  </p>
                </div>
              </div>
              <div className="col-xs-12 col-sm-6 col-md-4">
                <div className="service-box">
                  <div className="service-box-bg" />
                  <div className="service-title">
                    <i className="fa fa-line-chart" /> Deep Learning Solutions
                  </div>
                  <p>
                    We significantly improve business metrics by fine-tuning the
                    performance of algorithms powered by artificial neural
                    networks..
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
