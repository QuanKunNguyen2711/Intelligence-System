import { Typography } from "@mui/material";
import { ReactComponent as LogoDark } from "../assets/images/logos/materialpro.svg";
import { Link } from "react-router-dom";

const Logo = () => {
  return (
    <Link to="/">
      <Typography variant="h4" sx={{ color: 'ghostwhite' }}>Travel Booking Agencies</Typography>
      {/* <LogoDark /> */}
    </Link>
  );
};

export default Logo;
