import React from "react";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";

export default function DashboardSearcher(props) {
  function changeStore(e, value) {
    const newPlacekey: string = value.placekey;
    props.setFilteredData(
      props.data.filter((object) => object.placekey == newPlacekey)
    );
  }
  return (
    <Autocomplete
      id="combo-box-demo"
      options={props.uniqueStores}
      getOptionLabel={(option: any) => option.street_address}
      style={{ width: 200, height: 50 }}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Search store"
          variant="outlined"
          style={{ backgroundColor: "#fff", fontSize: "16pt" }}
        />
      )}
      onChange={changeStore}
    />
  );
}
