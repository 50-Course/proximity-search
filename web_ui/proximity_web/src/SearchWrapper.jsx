import React, { useState } from "react";
import {
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import axios from "axios";

function App() {
  const [location, setLocation] = useState("");
  const [filters, setFilters] = useState([]);
  const [result, setResult] = useState(null);

  const handleSearch = async () => {
    try {
      const response = await axios.post("backendUrl", { location, filters });
      setResult(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <TextField
        label="Location"
        variant="outlined"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        style={{ marginRight: "10px" }}
      />
      <FormControl
        variant="outlined"
        style={{ minWidth: "150px", marginRight: "10px" }}
      >
        <InputLabel>Filters</InputLabel>
        <Select
          multiple
          value={filters}
          onChange={(e) => setFilters(e.target.value)}
          label="Filters"
          MenuProps={{
            PaperProps: {
              style: {
                maxHeight: 224,
                width: 250,
              },
            },
          }}
        >
          <MenuItem value="filter1">Filter 1</MenuItem>
          <MenuItem value="filter2">Filter 2</MenuItem>
          <MenuItem value="filter3">Filter 3</MenuItem>
        </Select>
      </FormControl>
      <Button variant="contained" color="primary" onClick={handleSearch}>
        Search
      </Button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          {/* Render result on Maplibre map */}
          {/* Replace this with your Maplibre map component */}
          <div
            id="map"
            style={{
              width: "100%",
              height: "400px",
              border: "1px solid black",
            }}
          >
            {/* Render your map here */}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
