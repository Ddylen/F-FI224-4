%test code to evaluate distance correlation between my timings and relaive
%quality scores, superceeded by DistanceCorrelationGraph

%C= [1;1;1;2]
%D = [2;1;1;2]
%distcorr(C, D )

Aparams= 	[11.3;	169.9;	163.8];
Bparams=	[48.7;	101.7;	51.5];
Cparams=	[43.4;	129.8;	86];
Dparams= 	[23.9;	133.2;	64.9];
Eparams=	[21.4;	95.7;	133.6];


	%Appearance	Taste	Texture	Sum
Ascores=	[0.25;	-0.25;	-1.75;	-1.75];
Bscores=	[-0.5;	0;	-1;	-1.5];
Cscores=	[-1.333333333;	-0.666666667;	-1.333333333;	-3.333333333];
Dscores=	[-0.666666667;	0.333333333;	0.333333333;	0];
Escores=	[0.333333333;	0;	-1;	-0.666666667];

%           T_stir, T_Cook_1, T_Cook_2;
times=      [11.3,	169.9,	163.8;
            48.7,	101.7,	51.5;
            43.4,	129.8,	86;
            23.9,	133.2,	64.9;
            21.4,	95.7,	133.6;];
;
%           Appearance, Taste, Texture,	Sum;
scores=     [0.25,	-0.25,	-1.75,	-1.75;
            -0.5,	0,	-1,	-1.5;
            -1.333333333,	-0.666666667,	-1.333333333,	-3.333333333;
            -0.666666667,	0.333333333,	0.333333333,	0;
            0.333333333,	0,	-1,	-0.666666667;];

for test= 1:3
    for score = 1:4
        results(test,score)= distcorr(times(:,test), scores(:,score));
    end
end
results
plotresults = transpose(results)
X = categorical({'T\_Stir';'T\_Cook\_1';'T\_Cook\_2'});
bar(X, plotresults)
ylim([0 1])
title('Correlation of Key Parameters with Quality Scores')
%xlabel('Key Parameter') 
ylabel('Distance Correlation') 

legendlabels= {'Appearance','Taste','Texture', 'Overall'}
lgd = legend(legendlabels)
lgd.NumColumns = 4
lgd.Location = 'southoutside'
ax = gca;
ax.FontSize = 48;