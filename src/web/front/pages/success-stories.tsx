import DefaultHeader from "@/components/DefaultHeader";
import Footer from "@/components/Footer";
import NavigationBar from "@/components/NavigationBar";
import SuccessStory from "@/components/SuccessStory";

export default function CaseStudies() {
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
                      {/* 
                      <div>
                        <img src="images/pro3.jpg" />
                      </div> */}
                    </div>
                  </div>
                </div>
                <div className="col-md-5 p-details">
                  <div className="details-holder">
                    <h3 className="project-title">Subway</h3>
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
                      Posuere imperdiet
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
        <div className="header-holder casestudies">
          <div className="color-overlay" />
          <NavigationBar />
          <div id="top-content" className="container-fluid">
            <div className="container">
              <div className="row">
                <div className="col-xs-12">
                  <h1>Success stories.</h1>
                  <h1 className="headline">
                    Our Best Work For the Best People.
                  </h1>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div id="recent-studies" className="container-fluid">
          <div className="container">
            <div className="row">
              <div className="projects-list full-list">
                <SuccessStory
                  store="Subway"
                  img="/images/subway-card.jpg"
                  msg="Subway is very good company that does sandwiches for hungry and hurried people.
                       We built a predictive model that was able to predict the number of visitors"
                />
                <SuccessStory
                  store="Starbucks"
                  img="/images/starbucks-card.jpeg"
                  msg="Starbucks is a hipster place, we all know...  With our model we were able to predict the number of visitors pretty good"
                />
                {/* 
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro3.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 3</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro4.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 4</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro5.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 5</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro6.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 6</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro7.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 7</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro8.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 8</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro1.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 9</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro2.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 10</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro3.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 11</h4>
                          </div>
                      </a>
                  </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3 project-box-holder">
                  <div class="project-box">
                      <a href="#">
                          <img class="project-img" src="images/pro4.jpg" alt="">
                          <div class="box-overlay">
                              <h4>Text 12</h4>
                          </div>
                      </a>
                  </div>
              </div> */}
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    </div>
  );
}
