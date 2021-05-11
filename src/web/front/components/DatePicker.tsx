import TextField from "@material-ui/core/TextField";
import StaticDateRangePicker from "@material-ui/lab/StaticDateRangePicker";
import AdapterDateFns from "@material-ui/lab/AdapterDateFns";
import LocalizationProvider from "@material-ui/lab/LocalizationProvider";
import { makeStyles } from "@material-ui/core/styles";
import Box from "@material-ui/core/Box";
import { Fragment } from "react";

const useStyles = makeStyles({
  root: {
    minWidth: 200,
  },
});

const DatePicker = (props) => {
  function isDateNotInRange(date) {
    return !(date >= props.minMaxDates[0] && date <= props.minMaxDates[1]);
  }
  function changeDataDateRange(dates) {
    props.setDates(dates);
    if (dates[0] != undefined && dates[1] != undefined) {
      props.setFilteredData(
        props.data.filter(
          (object) =>
            object.placekey == props.placekey &&
            object.date >= dates[0] &&
            object.date <= dates[1]
        )
      );
    }
  }
  const classes = useStyles();

  return (
    <div className="d-flex" style={{ gridArea: "5/1/9/3" }}>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <StaticDateRangePicker
          className={classes.root}
          displayStaticWrapperAs="desktop"
          shouldDisableDate={isDateNotInRange}
          value={props.dates}
          onChange={(newValue) => {
            changeDataDateRange(newValue);
          }}
          calendars={1}
          renderInput={(startProps, endProps) => (
            <Fragment>
              <TextField {...startProps} variant="standard" />
              <Box sx={{ mx: 2 }}> to </Box>
              <TextField {...endProps} variant="standard" />
            </Fragment>
          )}
        />
      </LocalizationProvider>
    </div>
  );
};

export default DatePicker;
