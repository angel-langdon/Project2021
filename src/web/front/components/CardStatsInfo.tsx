import React from "react";

const CardStatsInfo = (props) => {
  return (
    <div
      style={{
        position: "fixed",
        flexDirection: "column",
        justifyContent: "space-between",
        height: "80%",
        width: "50%",
        left: "50%",
        maxHeight: 500,
        top: "50%",
        padding: "20px",
        backgroundColor: "#FFF",
        borderRadius: 10,
        transform: "translate(-50%, -50%)",
        display: props.visibility,
        zIndex: 99999,
      }}
    >
      <div>
        <h4>{props.indicator}</h4>
        <h6>{props.textInfo}</h6>
        <h5>{props.example}</h5>
      </div>
      <button
        type="button"
        className="btn btn-danger"
        onClick={() => props.setVisibility("none")}
      >
        CLOSE
      </button>
    </div>
  );
};

export default CardStatsInfo;
