import Link from "next/link";
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
            <Link href="/">
              <a>
                <img
                  className="logo"
                  src={require("../public/images/logo.png")}
                />
              </a>
            </Link>
          </div>
          <div className="col-md-9 menu-col">
            <div id="menu-holder">
              <ul className="main-menu">
                <li>
                  <Link href="/success-stories">
                    <a>
                      Success stories
                      <span className="link-underline" />
                    </a>
                  </Link>
                </li>
                <li>
                  <Link href="/about-us">
                    <a>
                      About us
                      <span className="link-underline" />
                    </a>
                  </Link>
                </li>
                <li>
                  <Link href="/#services">
                    <a>
                      Services
                      <span className="link-underline" />
                    </a>
                  </Link>
                </li>
                <li>
                  <Link href="/contact">
                    <a>
                      Contact
                      <span className="link-underline" />
                    </a>
                  </Link>
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
