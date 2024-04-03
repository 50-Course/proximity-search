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

const BACKEND_URL = "http://localhost:8000";
const PROD_BACKEND_URL = "https://api.example.com";

function SearchWrapper({ onSearch }) {
  const [location, setLocation] = useState("");
  const [radius, setRadius] = useState("");
  const [customRadius, setCustomRadius] = useState("");
  const [useCustomRadius, setUseCustomRadius] = useState(false);

  const handleSearch = () => {
    const searchRadius = useCustomRadius ? customRadius : radius;
    onSearch({ location, radius: searchRadius });
  };

  return (
    <div
      style={{ display: "flex", alignItems: "center", marginBottom: "20px" }}
    >
      <div style={{ marginRight: "10px" }}>
        <TextField
          label="Where?"
          variant="outlined"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          style={{ width: "200px" }}
        />
      </div>
      <div style={{ marginRight: "10px" }}>
        <FormControl variant="outlined" style={{ minWidth: "120px" }}>
          <InputLabel>Radius</InputLabel>
          <Select
            value={useCustomRadius ? "custom" : radius}
            onChange={(e) => {
              const selectedValue = e.target.value;
              if (selectedValue === "custom") {
                setUseCustomRadius(true);
                setRadius("");
              } else {
                setUseCustomRadius(false);
                setRadius(selectedValue);
              }
            }}
            label="Radius"
          >
            <MenuItem value="10">10 miles</MenuItem>
            <MenuItem value="20">20 miles</MenuItem>
            <MenuItem value="50">50 miles</MenuItem>
            <MenuItem value="custom">Custom</MenuItem>
          </Select>
        </FormControl>
      </div>
      {useCustomRadius && (
        <TextField
          label="Custom Radius (miles)"
          variant="outlined"
          value={customRadius}
          onChange={(e) => setCustomRadius(e.target.value)}
          style={{ width: "120px", marginRight: "10px" }}
        />
      )}
      <Button variant="contained" color="primary" onClick={handleSearch}>
        Search
      </Button>
    </div>
  );
}

function App() {
  const [searchResults, setSearchResults] = useState(null);

  const handleSearch = async ({ location, radius }) => {
    try {
      const response = await axios.post(BACKEND_URL, { location, radius });
      setSearchResults(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignContent: "center",
        alignItems: "center",
        minHeight: "100vh",
      }}
    >
      <SearchWrapper onSearch={handleSearch} />

      {searchResults === null ? (
        <div>No results found</div>
      ) : (
        searchResults.map((result) => (
          <div key={result.id}>
            {/* Display each search result as a card */}
            <h3>{result.name}</h3>
            <p>{result.description}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default App;
