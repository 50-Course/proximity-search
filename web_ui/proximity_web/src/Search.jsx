import React, { useState, useEffect } from "react";
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import InputAdornment from "@mui/material/InputAdornment";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";

const SearchBar = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const [filters, setFilters] = useState({
        minMembers: 0,
        maxMembers: Infinity,
        radius: 10,
        isPrivate: false,
    });

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleFilterChange = (event) => {
        setFilters({
            ...filters,
            [event.target.name]: event.target.checked,
        });
    };

    const handleSearch = () => {
        // Handle API call here with search term and filters
        console.log("Search term:", searchTerm);
        console.log("Filters:", filters);

        // For all filters selected, make an API call to the backend url
        // using axios, 
        // and pass the search term and array of filters as query parameters

        return (
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    backgroundColor: "white",
                }}
            >
                <TextField
                    id="outlined-basic"
                    label="Where?"
                    variant="outlined"
                    value={searchTerm}
                    onChange={handleSearchChange}
                    placeholder="Enter a town or city..."
                    fullWidth
                    InputProps={{
                        endAdornment: (
                            <InputAdornment position="end">
                                <IconButton onClick={handleSearch} edge="end" aria-label="search">
                                    <SearchIcon />
                                </IconButton>
                            </InputAdornment>
                        ),
                        style: {
                            backgroundColor: "white",
                            outline: "1px solid black",
                            color: "lightgray",
                        },
                    }}
                    InputLabelProps={{
                        style: {
                            color: "lightgray",
                        },
                    }}
                />
                <FormControl component="fieldset" style={{ marginLeft: "1rem" }}>
                    <FormLabel component="legend" style={{ color: "lightgray" }}>
                        Filters
                    </FormLabel>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={filters.minMembers > 0}
                                onChange={handleFilterChange}
                                name="minMembers"
                                value={1000}
                            />
                        }
                        label="Members Count > 1000"
                        style={{ color: "lightgray" }}
                    />
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={filters.maxMembers < 1000}
                                onChange={handleFilterChange}
                                name="maxMembers"
                                value={1000}
                            />
                        }
                        label="Members Count < 1000"
                        style={{ color: "lightgray" }}
                    />
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={filters.isPrivate}
                                onChange={handleFilterChange}
                                name="isPrivate"
                            />
                        }
                        label="Private Groups"
                        style={{ color: "lightgray" }}
                    />
                </FormControl>
            </div>
        );
    };

    export default SearchBar;
