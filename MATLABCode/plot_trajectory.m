%Code to plot the xy trajectory of a demonstrator, written by Simon Hauser

%% Tabula rasa
% close all
figure

%% Parameter setting
time_vector = 0:1/framerate:rows/framerate-1/framerate;

%% Plot regions
hold on
set(gcf,'color','w');
xlim([0 time_vector(end)])
ylimits = [-0.8 1.3]
ylim(ylimits)


empty = [0,0,0,0];
timecolour = [0,0,0,1];
actioncolour = [0.7, 0.7, 0.7, 0.7];
idle= [1,0,0,0.5];

rectangle('Position',[1230/framerate ylimits(1) (1880-1230)/framerate ylimits(2)-ylimits(1)],'FaceColor', idle,'EdgeColor', idle) %cooking 2 stage
rectangle('Position',[2170/framerate ylimits(1) (2500-2170)/framerate ylimits(2)-ylimits(1)],'FaceColor', idle,'EdgeColor', idle) %cooking 2 stage


rectangle('Position',[0 ylimits(1) pouring_end/framerate ylimits(2)-ylimits(1)],'FaceColor', actioncolour,'EdgeColor', actioncolour) %pouring stage
rectangle('Position',[ladel_start/framerate ylimits(1) (cooking_1_start-ladel_start)/framerate ylimits(2)-ylimits(1)],'FaceColor', actioncolour,'EdgeColor', actioncolour) %batter stage
rectangle('Position',[cooking_1_end/framerate ylimits(1) (cooking_2_start-cooking_1_end)/framerate ylimits(2)-ylimits(1)],'FaceColor', actioncolour,'EdgeColor', actioncolour) %flipping stage
rectangle('Position',[cooking_2_end/framerate ylimits(1) time_vector(end) ylimits(2)-ylimits(1)],'FaceColor', actioncolour,'EdgeColor', actioncolour) %cooking 2 stage

rectangle('Position',[stirring_start/framerate ylimits(1) (stirring_end-stirring_start)/framerate ylimits(2)-ylimits(1)],'FaceColor', empty,'EdgeColor', timecolour) %stirring stage
rectangle('Position',[cooking_1_start/framerate ylimits(1) cooking_1_time/framerate ylimits(2)-ylimits(1)],'FaceColor', empty,'EdgeColor', timecolour) %cooking 1 stage
rectangle('Position',[cooking_2_start/framerate ylimits(1) cooking_2_time/framerate ylimits(2)-ylimits(1)],'FaceColor', empty,'EdgeColor', timecolour) %cooking 2 stage
%% Plot trajectories

plot(time_vector',data(:,1),'LineWidth',2)
plot(time_vector',data(:,2),'LineWidth',2)
plot(time_vector',data(:,3),'LineWidth',2)

lgd = legend({'x position','y position', 'z position'})
lgd.Location = 'south'
lgd.NumColumns = 3
xlabel('time [s]')
ylabel('position [m]')
title('Example X, Y and Z Trajectories')
set(gca,'FontSize', 48);
grid on
hold off
cooking_2_end


