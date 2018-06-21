#!/usr/bin/env Rscript

# This script will first check the normality of my data.
# It will then perform the appropiate test for each system, and create a
# Q-Q plot (using ggplot2) for all of the distributions.
# After these checks, it will perform the t-test that I discuss in my thesis.

library(methods)
library(ggplot2)
library(gridExtra)

# Load all data
balanced_token = data.frame(dataset = 'Balanced', type='Tokens', fscore = scan('balanced_token.txt'))
balanced_pos = data.frame(dataset = 'Balanced', type='Part-of-speech tags', fscore = scan('balanced_pos.txt'))
unbalanced_token = data.frame(dataset = 'Unbalanced', type='Tokens', fscore = scan('unbalanced_token.txt'))
unbalanced_pos = data.frame(dataset = 'Unbalanced', type='Part-of-speech tags', fscore = scan('unbalanced_pos.txt'))

balanced_book_token = data.frame(dataset = 'Balanced', type='Tokens', fscore = scan('books/balanced_token.txt'))
balanced_book_pos = data.frame(dataset = 'Balanced', type='Part-of-speech tags', fscore = scan('books/balanced_pos.txt'))

# Check normality & comparisons to the baselines
p1 = ggplot(balanced_token, aes(sample=fscore)) + stat_qq() + stat_qq_line() + ggtitle("Balanced token-based system")
shapiro_data<-(shapiro.test(balanced_token$fscore))
message(ifelse((shapiro_data$p.value<0.05), "Not normally distributed", "Normally distributed"))
t.test(balanced_token$fscore, mu=.1666666666666, alternative = 'greater')
lsr::cohensD(balanced_token$fscore, mu=.1666666666666)

p2 = ggplot(balanced_pos, aes(sample=fscore)) + stat_qq() + stat_qq_line() + ggtitle("Balanced POS-based system")
shapiro_data<-(shapiro.test(balanced_pos$fscore))
message(ifelse((shapiro_data$p.value<0.05), "Not normally distributed", "Normally distributed"))
t.test(balanced_pos$fscore, mu=.1666666666666, alternative = 'greater')
lsr::cohensD(balanced_pos$fscore, mu=.1666666666666)

p3 = ggplot(unbalanced_token, aes(sample=fscore)) + stat_qq() + stat_qq_line() + ggtitle("Unbalanced token-based system")
shapiro_data<-(shapiro.test(unbalanced_token$fscore))
message(ifelse((shapiro_data$p.value<0.05), "Not normally distributed", "Normally distributed"))
test = wilcox.test(unbalanced_token$fscore, mu=.18, alternative = 'greater')
test
Zstat<-qnorm(test$p.value/2)
abs(Zstat)/sqrt(10)

p4 = ggplot(unbalanced_pos, aes(sample=fscore)) + stat_qq() + stat_qq_line() + ggtitle("Unbalanced POS-based system")
shapiro_data<-(shapiro.test(unbalanced_pos$fscore))
message(ifelse((shapiro_data$p.value<0.05), "Not normally distributed", "Normally distributed"))
t.test(unbalanced_pos$fscore, mu=.18, alternative = 'greater')
lsr::cohensD(unbalanced_pos$fscore, mu=.18)

# Show Q-Q plots
grid.arrange(p1, p2, p3, p4, ncol=2)

# Compare in-of-genre results of balanced and unbalanced systems

t.test(balanced_token$fscore, balanced_pos$fscore, alternative="greater", paired=TRUE)
lsr::cohensD(balanced_token$fscore, balanced_pos$fscore)

wilcox.test(unbalanced_token$fscore, unbalanced_pos$fscore, alternative="greater", paired=TRUE)

# Compare out-of-genre results of balanced systems
ggplot(balanced_book_token, aes(sample=fscore)) + stat_qq() + stat_qq_line() + ggtitle("Balanced token-based system (books)")
shapiro_data<-(shapiro.test(balanced_book_token$fscore))
message(ifelse((shapiro_data$p.value<0.05), "Not normally distributed", "Normally distributed"))

ggplot(balanced_book_pos, aes(sample=fscore)) + stat_qq() + stat_qq_line() + ggtitle("Balanced POS-based system (books)")
shapiro_data<-(shapiro.test(balanced_book_pos$fscore))
message(ifelse((shapiro_data$p.value<0.05), "Not normally distributed", "Normally distributed"))

t.test(balanced_book_pos$fscore, balanced_book_token$fscore, alternative="greater", paired=TRUE)
