import React, { lazy } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { AuthProvider, useAuth } from "../Provider/AuthProvider.js";
import PrivateRouter from "./PrivateRoute.js";

/****Layouts*****/
const FullLayout = lazy(() => import("../layouts/FullLayout.js"));

/***** Pages ****/
const Starter = lazy(() => import("../views/Starter.js"));
// const About = lazy(() => import("../views/About.js"));
// const Alerts = lazy(() => import("../views/ui/Alerts"));
// const Badges = lazy(() => import("../views/ui/Badges"));
// const Buttons = lazy(() => import("../views/ui/Buttons"));
const Cards = lazy(() => import("../views/ui/Cards.js"));
// const Grid = lazy(() => import("../views/ui/Grid"));
const Tables = lazy(() => import("../views/ui/Tables.js"));
const Datasets = lazy(() => import("../views/ui/Datasets.js"));
const Login = lazy(() => import("../views/ui/Login.js"));
const Model = lazy(() => import("../views/ui/Model.js"));
const Inference = lazy(() => import("../views/ui/Inference.js"));

// export default ThemeRoutes;
const ThemeRoutes = [
  {
    path: "/",
    element: <Login />,
  },
  {
    path: "/home",
    element: (
      <AuthProvider>
        {/* <PrivateRouter> */}
        <FullLayout />
        {/* </PrivateRouter> */}
      </AuthProvider>
    ),
    children: [
      { path: "/home", element: <Navigate to="/home/datasets" /> },
      { path: "/home/inference", element: <Inference /> },
      { path: "/home/model", element: <Model /> },
      { path: "/home/table", exact: true, element: <Tables /> },
      { path: "/home/datasets", element: <Datasets /> },
    ],
  },

  // {
  //   path: "*",
  //   element: <Login />,
  // },
];

export default ThemeRoutes;
