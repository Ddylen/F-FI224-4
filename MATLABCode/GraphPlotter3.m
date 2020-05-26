
%code to plot a graph of the taste scores 
%For the taste scores graph
workbooktouse = scoringworkbook3

mean1= workbooktouse{[2,3,4],2};
mean2 = workbooktouse{[2,3,4],3};
mean3= workbooktouse{[2,3,4],4};
mean4 = workbooktouse{[2,3,4],5};
mean5= workbooktouse{[2,3,4],6};
mean6= workbooktouse{[2,3,4],7};

mean1 = reshape(mean1,1,[])
mean2 = reshape(mean2,1,[])
mean3 = reshape(mean3,1,[])
mean4 = reshape(mean4,1,[])
mean5 = reshape(mean5,1,[])
mean6 = reshape(mean6,1,[])
means = [mean1; mean2; mean3; mean4; mean5; mean6]

%categorical(scoringworkbookS2{4,[2,3,4]})
X = categorical({'A';'B';'C'; 'D'; 'E'; 'Average'});
X = reordercats(X,{'A';'B';'C'; 'D'; 'E'; 'Average'});
bar(X, means)
ylim([0 10])
hold on

%er = errorbar(X,means,errlow,errhigh);   
title('Mean Pancake Quality Scores')
xlabel('Pancake') 
ylabel({'Mean Score'}) 
ax = gca;
ax.FontSize = 24;
legendlabels= {'Appearance','Taste','Texture'}
lgd = legend(legendlabels)
lgd.NumColumns = 1
ax.YGrid = 'on';