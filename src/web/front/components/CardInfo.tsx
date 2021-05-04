import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles({
  root: {
    position: "fixed",
    height: "80%",
    width: "50%",
    left: "50%",
    maxHeight: 500,
    top: "50%",
    transform: "translate(-50%, -50%)",
    zIndex: 99999,
  },
  media: {
    height: 300,
  },
  buttons: {},
});

const CardInfo = (props) => {
  const classes = useStyles();
  return (
    <Card className={classes.root}>
      <CardActionArea>
        <CardMedia
          className={classes.media}
          image={props.img}
          title={props.store}
        />
        <CardContent>
          <Typography gutterBottom variant="h3" component="h2">
            {props.store}
          </Typography>
          <Typography variant="h5" color="textSecondary" component="p">
            {props.msg}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions className={classes.buttons}>
        <Button size="large" color="primary">
          <Typography variant="h6">View example dashboard</Typography>
        </Button>
        <Button
          size="large"
          color="primary"
          onClick={() => props.setIsCardOpened(false)}
        >
          <Typography variant="h6">Close</Typography>
        </Button>
      </CardActions>
    </Card>
  );
};

export default CardInfo;
