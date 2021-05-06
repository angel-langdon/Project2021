import SuccessStory from "@/components/SuccessStory";
const SuccessStoriesList = () => {
  return (
    <div>
      <SuccessStory
        store="Subway"
        img="/images/subway-card.jpg"
        dashboardUrl="/dashboard-example-subway"
        msg="Subway is very good company that does sandwiches for hungry and hurried people.
                       We built a predictive model that was able to predict the number of visitors"
      />
      <SuccessStory
        store="Starbucks"
        img="/images/starbucks-card.jpeg"
        msg="Starbucks is a hipster place, we all know...  With our model we were able to predict the number of visitors pretty good"
        dashboardUrl="#"
      />
    </div>
  );
};
export default SuccessStoriesList;
