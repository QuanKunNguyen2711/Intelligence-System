import { Button, Nav, NavItem } from "reactstrap";
import { Link, useLocation } from "react-router-dom";
import user1 from "../assets/images/users/user4.jpg";
import probg from "../assets/images/bg/download.jpg";

const navigation = [
  // {
  //   title: "Dashboard",
  //   href: "/starter",
  //   icon: "bi bi-speedometer2",
  // },
  // {
  //   title: "Alert",
  //   href: "/alerts",
  //   icon: "bi bi-bell",
  // },
  // {
  //   title: "Badges",
  //   href: "/badges",
  //   icon: "bi bi-patch-check",
  // },
  // {
  //   title: "Buttons",
  //   href: "/buttons",
  //   icon: "bi bi-hdd-stack",
  // },
  {
    title: "AI Datasets",
    href: "/home/datasets",
    icon: "bi bi-card-text",
  },
  {
    title: "Model Training",
    href: "/home/model",
    icon: "bi bi-speedometer2",
  },
  {
    title: "Model Inference",
    href: "/home/inference",
    icon: "bi bi-textarea-resize",
  },
  // {
  //   title: "Cards",
  //   href: "/cards",
  //   icon: "bi bi-card-text",
  // },
  // {
  //   title: "Grid",
  //   href: "/grid",
  //   icon: "bi bi-columns",
  // },
  // {
  //   title: "Table",
  //   href: "/table",
  //   icon: "bi bi-layout-split",
  // },
  
  // {
  //   title: "Breadcrumbs",
  //   href: "/breadcrumbs",
  //   icon: "bi bi-link",
  // },
  // {
  //   title: "About",
  //   href: "/about",
  //   icon: "bi bi-people",
  // },
];

const Sidebar = () => {
  const showMobilemenu = () => {
    document.getElementById("sidebarArea").classList.toggle("showSidebar");
  };
  let location = useLocation();

  return (
    <div>
      <div className="d-flex align-items-center"></div>
      <div
        className="profilebg"
        style={{ background: `url(${probg}) no-repeat` }}
      >
        <div className="p-3 d-flex">
          <img src={user1} alt="user" width="50" className="rounded-circle" />
          <Button
            color="white"
            className="ms-auto text-white d-lg-none"
            onClick={() => showMobilemenu()}
          >
            <i className="bi bi-x"></i>
          </Button>
        </div>
        <div className="bg-dark text-white p-2 opacity-75">Hồng Quân Hotel</div>
      </div>
      <div className="p-3 mt-2">
        <Nav vertical className="sidebarNav">
          {navigation.map((navi, index) => (
            <NavItem key={index} className="sidenav-bg">
              <Link
                to={navi.href}
                className={
                  location.pathname === navi.href
                    ? "active nav-link py-3"
                    : "nav-link text-secondary py-3"
                }
              >
                <i className={navi.icon}></i>
                <span className="ms-3 d-inline-block">{navi.title}</span>
              </Link>
            </NavItem>
          ))}
  
        </Nav>
      </div>
    </div>
  );
};

export default Sidebar;
