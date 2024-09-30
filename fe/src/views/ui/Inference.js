import {
  Card,
  Row,
  Col,
  CardTitle,
  CardBody,
  Button,
  Form,
  FormGroup,
  Label,
  Input,
  FormText,
  CardHeader,
} from "reactstrap";
import { styled } from "@mui/material/styles";
// import * as React from "react";
import React, { useState, useEffect } from "react";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import ListItemText from "@mui/material/ListItemText";
import Select from "@mui/material/Select";
import Checkbox from "@mui/material/Checkbox";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import axios from "axios"; // Import Axios
import ProjectTables from "../../components/dashboard/ProjectTable";
import { ToastContainer, toast } from "react-toastify";
import { useAuth } from "../../Provider/AuthProvider";
import { axiosInstance } from "../../axios/AxiosClient";
import HistogramChart from "./HistogramChart";
import PreprocessedTable from "./PreprocessedTable";
import { CountertopsTwoTone } from "@mui/icons-material";
import ModelTrain from "./TrainingEpoch";
import { CardContent, Grid, Typography } from "@mui/material";
import EvaluationMetrics from "./EvaluationMetrics";
import HeatMapChart from "./HeatMapChart";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const Inference = () => {
  const [text, setText] = useState("");
  const [score, setScore] = useState();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setText(value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      // Example API endpoint
      axiosInstance.post("/infer", { text: text }).then((res) => {
        toast.success(`Sentiment Evaluation: ${res.data.score}`, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: false,
          draggable: true,
          progress: undefined,
          theme: "light",
        });
        setScore(res.data.score);
      });
      // Handle response data as needed
    } catch (error) {
      console.error("API Error:", error);
    }
  };

  return (
    <>
      <Row>
        <Col xs={12}>
          <Card>
            <CardTitle tag="h6" className="border-bottom p-3 mb-0">
              <i className="bi bi-bell me-2"> </i>
              Score Sentiment
            </CardTitle>
            <CardBody>
              <Form onSubmit={handleSubmit}>
                <FormGroup>
                  <Label for="description">Review Texts</Label>
                  <Input
                    id="description"
                    name="description"
                    placeholder="Input your reviews"
                    type="textarea"
                    rows={6}
                    onChange={handleChange}
                  />
                </FormGroup>
                <Typography variant="body1" gutterBottom>
                  I apologize for not being able to implement all system
                  functionalities for the customers, including features like
                  viewing hotels, booking vacation dates, and submitting
                  post-visit feedback, for the hotel owner, including the
                  management of the booking history and customer feedback. My
                  expertise primarily lies in backend and AI development, and
                  and I struggle with UI/UX design and frontend code. Despite my
                  best efforts, I've faced difficulties in these areas. I hope
                  you understand the level of dedication I've put into this
                  project, sir.
                </Typography>
                <Grid item container sx={{width: '200px', marginBottom: 2, marginTop: 2}}>
                  <Grid item xs={3}>
                    <Typography
                      sx={{ fontWeight: "bold"}}
                      color={"black"}
                    >
                      Score
                    </Typography>
                  </Grid>
                  <Grid item xs={9}>
                    <Typography color={"black"}>
                      {score !== null ? score : ""}
                    </Typography>
                  </Grid>
                </Grid>

                <Button type="submit">Submit</Button>
              </Form>
            </CardBody>
          </Card>
        </Col>
      </Row>
      <ToastContainer />
    </>
  );
};

export default Inference;
