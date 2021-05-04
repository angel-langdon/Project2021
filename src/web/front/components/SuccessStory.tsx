import { useState } from "react";
import CardInfo from "@/components/CardInfo";

interface IProps {
  store: string;
  img: string;
  msg: string;
}

const SuccessStory = (props: IProps) => {
  const [isCardOpened, setIsCardOpened] = useState<boolean>(false);
  const openCard = () => {
    setIsCardOpened(true);
  };
  return (
    <div>
      {/*if the card is opened show the card, else don't show anything*/}
      {isCardOpened ? (
        <CardInfo {...props} setIsCardOpened={setIsCardOpened} />
      ) : null}
      <div className="col-xs-12 col-sm-6 col-md-3 project-box-holder">
        <div className="project-box" onClick={() => openCard()}>
          <img className="project-img" src={props.img} />
          <div className="box-overlay">
            <h4>{props.store}</h4>
          </div>
        </div>
      </div>
    </div>
  );
};
export default SuccessStory;
