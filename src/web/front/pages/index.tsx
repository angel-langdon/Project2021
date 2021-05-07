import Footer from "@/components/Footer";
import NavigationBar from "@/components/NavigationBar";
import DefaultHeader from "@/components/DefaultHeader";
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
                        <img src="images/pro1.jpg" />
                      </div>
                      <div>
                        <img src="images/pro2.jpg" />
                      </div>
                      <div>
                        <img src="images/pro3.jpg" />
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
                    <a className="dw-button-link" href="success-stories">
                      Success stories
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* 
    <div id="counts" class="container-fluid">
  <div class="container">
      <div class="row">
          <div class="col-xs-12 col-sm-6 col-md-3 text-center">
              <div class="count-box">
                  <h1>7</h1>
                  <img src="images/countlogo1.png" alt="">
              </div>
          </div>
          <div class="col-xs-12 col-sm-6 col-md-3 text-center">
              <div class="count-box">
                  <h1>3</h1>
                  <img src="images/countlogo2.png" alt="">
              </div>
          </div>
          <div class="col-xs-12 col-sm-6 col-md-3 text-center">
              <div class="count-box">
                  <h1>8</h1>
                  <img src="images/countlogo3.png" alt="">
              </div>
          </div>
          <div class="col-xs-12 col-sm-6 col-md-3 text-center">
              <div class="count-box">
                  <h1>5</h1>
                  <img src="images/countlogo4.png" alt="">
              </div>
          </div>
      </div>
  </div>
    </div>
    */}
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
                    <img src="images/office1.jpg" />
                  </div>
                  {/* 
                  <div>
                    <img src="images/office2.jpg" />
                  </div> */}
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
            {/*}
            <div className="row">
              <div className="col-xs-12 text-right">
                <a className="view-all-link" href="casestudies.html">
                  <div className="link-text">view all</div>{" "}
                  <div className="plus-icon">
                    <span className="plus-line line1" />
                    <span className="plus-line line2" />
                  </div>
                </a>
              </div>
            </div>
            */}
            <div className="row">
              <div className="projects-list">
                <SuccessStoriesList />
                {/*  
                <div className="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div className="project-box">
                    <a href="#">
                      <img className="project-img" src="images/pro3.jpg" />
                      <div className="box-overlay">
                        <h4>Text 3</h4>
                      </div>
                    </a>
                  </div>
                </div>
                <div className="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div className="project-box">
                    <a href="#">
                      <img className="project-img" src="images/pro4.jpg" />
                      <div className="box-overlay">
                        <h4>Text 4</h4>
                      </div>
                    </a>
                  </div>
                </div>
                <div className="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div className="project-box">
                    <a href="#">
                      <img className="project-img" src="images/pro5.jpg" />
                      <div className="box-overlay">
                        <h4>Text 5</h4>
                      </div>
                    </a>
                  </div>
                </div> */}

                {/* 
                <div className="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div className="project-box">
                    <a href="#">
                      <img className="project-img" src="images/pro6.jpg" />
                      <div className="box-overlay">
                        <h4>Text 6</h4>
                      </div>
                    </a>
                  </div>
                </div>
                <div className="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div className="project-box">
                    <a href="#">
                      <img className="project-img" src="images/pro7.jpg" />
                      <div className="box-overlay">
                        <h4>Text 7</h4>
                      </div>
                    </a>
                  </div>
                </div>
                <div className="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div className="project-box">
                    <a href="#">
                      <img className="project-img" src="images/pro8.jpg" />
                      <div className="box-overlay">
                        <h4>Text 8</h4>
                      </div>
                    </a>
                  </div>
                </div> */}
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
              {/* 
          <div class="col-xs-12 col-sm-6 col-md-4">
              <div class="service-box">
                  <div class="service-box-bg"></div>
                  <div class="service-title"><i class="dw dw-icon4"></i>Data Capture</div>
                  <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris egestas non ante non consequat. Aenean accumsan eros vel elit tristique, non sodales nunc luctus. Etiam vitae odio eget.</p>
              </div>
          </div>
          */}
            </div>
          </div>
        </div>
      </div>
      {/* 
                <div id="top-footer" class="container-fluid">
              <div class="image-bg"></div>
              <div class="container">
                  <div class="row">
                      <div class="col-xs-12">
                          <h3>Lorem ipsum dolor sit amet, consectetur adipiscing elit</h3>
                          <div class="dw-botton2"><a href="#">contact us</a></div>
                      </div>
                  </div>
              </div>
                </div>
                */}
      <Footer />
    </div>
  );
}
