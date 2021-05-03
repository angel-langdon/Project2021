const NavigationBar = () => {
  return (
    <div id="header" className="container-fluid">
      <div className="container">
        <div className="row">
          <div id="toggle-menu">
            <span className="toggle-icon ti1" />
            <span className="toggle-icon ti2" />
            <span className="toggle-icon ti3" />
          </div>
          <div className="col-md-3">
            <a href="/">
              <img className="logo" src="/images/logo.png" />
            </a>
          </div>
          <div className="col-md-9 menu-col">
            <div id="menu-holder">
              <ul className="main-menu">
                <li>
                  <a href="succes-stories">
                    Succes stories
                    <span className="link-underline" />
                  </a>
                </li>
                <li>
                  <a href="about-us">
                    About us
                    <span className="link-underline" />
                  </a>
                </li>
                <li>
                  <a href="/#services">
                    Services
                    <span className="link-underline" />
                  </a>
                </li>
                <li>
                  <a href="contact">
                    Contact
                    <span className="link-underline" />
                  </a>
                </li>
                <li>
                  <a href="dashboard">
                    Dashboard Example
                    <span className="link-underline" />
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default NavigationBar;
