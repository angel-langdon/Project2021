const RoundedRectangleContainer = (props) => {
  return (
    <div className={props.className + " rounded-rectangle-container"}>
      {props.element}
    </div>
  );
};
export default RoundedRectangleContainer;
