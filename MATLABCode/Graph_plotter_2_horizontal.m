%Code to plot the time distribution graph horizontally

%For the time distrbution graph
workbooktouse = scoringworkbookS1
means = workbooktouse{2,[2,3,4]}
errhigh = workbooktouse{3,[2,3,4]}
errlow= workbooktouse{3,[2,3,4]}
%categorical(scoringworkbookS2{4,[2,3,4]})
X = categorical({'T\_Stir','T\_Cook\_1','T\_Cook\_2'});
X = reordercats(X,{'T\_Cook\_2', 'T\_Cook\_1','T\_Stir'});
barh(X,means)
hold on

er = errorbar(means,X, errlow,errhigh, 'horizontal');   
title({'Mean Automated Time Measurement'})
%xlabel('Measurement') 
xlabel('Mean Time (s)') 
ax = gca;
ax.FontSize = 48;
er.Color = [0 0 0];                            
er.LineStyle = 'none';  
er.CapSize = 40;
er.LineWidth = 3;
ax.YGrid = 'on';
xtickangle(0);