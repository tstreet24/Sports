library(tidyverse)
library(readxl)
library(ggplot2)
library(ggsci)
library(cowplot)
library(reshape2)
library(viridis)
################################################################################
setwd("~/Documents/MIT/15.285_Sports_Analytics/Sports")
################################################################################
### Judge IDs
ids <- read_csv("unique_judges.csv")
names(ids) <- c("ID", "Judge Name")

media_df <- data.frame(ID=-1,
                       Judge_Name="Media")
names(media_df) <- c("ID", "Judge Name")

ids <- rbind(ids, media_df)
rm(media_df)

### average_agreements.csv -> judge agreement with fight outcome
agreements <- read_csv("average_agreements.csv")
agreements <- agreements[, -1]
agreements <- merge(x=ids %>% filter(`Judge Name` != "Media"),
                    y=agreements,
                    on="Judge Name")

### average_agreements_media.csv -> judge agreement with media
media_agreements <- read_csv("average_agreements_media.csv")
media_agreements <- media_agreements[, -1]
media_agreements <- merge(x=ids %>% filter(`Judge Name` != "Media"),
                          y=media_agreements,
                          on="Judge Name")

### analysis.csv -> table of statistics of fights (w/ cluster numbers)
analysis <- read_csv("analysis.csv")
analysis <- analysis[, -1]

### judges_stats_per_cluster.csv -> judge agreement stats per cluster
judge_stats <- read_csv("judges_stats_per_cluster.csv")
judge_stats <- judge_stats[, -1]
judge_stats <- merge(x=ids,
                     y=judge_stats,
                     by.x="Judge Name",
                     by.y="Judge")
################################################################################
### Number of Fights by Cluster
ggplot(data=analysis %>% mutate(Cluster = Cluster+1), aes(x=as.factor(Cluster), group=as.factor(Cluster), fill=as.factor(reorder(Cluster, desc(Cluster))))) +
    geom_bar(fill="blue") +
    labs(x="Cluster",
         y="# of Fights",
         fill="Cluster",
         title="Number of Split-Decision Fights per Cluster",
         subtitle="Professional Judges") +
    theme_classic() +
    theme(legend.position="none")
ggsave(filename="professional_judge_votes_histogram.png", path="figures")

### Graph for % Agreement of Outcome by Judge
agreements_plot <- agreements %>%
    filter(Count >= 5)
ggplot(data=agreements_plot, aes(x=as.factor(reorder(ID, desc(Average_Agreement))), y=Average_Agreement, fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Average Rate with Outcome",
         title="Agreement Rate with Outcome by Judge",
         subtitle="For Judges with at least 5 fights") +
    ylim(0, 1)
ggsave(filename="agreement_rate_by_judge_outcome_all_clusters.png", path="figures")

### Graph for % Agreement of Media by Judge
media_agreements_plot <- media_agreements %>%
    filter(Count >= 5)
ggplot(data=media_agreements_plot, aes(x=as.factor(reorder(ID, desc(Average_Agreement))), y=Average_Agreement, fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Average Rate with Media Decision",
         title="Agreement Rate with Media Decision by Judge",
         subtitle="For Judges with at least 5 fights") +
    ylim(0, 1)
ggsave(filename="agreement_rate_by_judge_media_all_clusters.png", path="figures")

### Graph for % Agreement of Outcome by Judge, by Cluster
# Cluster 1
ggplot(data=judge_stats %>%
           filter(Cluster_0_Prop != -1) %>%
           mutate(Cluster_0_Prop = ifelse(Cluster_0_Prop == 0, 0.005, Cluster_0_Prop)),
       aes(x=as.factor(reorder(ID, desc(Cluster_0_Prop))),
           y=Cluster_0_Prop,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Outcome",
         title="Agreement Rates with Outcome for Cluster 1 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 1")
ggsave(filename="agreement_rate_by_judge_outcome_cluster_1.png", path="figures")

# Cluster 2
ggplot(data=judge_stats %>%
            filter(Cluster_1_Prop != -1) %>%
            mutate(Cluster_1_Prop = ifelse(Cluster_1_Prop == 0, 0.005, Cluster_1_Prop)),
       aes(x=as.factor(reorder(ID, desc(Cluster_1_Prop))),
           y=Cluster_1_Prop,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Outcome",
         title="Agreement Rates with Outcome for Cluster 2 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 2")
ggsave(filename="agreement_rate_by_judge_outcome_cluster_2.png", path="figures")

# Cluster 3
ggplot(data=judge_stats %>%
           filter(Cluster_2_Prop != -1) %>%
           mutate(Cluster_2_Prop = ifelse(Cluster_2_Prop == 0, 0.005, Cluster_2_Prop)),
       aes(x=as.factor(reorder(ID, desc(Cluster_2_Prop))),
           y=Cluster_2_Prop,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Outcome",
         title="Agreement Rates with Outcome for Cluster 3 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 3")
ggsave(filename="agreement_rate_by_judge_outcome_cluster_3.png", path="figures")

# Cluster 4
ggplot(data=judge_stats %>%
           filter(Cluster_3_Prop != -1) %>%
           mutate(Cluster_3_Prop = ifelse(Cluster_3_Prop == 0, 0.005, Cluster_3_Prop)),
       aes(x=as.factor(reorder(ID, desc(Cluster_3_Prop))),
           y=Cluster_3_Prop,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Outcome",
         title="Agreement Rates with Outcome for Cluster 4 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 4")
ggsave(filename="agreement_rate_by_judge_outcome_cluster_4.png", path="figures")

# Cluster 5
ggplot(data=judge_stats %>%
           filter(Cluster_4_Prop != -1) %>%
           mutate(Cluster_4_Prop = ifelse(Cluster_4_Prop == 0, 0.005, Cluster_4_Prop)),
       aes(x=as.factor(reorder(ID, desc(Cluster_4_Prop))),
           y=Cluster_4_Prop,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Outcome",
         title="Agreement Rates with Outcome for Cluster 5 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 5")
ggsave(filename="agreement_rate_by_judge_outcome_cluster_5.png", path="figures")

# Cluster 6
ggplot(data=judge_stats %>%
           filter(Cluster_5_Prop != -1) %>%
           mutate(Cluster_5_Prop = ifelse(Cluster_5_Prop == 0, 0.005, Cluster_5_Prop)),
       aes(x=as.factor(reorder(ID, desc(Cluster_5_Prop))),
           y=Cluster_5_Prop,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Outcome",
         title="Agreement Rates with Outcome for Cluster 6 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 6")
ggsave(filename="agreement_rate_by_judge_outcome_cluster_6.png", path="figures")

### Graph for % Agreement of Media by Judge, by Cluster
# Cluster 1
ggplot(data=judge_stats %>%
           filter(Cluster_0_Prop_media != -1) %>%
           mutate(Cluster_0_Prop_media = ifelse(Cluster_0_Prop_media == 0, 0.005, Cluster_0_Prop_media)),
       aes(x=as.factor(reorder(ID, desc(Cluster_0_Prop_media))),
           y=Cluster_0_Prop_media,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Media Decision",
         title="Agreement Rates with Media Decision for Cluster 1 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 1")
ggsave(filename="agreement_rate_by_judge_media_cluster_1.png", path="figures")

# Cluster 2
ggplot(data=judge_stats %>%
           filter(Cluster_1_Prop_media != -1) %>%
           mutate(Cluster_1_Prop_media = ifelse(Cluster_1_Prop_media == 0, 0.005, Cluster_1_Prop_media)),
       aes(x=as.factor(reorder(ID, desc(Cluster_1_Prop_media))),
           y=Cluster_1_Prop_media,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Media Decision",
         title="Agreement Rates with Media Decision for Cluster 2 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 2")
ggsave(filename="agreement_rate_by_judge_media_cluster_2.png", path="figures")

# Cluster 3
ggplot(data=judge_stats %>%
           filter(Cluster_2_Prop_media != -1) %>%
           mutate(Cluster_2_Prop_media = ifelse(Cluster_2_Prop_media == 0, 0.005, Cluster_2_Prop_media)),
       aes(x=as.factor(reorder(ID, desc(Cluster_2_Prop_media))),
           y=Cluster_2_Prop_media,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Media Decision",
         title="Agreement Rates with Media Decision for Cluster 3 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 3")
ggsave(filename="agreement_rate_by_judge_media_cluster_3.png", path="figures")

# Cluster 4
ggplot(data=judge_stats %>%
           filter(Cluster_3_Prop_media != -1) %>%
           mutate(Cluster_3_Prop_media = ifelse(Cluster_3_Prop_media == 0, 0.005, Cluster_3_Prop_media)),
       aes(x=as.factor(reorder(ID, desc(Cluster_3_Prop_media))),
           y=Cluster_3_Prop_media,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Media Decision",
         title="Agreement Rates with Media Decision for Cluster 4 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 4")
ggsave(filename="agreement_rate_by_judge_media_cluster_4.png", path="figures")

# Cluster 5
ggplot(data=judge_stats %>%
           filter(Cluster_4_Prop_media != -1) %>%
           mutate(Cluster_4_Prop_media = ifelse(Cluster_4_Prop_media == 0, 0.005, Cluster_4_Prop_media)),
       aes(x=as.factor(reorder(ID, desc(Cluster_4_Prop_media))),
           y=Cluster_4_Prop_media,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Media Decision",
         title="Agreement Rates with Media Decision for Cluster 5 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 5")
ggsave(filename="agreement_rate_by_judge_media_cluster_5.png", path="figures")

# Cluster 6
ggplot(data=judge_stats %>%
           filter(Cluster_5_Prop_media != -1) %>%
           mutate(Cluster_5_Prop_media = ifelse(Cluster_5_Prop_media == 0, 0.005, Cluster_5_Prop_media)),
       aes(x=as.factor(reorder(ID, desc(Cluster_5_Prop_media))),
           y=Cluster_5_Prop_media,
           fill="Red")) +
    geom_col() +
    theme_classic() +
    theme(legend.position="none",
          axis.text.x=element_blank(),
          axis.ticks.x=element_blank()) +
    labs(x="Judge",
         y="Agreement Rate with Media Decision",
         title="Agreement Rates with Media Decision for Cluster 6 Fights",
         subtitle="For Judges with at least 1 fight in Cluster 6")
ggsave(filename="agreement_rate_by_judge_media_cluster_6.png", path="figures")

### Graph for % Agreement of Media, by Cluster
media_plot <- judge_stats %>%
    filter(`Judge Name` == "Media") %>%
    melt() %>%
    mutate(Cluster=if_else(grepl("_0_", variable, fixed=TRUE), 1,
                   if_else(grepl("_1_", variable, fixed=TRUE), 2,
                   if_else(grepl("_2_", variable, fixed=TRUE), 3,
                   if_else(grepl("_3_", variable, fixed=TRUE), 4,
                   if_else(grepl("_4_", variable, fixed=TRUE), 5,
                   if_else(grepl("_5_", variable, fixed=TRUE), 6, -1)))))),
           type=if_else(grepl("_Count", variable, fixed=TRUE), "Count",
                if_else(grepl("_Prop_media", variable, fixed=TRUE), "Prop_Media",
                if_else(grepl("_Prop", variable, fixed=TRUE), "Prop", "Other")))) %>%
    dcast(`Judge Name` + Cluster ~ type) %>%
    select(`Judge Name`, Cluster, Count, Prop) %>%
    filter(Cluster != -1)

# Count of Media Votes per Cluster
ggplot(data=media_plot,
       aes(x=as.factor(Cluster),
           y=Count,
           group=as.factor(Cluster),
           fill=as.factor(reorder(Cluster, desc(Cluster))))) +
    geom_col(fill="blue") +
    labs(x="Cluster",
         y="# of Fights",
         fill="Cluster",
         title="Number of Split-Decision Fights per Cluster",
         subtitle="Media Scoring") +
    theme_classic() +
    theme(legend.position="none")
ggsave(filename="media_votes_count_histogram.png", path="figures")

# Agreement Proportion of Media per Cluster
ggplot(data=media_plot,
       aes(x=as.factor(Cluster),
           y=Prop)) +
    geom_col(fill="blue") +
    labs(x="Cluster",
         y="Agreement Rate of Outcome",
         fill="Cluster",
         title="Agreement Rate with Outcome by Cluster",
         subtitle="Media Scoring") +
    theme_classic() +
    theme(legend.position="none")
ggsave(filename="media_votes_agreement_rates_histogram.png", path="figures")
################################################################################