
import FullLayout from "../layouts/FullLayout";
import Cards from "../views/ui/Cards";
import Tables from "../views/ui/Tables";
import Datasets from "../views/ui/Datasets";
import { Navigate } from "react-router-dom";
// export const ChildrenRootRoutes = [{ path: 'users', element: <RootPage />, index: true }];

export const ChildrenHotelOwnerRoutes = [
    {
        path: "/",
        element: <FullLayout />,
        children: [
          {path: '/', element: <Navigate to="/datasets" />},
          { path: "/cards", exact: true, element: <Cards /> },
          { path: "/table", exact: true, element: <Tables /> },
          { path: "/datasets", exact: true, element: <Datasets /> },
        ],
      },
];

// export const ChildrenUserRoutes = [
//   { path: 'dashboard', element: <DashboardAppPage />, index: true },
//   { path: 'users', element: <UserPage /> },
//   { path: 'products', element: <ProductsPage /> },
//   { path: 'blogs', element: <BlogPage /> },
// ];
