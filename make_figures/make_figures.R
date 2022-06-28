################################################################################### DATA
library(stringr)
library(htmlwidgets)
library(ggplot2)
library(forcats)
library(plyr)

df <- read.table(file = "betas_evals.tsv", sep = '\t', header = TRUE)

grafi = list()
ime = c("r2", "MAE", "RMSE", "NRMSE", "Spearman cor", "Pearson cor", "Cosine sim")
k = 1

median_by = by(df$Value, df$Metric, median)
median_by = rbind(median_by)[1,]

for (i in unique(df$Metric)) {
  grafi[[k]] = ggplot(data = df[df$Metric == i,], aes(x = Metric, y = Value)) +
    geom_violin(aes(fill = fct_reorder(name, Value, median))) + theme_classic() + geom_boxplot(width=0.1) + 
    theme(axis.text.x = element_text(angle = 50, vjust = 1, hjust=1, size = 10),
          legend.key.size = unit(1, 'cm'),
          legend.text = element_text(size=10),
          legend.title = element_text(size = 14),
          plot.title = element_text(hjust = 0.5)) + scale_fill_discrete(name = paste("Model by median", ime[k])) +
    ylab(ime[k]) + xlab("Model") + ggtitle(ime[k]) + 
    geom_text(data = p_meds, aes(x = name, y = df_max$max, label = med), size = 4, angle = 90, hjust = -0.5) + ylim(0, 0.3)
  k = k+1
}

boxplot(df$Value[df$Metric == "cvrmse"])
grafi

###############################################################################

p_meds = p_meds[order(p_meds$med),][1:5,]
p_meds$med = round(p_meds$med, 4)
df2 = NULL
for (u in p_meds$name) {
  df2 = rbind(df2, df[df$name == u,])
}
i = "cvrmse"
df_max <- ddply(df2[df2$Metric == i,], .(name), summarise, max = max(Value))
k = 4
ggplot(data = df2[df2$Metric == i,], aes(x = fct_reorder(name, Value, median), y = Value, fill = name))  +
  geom_violin() +  scale_fill_brewer(palette="RdBu") + geom_boxplot(width=0.1, fill = "white")  +
  ylab(ime[k]) + xlab("Model") + ggtitle(ime[k]) + theme_minimal() +  
  theme(axis.text.x = element_text(size = 12, angle = 15, vjust = 0.8, hjust = 0.6), 
        plot.title = element_text(hjust = 0.5),
        legend.position = "none") + 
  geom_text(data = p_meds, aes(x = name, y = df_max$max, label = med), size = 4, angle = 90, hjust = -0.4) + ylim(0, 0.26) 


###############################################################################
df3 = cbind(df$Value[df$name == p_meds$name[1] & df$Metric == i], df$Value[df$name == p_meds$name[5] & df$Metric == i])
df3 = data.frame(df3)
head(df3)
names(df3) <- c("novi", "stari")
ggplot(data = df3, aes(x = novi, y = stari)) + geom_point(size = 1.2) + ylab(paste(p_meds$name[1], "NRMSE")) + xlab(paste(p_meds$name[5], "NRMSE")) + 
  geom_abline(intercept = 0, slope = 1, col = "red") + theme_minimal()


p_meds = p_meds[order(p_meds$med),]
p_meds$med = round(p_meds$med, 5)
p_meds


###############################################################################
library(stringr)
library(ggplot2)

#data import

df = NULL
k = 1
for (i in list.files()) {
  tmp = read.table(i, sep = '\t', header = TRUE)
  df = rbind(df, tmp)
}

# gene LASSO
# all graphs

k = 1
for (i in unique(df$Metric)) {
  fig[[k]] = ggplot(data = df[df$Metric == i,], aes(x = fct_reorder(HyperParameter, Value, median), y = Value)) + geom_violin() + theme_minimal() + labs(title = i)
  k = k + 1
}
fig

by(df$Value[df$Metric == "cvrmse"], df$HyperParameter[df$Metric == "cvrmse"], median)

# final graphs
# cosine similarity
i = "cosine"
ggplot(data = df[df$Metric == i,], aes(x = factor(HyperParameter), y = Value, fill = factor(HyperParameter))) + 
  geom_violin() + theme_minimal() + labs(title = "Podobnost kosinusa")  +  scale_fill_brewer(palette="RdBu")  + 
  theme(plot.title = element_text(hjust = 0.5), 
        legend.position = "none") + ylab("Podobnost kosinusa") + xlab("Hiperparameter") + geom_boxplot(width=0.12, fill = "white")

# RMSE

i = "rmse"
ggplot(data = df[df$Metric == i,], aes(x = factor(HyperParameter), y = Value, fill = factor(HyperParameter))) + 
  geom_violin() + theme_minimal() + labs(title = "RMSE")  +  scale_fill_brewer(palette="RdBu")  + 
  theme(plot.title = element_text(hjust = 0.5), 
        legend.position = "none") + ylab("RMSE") + xlab("Hiperparameter") + geom_boxplot(width=0.12, fill = "white")

################################## best

# cosine

i = "cosine"
ggplot(data = df[df$Metric == i,], aes(x = factor(Model), y = Value, fill = factor(Model))) + 
  geom_violin() + theme_minimal() + labs(title = "Podobnost kosinusa")  +  scale_fill_brewer(palette="RdBu")  + 
  theme(plot.title = element_text(hjust = 0.5), 
        legend.position = "none") + ylab("Podobnost kosinusa") + xlab("Hiperparameter") + geom_boxplot(width=0.12, fill = "white")

# RMSE

i = "rmse"
ggplot(data = df[df$Metric == i,], aes(x = factor(Model), y = Value, fill = factor(Model))) + 
  geom_violin() + theme_minimal() + labs(title = "RMSE")  +  scale_fill_brewer(palette="RdBu")  + 
  theme(plot.title = element_text(hjust = 0.5), 
        legend.position = "none") + ylab("RMSE") + xlab("Hiperparameter") + geom_boxplot(width=0.12, fill = "white")




