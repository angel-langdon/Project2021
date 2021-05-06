import RoundedRectangleContainer from "./RoundedRectangleContanier";
interface IProps {
  number: number;
  unit: string;
  description: string;
  className: string;
}
const KPI = (props: IProps) => {
  const kpi = (
    <div className={props.className}>
      <h4 className="text-primary">
        {props.number.toString() + " " + props.unit}
      </h4>
      <small className="text-muted">{props.description}</small>
    </div>
  );
  return (
    <RoundedRectangleContainer className={props.className} element={kpi} />
  );
};
export default KPI;
