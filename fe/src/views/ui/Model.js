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
import { CardContent } from "@mui/material";
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

const Model = () => {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    hidden_size: "",
    batch_size: "",
    num_epochs: "",
  });
  const [epochs, setEpochs] = useState([]);
  const [evaluatioMetric, setEvaluationMetric] = useState({});
  const [confusionMatrix, setConfusionMatrix] = useState([]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  useEffect(() => {
    const token = window.localStorage.getItem("access_token");
    const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
    ws.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.event === 'training_epoch') {
        toast.success(
            `Epoch: ${msg.epoch}, Train_loss: ${msg.train_loss}, Val_loss: ${msg.val_loss}`,
            {
              position: "top-right",
              autoClose: 3000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: false,
              draggable: true,
              progress: undefined,
              theme: "light",
            }
          );
          setEpochs((prev) => [...prev, msg]);
      }
      else if (msg.event === 'evaluation_metric') {
        toast.success(
            `Evaluation Metrics - Precision: ${msg.precision}, Recall: ${msg.recall}, F1-Score: ${msg.f1_score}, Accuracy: ${msg.accuracy}.`,
            {
              position: "top-right",
              autoClose: 3000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: false,
              draggable: true,
              progress: undefined,
              theme: "light",
            }
          );
          setEvaluationMetric({precision: msg.precision, recall: msg.recall, f1_score: msg.f1_score, accuracy: msg.accuracy});
          setConfusionMatrix(msg.confusion_matrix)
      }
      else if (msg.event === 'early_stopping') {
        toast.success(
        `Event ${msg.event}: ${msg.early_stopping}`,
            {
              position: "top-right",
              autoClose: 3000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: false,
              draggable: true,
              progress: undefined,
              theme: "light",
            }
          );
      }
      
    };

    // Clean up WebSocket connection on component unmount
    return () => {
      ws.close();
    };
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    let sendData = {
      name: formData["name"],
      description: formData["description"],
      hidden_size: parseInt(formData["hidden_size"]),
      batch_size: parseInt(formData["batch_size"]),
      num_epochs: parseInt(formData["num_epochs"]),
    };

    try {
      // Example API endpoint
      axiosInstance.post("/train", sendData).then((res) => {
        toast.success(`${res.data.message}`, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: false,
          draggable: true,
          progress: undefined,
          theme: "light",
        });
      });
      // Handle response data as needed
    } catch (error) {
      console.error("API Error:", error);
      // Handle errors
    }
  };

  return (
    <>
      <Row>
        <Col xs={6}>
          <Card>
            <CardTitle tag="h6" className="border-bottom p-3 mb-0">
              <i className="bi bi-bell me-2"> </i>
              Model Configuration
            </CardTitle>
            <CardBody>
              <Form onSubmit={handleSubmit}>
                <FormGroup>
                  <Label for="name">Name</Label>
                  <Input
                    id="name"
                    name="name"
                    placeholder="Name"
                    type="text"
                    onChange={handleChange}
                  />
                </FormGroup>
                <FormGroup>
                  <Label for="description">Description</Label>
                  <Input
                    id="description"
                    name="description"
                    placeholder="Description"
                    type="textarea"
                    onChange={handleChange}
                  />
                </FormGroup>
                <FormGroup>
                  <Label for="hidden_size">Hidden Size</Label>
                  <Input
                    id="hidden_size"
                    name="hidden_size"
                    placeholder="64"
                    type="text"
                    onChange={handleChange}
                  />
                </FormGroup>
                <FormGroup>
                  <Label for="batch_size">Batch Size</Label>
                  <Input
                    id="batch_size"
                    name="batch_size"
                    placeholder="64"
                    type="text"
                    onChange={handleChange}
                  />
                </FormGroup>
                <FormGroup>
                  <Label for="num_epochs">Number of Epochs</Label>
                  <Input
                    id="num_epochs"
                    name="num_epochs"
                    placeholder="100"
                    type="text"
                    onChange={handleChange}
                  />
                </FormGroup>
                <Button type="submit">Submit</Button>
              </Form>
            </CardBody>
          </Card>
        </Col>
        <Col xs={6}>
          <Card sx={{ height: "523px", overflowY: "scroll", width: "100%" }}>
            <CardTitle tag="h6" className="border-bottom p-3 mb-0">
              <i className="bi bi-bell me-2"> </i>
              Training Epochs
            </CardTitle>
            <CardContent>
              {epochs.length > 0 ? <ModelTrain epochs={epochs} /> : null}
            </CardContent>
          </Card>
        </Col>
      </Row>
      <Row>
        <Col xs={6}>
          <Card sx={{ height: "600px", overflowY: "auto", width: "100%" }}>
            <CardTitle tag="h6" className="border-bottom p-3 mb-0">
              <i className="bi bi-bell me-2"> </i>
              Evaluation Metrics
            </CardTitle>
            <CardContent>
              {Object.keys(evaluatioMetric).length > 0 ? <EvaluationMetrics metrics={evaluatioMetric} /> : null}
            </CardContent>
          </Card>
        </Col>
        <Col xs={6}>
          <Card sx={{ height: "600px", overflowY: "auto", width: "100%" }}>
            <CardTitle tag="h6" className="border-bottom p-3 mb-0">
              <i className="bi bi-bell me-2"> </i>
              Heatmap
            </CardTitle>
            <CardContent>
              {confusionMatrix.length > 0 ? <HeatMapChart confusionMatrix={confusionMatrix} /> : null}
            </CardContent>
          </Card>
        </Col>
      </Row>

      {/* <Row>
        <Col lg="12">
          {headData.length > 0 ? <PreprocessedTable data={headData} /> : null}
        </Col>
      </Row>
      <Row>
        <Col lg="12">
          {labels.length > 0 ? (
            <HistogramChart
              title="Label Histogram"
              subheader=""
              chartLabels={labels}
              chartData={[
                {
                  name: "Team A",
                  type: "column",
                  fill: "solid",
                  data: counts,
                },
              ]}
              // chartData={listRecordProcessed["counts"]}
              type="new"
            />
          ) : null}
        </Col>
      </Row> */}

      <ToastContainer />
    </>
  );
};

export default Model;
