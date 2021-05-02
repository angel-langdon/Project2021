import NavigationBar from "@/components/NavigationBar"
import Footer from "@/components/Footer"

export default function AboutUs() {
    return (<>
  <title>Entre Datos</title>
  <div className="page-holder">
    <div className="header-holder theagency">
      <div className="color-overlay" />
      <NavigationBar/>
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
            <div><div className="top-line" /></div>
            <h3>Entre Datos is not just a creative agency.</h3>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ut vehicula ante. Donec turpis est, pulvinar sed ipsum sed, hendrerit blandit mauris. Cras egestas eget augue vel pulvinar.</p>
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
            <div className="info-card-img"><img src="images/team1.jpg" /></div>
            <div className="info-card-details">
              <div className="person-name">Anne Robbins</div>
              <div className="person-title">Co-Founder</div>
              <div className="person-email">anne@designway.co</div>
              <div className="person-phone">+973 912949238</div>
              <div className="person-social">Instagram: @annerobbin</div>
            </div>
          </div>
        </div>
        <div className="col-xs-12 col-sm-6 col-md-3">
          <div className="info-card">
            <div className="info-card-img"><img src="images/team2.jpg" /></div>
            <div className="info-card-details">
              <div className="person-name">Mary Adam</div>
              <div className="person-title">Project manager</div>
              <div className="person-email">mary@designway.co</div>
              <div className="person-phone">+973 912949238</div>
              <div className="person-social">Instagram: @maryadam</div>
            </div>
          </div>
        </div>
        <div className="col-xs-12 col-sm-6 col-md-3">
          <div className="info-card">
            <div className="info-card-img"><img src="images/team3.jpg" /></div>
            <div className="info-card-details">
              <div className="person-name">Tonny Brendon</div>
              <div className="person-title">Coder &amp; developer</div>
              <div className="person-email">tonny@designway.co</div>
              <div className="person-phone">+973 912949238</div>
              <div className="person-social">Instagram: @tonybrendon</div>
            </div>
          </div>
        </div>
        <div className="col-xs-12 col-sm-6 col-md-3">
          <div className="info-card">
            <div className="info-card-img"><img src="images/team4.jpg" /></div>
            <div className="info-card-details">
              <div className="person-name">Rhea Fitzpatric</div>
              <div className="person-title">Web designer</div>
              <div className="person-email">rhea@designway.co</div>
              <div className="person-phone">+973 912949238</div>
              <div className="person-social">Instagram: @rheafitric</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer/>
  </div>
</>)

}