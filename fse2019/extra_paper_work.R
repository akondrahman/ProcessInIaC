cat("\014") 
options(max.print=1000000)
t1 <- Sys.time()
library(ggplot2)
library(likert)

THE_FILE <- "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/extra-work/ALL_RAW_DEVS.csv"
CDF_COL  <- 8

# THE_FILE <- "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/extra-work/ALL_DEVS.csv"

# THE_FILE <- "/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/output/FSE2019/extra-work/devs-cutoff-minmax.csv"

THE_DAT  <- read.csv(THE_FILE)
print(head(THE_DAT))


#pdf('/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/writing/devs-perc.pdf', width=10, height=3)
	

# cdf_plt <- ggplot(THE_DAT, aes(DeveloperCount, colour=Dataset)) + stat_ecdf(geom = "step")  + labs(x='Developer count', y='Defective script (%)')
# cdf_plt <- cdf_plt + theme(plot.title = element_text(hjust = 0.5), text = element_text(size=12.5), axis.text=element_text(size=12.5))
# cdf_plt <- cdf_plt + theme(legend.position="bottom")
# cdf_plt <- cdf_plt + scale_x_continuous(limits=c(1, 30), breaks=c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 30) ) 
# 
# cdf_plt 

# line_plot <- ggplot()  + geom_line(aes(y = Perc, x = DeveloperCount, colour = Dataset), data = THE_DAT, stat="identity") 
# line_plot <- line_plot + scale_x_continuous(breaks=seq(1, 43, 1))
# line_plot <- line_plot + labs(x='Developer count', y='Defective script (%)')
# line_plot <- line_plot + scale_y_continuous(breaks=seq(1, 60, 9))
# line_plot <- line_plot + theme(legend.position="bottom")
# line_plot <- line_plot + theme( text = element_text(size=11), axis.text=element_text(size=11))
# line_plot

# pdf('/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/writing/devs-max-max.pdf', width=10, height=2.5)
# # reff: https://stackoverflow.com/questions/9968976/group-by-two-columns-in-ggplot2
# line_plot <- ggplot(data=THE_DAT, aes(x=x, y=y, group=interaction(type, dataset)))  + geom_line(aes(linetype=type)) + geom_point(aes(color=type), size = 3) 
# line_plot <- line_plot + scale_x_continuous(breaks=seq(1, 45, 5))
# line_plot <- line_plot + labs(x='Developer count')
# line_plot <- line_plot + theme_classic()
# line_plot <- line_plot + theme(legend.position="bottom")
# line_plot <- line_plot + theme( text = element_text(size=18), axis.text=element_text(size=18))
# line_plot <- line_plot + theme( axis.line.y  = element_blank(), axis.title.y = element_blank() , axis.ticks.y = element_blank(), axis.text.y=element_blank() ) 
# line_plot <- line_plot + geom_vline(xintercept = 12, linetype="twodash", color = "magenta", size=0.5) #reff: http://www.sthda.com/english/wiki/ggplot2-add-straight-lines-to-a-plot-horizontal-vertical-and-regression-lines
# line_plot
# 
# 
# 
# dev.off()

#pdf('/Users/akond/Documents/AkondOneDrive/OneDrive/ProcessInIaC/writing/devs-max-max.pdf', width=10, height=2.5)

the_plot <- ggplot(THE_DAT, aes(x=Type, y=Count, group=interaction(Type, Dataset))) + geom_boxplot(aes(fill=Type), width=0.3, outlier.shape=15, outlier.size=1) 
the_plot <- the_plot + theme_classic()
the_plot <- the_plot + theme(legend.position="bottom")
the_plot <- the_plot + labs(y='Developer count') 
the_plot <- the_plot + scale_y_continuous(breaks=seq(1, 45, 3))
the_plot <- the_plot + coord_flip() + theme(axis.title.y = element_blank())

the_plot



#dev.off()

t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))