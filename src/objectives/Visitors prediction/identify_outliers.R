path = '/Users/mazcu/Projects/Project2021/src/objectives/Visitors prediction/starbucks.csv'
library(ggplot2)
df = read.csv(path)

stores = unique(df$safegraph_place_id)
for (store in stores){
  df_ = df[df$safegraph_place_id == store, ]
  plot(df_$visits, type='l')
  Sys.sleep(5)
}

path = '/Users/mazcu/Projects/Project2021/src/objectives/Visitors prediction/starbucks.csv'
library(ggplot2)
df = read.csv(path)
df_ = df[df$safegraph_place_id == 'sg:b1ba9c1947974b5597eab48611826512', ]
plot(df_$visits, type='l')

path = '/Users/mazcu/Projects/Project2021/src/objectives/Visitors prediction/testing.csv'
library(ggplot2)
df__ = read.csv(path)

plot(df__$new, type='l')
