import NavigationBar from "@/components/NavigationBar";
import Footer from "@/components/Footer";
import DefaultHeader from "@/components/DefaultHeader";

export default function AboutUs() {
  return (
    <div>
      <DefaultHeader />
      <title>Entre Datos</title>
      <div className="page-holder">
        <div className="header-holder theagency">
          <div className="color-overlay" />
          <NavigationBar />
          <div id="top-content" className="container-fluid">
            <div className="container">
              <div className="row">
                <div className="col-xs-12">
                  <h1>About us</h1>
                  <h1 className="headline">The story behind Entre Datos.</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div id="info3" className="container-fluid">
          <div className="container">
            <div className="row">
              <div className="col-md-12 info-text-holder">
                <div>
                  <div className="top-line" />
                </div>
                <h3>Teamwork divides the task and multiplies success</h3>
                {/* 
                <p>
                  It is a project created by six students in a third year of DataScience Degree.
                </p>*/}
              </div>
            </div>
          </div>
        </div>
        <div id="team" className="container-fluid">
          <div className="row">
            <div className="col-xs-12">
              <h3 className="title-with-line">Our gurus</h3>
            </div>
          </div>
          <div className="row">
            <div className="col-xs-12 col-sm-6 col-md-3">
              <div className="info-card">
                <div className="info-card-img">
                  <img src="images/team1.jpg" />
                </div>
                <div className="info-card-details">
                  <div className="person-name">Ignacio Cano Navarro</div>
                  <div className="person-title"> CEO and founder</div>
                  <div className="person-email">nachonavarrocano@gmail.com</div>
                  <ul
                    className="person-linkedin"
                  >
                   <a href="https://www.linkedin.com/in/ignacio-cano/"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                  </ul>
                </div>
              </div>
            </div>
            <div className="col-xs-12 col-sm-6 col-md-3">
              <div className="info-card">
                <div className="info-card-img">
                  <img src="images/team2.jpg" />
                </div>
                <div className="info-card-details">
                  <div className="person-name">Álvaro Mazcuñán Herreros</div>
                  <div className="person-title">Project manager</div>
                  <div className="person-email">
                    alvaromazcuherreros@gmail.com
                  </div>
                  <ul
                    className="person-linkedin"
                  >
                   <a href="https://www.linkedin.com/in/alvaro-mazcu-herreros/"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                  </ul>
                </div>
              </div>
            </div>
            <div className="col-xs-12 col-sm-6 col-md-3">
              <div className="info-card">
                <div className="info-card-img">
                  <img src="images/team3.jpg" />
                </div>
                <div className="info-card-details">
                  <div className="person-name">Lisa Gilyarovskaya</div>
                  <div className="person-title">Coder &amp; developer</div>
                  <div className="person-email">
                    lisa.gilyarovskaya@gmail.com
                  </div>
                  <ul
                    className="person-linkedin"
                  >
                   <a href="https://www.linkedin.com/in/lisagilyarovskaya"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                  </ul>
                </div>
              </div>
            </div>
            <div className="col-xs-12 col-sm-6 col-md-3">
              <div className="info-card">
                <div className="info-card-img">
                  <img src="images/team4.jpg" />
                </div>
                <div className="info-card-details">
                  <div className="person-name">Miquel Marin Colomé</div>
                  <div className="person-title">
                    Machine Learning specialist
                  </div>
                  <div className="person-email">miquelmarin43@gmail.com</div>
                  <ul
                    className="person-linkedin"
                  >
                   <a href="https://www.linkedin.com/in/miquel-marin-colome/"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                  </ul>
                </div>
              </div>
            </div>
            <div className="col-xs-12 col-sm-6 col-md-3">
              <div className="info-card">
                <div className="info-card-img">
                  <img src="images/team5.jpg" />
                </div>
                <div className="info-card-details">
                  <div className="person-name">Angel Langdon Villamayor</div>
                  <div className="person-title">
                    Data Scientist & Software Engineer
                  </div>
                  <div className="person-email">supername1337@gmail.com</div>
                  <ul
                    className="person-linkedin"
                  >
                   <a href="https://www.linkedin.com/in/ángel-langdon-villamayor-a44b49187/"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                  </ul>
                </div>
              </div>
            </div>
            <div className="col-xs-12 col-sm-6 col-md-3">
              <div className="info-card">
                <div className="info-card-img">
                  <img src="images/team6.jpg" />
                </div>
                <div className="info-card-details">
                  <div className="person-name">Iker Rodríguez Martínez</div>
                  <div className="person-title">Commercial Agent</div>
                  <div className="person-email">ikrodmar@upv.edu.es</div>
                  <ul
                    className="person-linkedin"
                  >
                   <a href="#"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    </div>
  );
}
{/*
<div class="col-xs-12 col-sm-6 col-md-3 list-holder">
<h4>Media</h4>
<ul class="list-menu">
    <li><a href="#"><i class="fa fa-behance"></i>Behance Network</a></li>
    <li><a href="#"><i class="fa fa-youtube"></i>Youtube</a></li>
    <li><a href="#"><i class="fa fa-twitter"></i>Twitter</a></li>
    <li><a href="#"><i class="fa fa-facebook"></i>Facebook</a></li>
    <li><a href="#"><i class="fa fa-instagram"></i>Instagram</a></li>
    <li><a href="#"><i class="fab fa-linkedin-in"></i>Linkedin</a></li>
</ul>
</div>
 */}