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

const cols = ["title", "pos_rw", "neg_rw", "avg_score"];
const cols_remain = ["avg_score"];

const Datasets = () => {
  const { user } = useAuth();
  const [historamLabels, setHistoramLabels] = useState([]);
  const [listRecordProcessed, setListRecordProcessed] = useState({});
  const [headData, setHeadData] = useState([]);
  const [formData, setFormData] = useState({
    email: "",
    file: "",
    features: [],
    label: [], // Initialize remainingOptions
  });

  const [selectedFile, setSelectedFile] = useState("");
  const [labels, setLabels] = useState([]);
  const [counts, setCounts] = useState([]);
  // const [selectedFile, setSelectedFile] = React.useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFeatureSelect = (selectedFeatures) => {
    const remainingOptions = cols.filter(
      (option) => !selectedFeatures.includes(option)
    );
    setFormData((prevData) => ({
      ...prevData,
      features: selectedFeatures,
      // remainingOptions: remainingOptions, // Update remainingOptions
    }));
  };

  const handleLabelSelect = (selectedLabel) => {
    setFormData((prevData) => ({
      ...prevData,
      label: selectedLabel,
      // remainingOptions: remainingOptions, // Update remainingOptions
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formDataSend = new FormData();
    // formDataSend.append("file", formData["file"]);
    formDataSend.append("file", selectedFile);
    formDataSend.append(
      "mapping",
      JSON.stringify({
        features: formData["features"],
        label: formData["label"][0],
      })
    );
    try {
      // Example API endpoint
      toast.success(`Send preprocessing task successfully`, {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: false,
        draggable: true,
        progress: undefined,
        theme: "light",
      });
      axiosInstance.post("/preprocess-dataset", formDataSend).then((res) => {

        let labels = [];
        let counts = [];
        setHeadData(res.data.result);
        Object.entries(res.data.reduced_score).forEach(([label, count]) => {
          labels.push(label);
          counts.push(count);
        });
        setLabels(labels);
        setCounts(counts);
        setHistoramLabels(res.data.reduced_score);
        toast.success(`Dataset has been preprocessed successfully`, {
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
      // const apiUrl = "http://localhost:8000/api/preprocess-dataset";
      // const token = localStorage.getItem("access_token");
      // // Make POST request with Axios
      // const response = await axios.post(apiUrl, formDataSend, {
      //   headers: {
      //     Authorization: `Bearer ${token}`, // Include the token in the Authorization header
      //     "Content-Type": "multipart/form-data",
      //   },
      // });

      // Handle response data as needed
    } catch (error) {
      console.error("API Error:", error);
      // Handle errors
    }
  };


  const handleFileChange = (event) => {
    // Get the selected file from the input element
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  return (
    <>
      <Row>
        <Col>
          <Card>
            <CardTitle tag="h6" className="border-bottom p-3 mb-0">
              <i className="bi bi-bell me-2"> </i>
              Upload Datasets
            </CardTitle>
            <CardBody>
              <Form onSubmit={handleSubmit}>
                <FormGroup>
                  <Label for="exampleFile">File</Label>
                  <Input
                    id="exampleFile"
                    name="file"
                    type="file"
                    onChange={handleFileChange}
                  />
                  <FormText>Upload your own file's dataset</FormText>
                </FormGroup>
                <FormGroup>
                  <FormControl sx={{ m: 1, width: 300 }}>
                    <InputLabel id="demo-multiple-checkbox-label">
                      Features
                    </InputLabel>
                    <Select
                      labelId="demo-multiple-checkbox-label"
                      id="demo-multiple-checkbox"
                      multiple
                      value={formData.features}
                      onChange={(event) =>
                        handleFeatureSelect(event.target.value)
                      }
                      input={<OutlinedInput label="Features" />}
                      renderValue={(selected) => selected.join(", ")}
                      MenuProps={MenuProps}
                    >
                      {cols.map((name) => (
                        <MenuItem key={name} value={name}>
                          <Checkbox
                            checked={formData.features.includes(name)}
                          />
                          <ListItemText primary={name} />
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </FormGroup>
                <FormGroup>
                  <FormControl sx={{ m: 1, width: 300 }}>
                    <InputLabel id="demo-multiple-checkbox-label">
                      Label
                    </InputLabel>
                    <Select
                      labelId="demo-multiple-checkbox-label"
                      id="demo-multiple-checkbox-remaining"
                      multiple
                      value={formData.label} // Ensure it's an array
                      onChange={(event) =>
                        handleLabelSelect(event.target.value)
                      }
                      input={<OutlinedInput label="Label" />}
                      renderValue={(selected) => selected.join(", ")}
                      MenuProps={MenuProps}
                    >
                      {cols_remain.map((name) => (
                        <MenuItem key={name} value={name}>
                          <Checkbox checked={formData.label.includes(name)} />
                          <ListItemText primary={name} />
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </FormGroup>
                <Button type="submit">Submit</Button>
              </Form>
            </CardBody>
          </Card>
        </Col>
      </Row>
      <Row>
        <Col lg="12">{headData.length > 0 ? <PreprocessedTable data={headData}/> : null}</Col>
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
      </Row>

      <ToastContainer />
    </>
  );
};

export default Datasets;
