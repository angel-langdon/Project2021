path = '/Users/mazcu/Projects/Project2021/src/objectives/Visitors prediction/test.csv'
library(ggplot2)
df = read.csv(path)

stores = unique(df$safegraph_place_id)

for (store in stores){
  df_ = df[df$safegraph_place_id == store, ]
  plot(df_$visits, type='l')
  Sys.sleep(5)
}

