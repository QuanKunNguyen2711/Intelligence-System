
import React, {lazy} from "react";
import { useRoutes, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "../Provider/AuthProvider";
import PrivateRoute from "./PrivateRoute";

/****Layouts*****/
const FullLayout = lazy(() => import("../layouts/FullLayout.js"));

/***** Pages ****/
const Starter = lazy(() => import("../views/Starter.js"));
const About = lazy(() => import("../views/About.js"));
const Alerts = lazy(() => import("../views/ui/Alerts"));
const Badges = lazy(() => import("../views/ui/Badges"));
const Buttons = lazy(() => import("../views/ui/Buttons"));
const Cards = lazy(() => import("../views/ui/Cards"));
const Grid = lazy(() => import("../views/ui/Grid"));
const Tables = lazy(() => import("../views/ui/Tables"));
const Datasets = lazy(() => import("../views/ui/Datasets.js"));
const Login = lazy(() => import("../views/ui/Login"));
// const Breadcrumbs = lazy(() => import('../views/ui/Breadcrumbs'));
// const Unauthorized = lazy(() => import('../views/ui/Unauthorized'));

const routes = [
  { path: "/", element: <Navigate to="/datasets" /> },
  // { path: "/starter", element: <Starter /> },
  // { path: "/about", element: <About /> },
  // { path: "/alerts", element: <Alerts /> },
  // { path: "/badges", element: <Badges /> },
  // { path: "/buttons", element: <Buttons /> },
  { path: "/cards", element: <Cards /> },
  // { path: "/grid", element: <Grid /> },
  { path: "/table", element: <Tables /> },
  { path: "/datasets", element: <Datasets /> },
  { path: "/login", element: <Login /> },
];

// export const AppRoutes = () => {
//   const { user } = useAuth();
//   console.log(user)
//   const routing = useRoutes(
//     routes.map((route) => ({
//       ...route,
//       element: route.path === '/login' ? route.element : user ? <PrivateRoute element={route.element} /> : <Navigate to="/login" />
//     }))
//   );

//   return <div className="dark">{routing}</div>;
// };