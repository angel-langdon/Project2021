import dynamic from "next/dynamic";
import KPIsTop from "@/components/dashboard/KPIsTop";
import DefaultHeader from "@/components/DefaultHeader";
import { useState } from "react";
import React from "react";
import { makeStyles, Theme } from "@material-ui/core/styles";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import KPIsPlotVisits from "./KPIsPlotVisits";
import TabPanel from "@material-ui/lab/TabPanel";
import { AppBar } from "@material-ui/core";
const LinePlotVisits = dynamic(
  () => import("@/components/dashboard/LinePlotVisits"),
  { ssr: false }
);
// ? for optional parameters
interface IProps {
  store: string;
  data: Array<any>;
  filteredData?: object;
  placekey?: string;
}
const DashboardTabs = () => {
  const useStyles = makeStyles({
    root: {
      flexGrow: 1,
      maxWidth: 500,
    },
  });
  const [value, setValue] = React.useState(0);
  const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setValue(newValue);
  };
  const classes = useStyles();
  return (
    <div className={classes.root}>
      <AppBar position="static" color="default">
        <Tabs
          value={value}
          onChange={handleChange}
          indicatorColor="primary"
          textColor="primary"
          variant="scrollable"
          scrollButtons="auto"
          aria-label="scrollable auto tabs example"
        >
          <Tab label="Item One" />
          <Tab label="Item Two" />
          <Tab label="Item Three" />
          <Tab label="Item Four" />
          <Tab label="Item Five" />
          <Tab label="Item Six" />
          <Tab label="Item Seven" />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        Item One
      </TabPanel>
      <TabPanel value={value} index={1}>
        Item Two
      </TabPanel>
    </div>
  );
};

const Dashboard = (props: IProps) => {
  // By default we pick the first place key
  const [placekey, setPlacekey] = useState<string>(props.data[0]["placekey"]);
  const [filteredData, setFilteredData] = useState<Array<object>>(
    props.data.filter((object) => object.placekey == placekey)
  );
  props = { ...props, filteredData: filteredData, placekey: placekey };
  return (
    <div className="dashboard-container">
      <DefaultHeader />
      <DashboardTabs />
      <div className="row horizontal-kpis-container">
        <KPIsTop {...props} />
      </div>
      <div className="row">
        <div className="col-10">
          <LinePlotVisits {...props} />
        </div>
        <div className="col">
          <KPIsPlotVisits {...props} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
