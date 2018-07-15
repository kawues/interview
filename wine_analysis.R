```{r echo=FALSE}
library(data.table)
library(ggplot2)

dataset <- read.csv('wines.csv', header = TRUE, sep = ';')
sorted_dataset <- dataset[ order(-dataset$quality, -dataset$alcohol), ]
cat("Sorted dataset, first 30 observations: ")
head(sorted_dataset,30)

observation_num = nrow(dataset)
cat("Observations number: ", observation_num)
variables_num = ncol(dataset)
cat("Variables number: ", variables_num)
complete_obs = nrow(dataset) - nrow(dataset[!complete.cases(dataset),])
cat("Number of complete observations: ", complete_obs)

white_count = sum(sorted_dataset$color == "white")
cat("Number of observations describing white wines: ", white_count)
red_count = sum(sorted_dataset$color == "red")
cat("Number of observations describing red wines: ", red_count)

varSummary <- function(var)
{
  cat(mean(var, na.rm =TRUE), sd(var, na.rm = TRUE), max(var,na.rm = TRUE)-min(var,na.rm = TRUE),"\n", sep = " ")
}

cat("Function 'varSummary' results for each column:")
for(i in dataset)
{
  if(is.numeric(i))
  {
    varSummary(i)
  }
}
sweetnes_types = dplyr::summarise(dplyr::group_by(dataset,dataset$sweetnes))
for(name in sweetnes_types$`dataset$sweetnes`)
{
  cat("Calling varSumary for sweetnes type: ", name, "\n")
  varSummary(dataset[dataset[, "sweetnes"] == name,]$quality)
}

cat("Number of wines in groups: ")
for(name in sweetnes_types$`dataset$sweetnes`)
{
  cat(name, ": ")
  cat(sum(dataset$sweetnes == name), "\n")
}

cat("Boxplot of quality for groupes of sweetness: ")
boxplot(dataset$residual.sugar~dataset$sweetnes,dataset)
hist(dataset$quality, main = "Quality histogram")
```{r echo=FALSE, message=FALSE, warning=FALSE}
ggplot(dataset,aes(x=dataset$quality))+geom_histogram()+facet_grid(~dataset$sweetnes)+theme_bw() +labs(title="Quality histogram grouped by sweetness")
ggplot(dataset, aes(dataset$quality)) +geom_density() +facet_grid(~dataset$sweetnes) +labs(title="Density function of quality grouped by sweetness")


corelation <- cor(dataset[sapply(dataset, is.numeric)], use = "complete.obs")
cat("Correlation for all pairs of variables in dataset:")
corelation

corr_format = setDT(melt(corelation))[Var1 != Var2][order(-value)]
most_corr_pairs = setDT(melt(corelation))[Var1 != Var2][order(-value)][c(1,3,5),]

cat("Plots for three most correlated pairs of variables: ")
plot(dataset[[most_corr_pairs[1]$Var1]],dataset[[most_corr_pairs[1]$Var2]], xlab = "total.sulfur.dioxide", ylab = "free.sulfur.dioxide")
plot(dataset[[most_corr_pairs[2]$Var1]],dataset[[most_corr_pairs[2]$Var2]], xlab= "density", ylab="residual.sugar")
plot(dataset[[most_corr_pairs[3]$Var1]],dataset[[most_corr_pairs[3]$Var2]], xlab = "total.sulfur.dioxide
", ylab="residual.sugar")
most_corr_with_quality = head(corr_format[corr_format$Var1 == "quality",],3)
cat("Most correlated with quality: ")
head(most_corr_with_quality,1)

cat("Plot of three variables that have strongest correlation with wine quality")
plot(dataset[[most_corr_with_quality[1]$Var2]],dataset[[most_corr_with_quality[2]$Var2]],xlab="x",ylab="y")
points(dataset[[most_corr_with_quality[1]$Var2]],dataset[[most_corr_with_quality[3]$Var2]])

