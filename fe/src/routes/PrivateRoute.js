// // PrivateRouter.js
// import React, { useEffect } from "react";
import { Navigate, Outlet, Route } from "react-router-dom";
import { useAuth } from "../Provider/AuthProvider";

const PrivateRouter = () => {
  const { user } = useAuth();
  console.log(user);
  if (!user) {
    // If the user is not authenticated, redirect to the login page
    return <Navigate to="/login" />;
  }

  // If the user is authenticated, render the requested component
  return <Outlet />;
};

export default PrivateRouter;

// export const PrivateRouter = ({ children, ...rest }) => {
//   const { user } = useAuth(); // Get the authentication status from the context
//     console.log(user)
//   // If the user is logged in, render the children, otherwise, redirect to login
//   return user ? (
//     <Route {...rest}>{children}</Route>
//   ) : (
//     <Navigate to="/login" />
//   );
// };