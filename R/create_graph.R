#!/usr/bin/env Rscript

balanced_token = data.frame(dataset = 'Balanced', type='Tokens', accuracy = scan('balanced_token.txt'))
balanced_pos = data.frame(dataset = 'Balanced', type='Part-of-speech tags', accuracy = scan('balanced_pos.txt'))
unbalanced_token = data.frame(dataset = 'Unbalanced', type='Tokens', accuracy = scan('unbalanced_token.txt'))
unbalanced_pos = data.frame(dataset = 'Unbalanced', type='Part-of-speech tags', accuracy = scan('unbalanced_pos.txt'))

data = rbind(balanced_token, balanced_pos, unbalanced_token, unbalanced_pos)

library(ggplot2)
ggplot(data, aes(x = dataset, y = accuracy, colour = type, fill = type)) +
    geom_boxplot() +
    labs(title="System F1-score", x = "Dataset", y = "F1-score") +
    scale_fill_manual(name="Features", values=c("darkorange", "darkolivegreen2")) +
    scale_colour_manual(name="Features", values=c("darkorange3", "darkolivegreen4")) +
    geom_hline(yintercept = 0.18) +
    geom_label(x = 2, y = 0.18, label = "Random (unbalanced)", vjust = -.2, colour="black", fill="gray90", show.legend=FALSE) +
    geom_hline(yintercept = 0.16666666666666666) +
    geom_label(x = 1, y = 0.16666666666666666, label = "Random (balanced)", vjust = 1.2, colour="black", fill="gray90", show.legend=FALSE) +
    theme(plot.background = element_rect(fill = "transparent"), legend.background = element_rect(fill = "transparent")) +
    scale_y_continuous(breaks = scales::pretty_breaks(n = 20))

