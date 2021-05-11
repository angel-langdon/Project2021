import SuccessStory from "@/components/SuccessStory";
const SuccessStoriesList = () => {
  return (
    <div>
      <SuccessStory
        store="Subway"
        img="/images/subway-card.jpg"
        dashboardUrl="/dashboard-example-subway"
        msg="Subway is a restaurant chain specializing in submarine sandwiches
                       We built a predictive model that was able to predict the daily number of visitors in a determined local."
      />
      <SuccessStory
        store="Starbucks"
        img="/images/starbucks-card.jpeg"
        msg="Starbucks Corp is a coffee roaster and retailer of specialty coffee with operations in approximately 82 markets around the world.  With our model we were able to predict the number of visitors pretty good."
        dashboardUrl="/dashboard-example-starbucks"
      />

      <SuccessStory
        store="Walmart"
        img="/images/walmart-card.jpg"
        msg="Walmart Inc. is an American multinational retail corporation that operates a chain of hypermarkets, discount department stores, and grocery stores from the United States."
        dashboardUrl="/dashboard-example-walmart"
      />

      <SuccessStory
        store="Old Navy"
        img="/images/oldnavy-card.jpeg"
        msg="Old Navy is an American clothing and accessories retailing company owned by American multinational corporation Gap Inc.."
        dashboardUrl="/dashboard-example-oldnavy"
      />
    </div>
  );
};
export default SuccessStoriesList;
