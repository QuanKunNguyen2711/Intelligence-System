import Themeroutes from "./routes/RouterDummy";
import { AuthProvider, useAuth } from "./Provider/AuthProvider";
import { BrowserRouter as Router, Routes, Route, Navigate, useRoutes } from 'react-router-dom';
import Login from "./views/ui/Login";
import FullLayout from "./layouts/FullLayout";
import Datasets from "./views/ui/Datasets";
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
  // const {user} = useAuth(false);
  // let token = window.localStorage.getItem('access_token');
  // const PrivateRoute = ({ element, ...rest }) => {
  //   return token ? (
  //     <Route {...rest} element={element} />
  //   ) : (
  //     <Navigate to="/login" replace />
  //   );
  // };

  // return (
  //   <Router>
  //     <Routes>
  //       <Route path="/login" element={<Login />} />
  //       <PrivateRoute path="/" element={<FullLayout />} />
  //       <PrivateRoute path="datasets" element={<Datasets />} />
  //     </Routes>
  //   </Router>
  // );

  const routing = useRoutes(Themeroutes);

  return <div className="dark">{routing}</div>;
};

export default App;
