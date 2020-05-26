%Code to highligh T_Cook_1 in teh trajectory - based on modifying code by
%SImon Hauser

%% Tabula rasa
%clear all
clc
close all
format compact

%% Import data
%run import_script.m

%% Parameter setting
framerate = 10;

%% Define tool positions
area_bowl = [-0.16 0.16 0.04 0.6]; %extended bowl area
area_cups = [-0.19 -0.17 0.04 0.06]; %extended cups area
area_whisk = [-0.3 -0.07 -0.16 0.2];
area_ladel = [-0.41 -0.07 -0.3 0.2];
area_spatula = [-0.55 -0.07 -0.41 0.51];
area_pan = [0.025 0.02 0.46 0.52]; %extended pan area
area_idle = [-0.1 0.6 0.5 1.1];

%% Draw scene

hold on
set(gcf,'color','w');
sidelength = 0.7
x1 = -0.6
y1 = -0.2
%axis equal
%xlim([-0.6 0.1]) %make sure x and y have the same range
%ylim([-0.2 0.52])
axis equal
xlim([-0.6 0.5]) %make sure x and y have the same range
ylim([-0.2 1.1])


rectangle_colour = '#DCDCDC';
%rectangle('Position',[0.04 0.32 0.42 0.11],'FaceColor', [0.8, 0.8, 0.8, 0.5],'EdgeColor', [0.8, 0.8, 0.8, 0.5]) %extended pan region top
rectangle('Position',[area_pan(1) area_pan(2) area_pan(3)-area_pan(1) area_pan(4) - area_pan(2)],'FaceColor', rectangle_colour,'EdgeColor', [0.8, 0.8, 0.8, 0.5]) %extended pan region left
rectangle('Position',[0.16 0.02 0.3 0.3]) %pan

rectangle('Position',[area_bowl(1) area_bowl(2) area_bowl(3)-area_bowl(1) area_bowl(4) - area_bowl(2)],'FaceColor', rectangle_colour,'EdgeColor', [0.7, 0.7, 0.7, 0.7]) %extended bowl region
rectangle('Position',[-0.16 0.16 0.2 0.17]) %bowl rectangle
rectangle('Position',[-0.15 0.16 0.18 0.17],'Curvature',[1 1]) %bowl


rectangle('Position',[area_cups(1) area_cups(2) area_cups(3)-area_cups(1) area_cups(4) - area_cups(2)],'FaceColor', rectangle_colour,'EdgeColor', [0.8, 0.8, 0.8, 0.7]) %extended cup region
rectangle('Position',[-0.19 -0.17 0.23 0.1]) %cups rectangle
rectangle('Position',[-0.19 -0.17 0.1 0.1],'Curvature',[1 1]) %cup1
rectangle('Position',[-0.06 -0.17 0.1 0.1],'Curvature',[1 1]) %cup2


rectangle('Position', [area_whisk(1) area_whisk(2) area_whisk(3)-area_whisk(1) area_whisk(4) - area_whisk(2)]) %whisk device [-0.3 -0.07 0.14 0.27]


rectangle('Position',[area_ladel(1) area_ladel(2) area_ladel(3)-area_ladel(1) area_ladel(4) - area_ladel(2)]) %ladel device


rectangle('Position',[area_spatula(1) area_spatula(2) area_spatula(3)-area_spatula(1) area_spatula(4) - area_spatula(2)]) %spatula


rectangle('Position',[area_idle(1) area_idle(2) area_idle(3)-area_idle(1) area_idle(4) - area_idle(2)]) %idle
%text(-0.1,0.5-0.02,'idle','FontSize', 20)

%plot(data(:,1),data(:,2), 'Color' ,'#808080') %simple plotting
%colorful plotting
 %for a=1:1:rows-1 
  %   plot(data(a:a+1,1),data(a:a+1,2),'Color',[a/rows, 0, 0], 'LineWidth', 2)
% end
%plot(data(1,1),data(1,2),'k.','MarkerSize',30)
colormap([((0+1/rows):1/rows:1)',zeros(rows,1),zeros(rows,1)])
%colorbar('Ticks',[0, 1],'TickLabels',{'0 s',strcat(num2str(floor(rows/framerate)),' s')})
xlabel('x position [m]')
ylabel('y position [m]')
%title('Example Cooking Trajectory')
set(gca,'FontSize', 24);

labelfontsize = 24

% text(0.16,0.02-0.02,'pan', 'FontSize', labelfontsize)
% text(-0.05,0.16-0.02,'bowl','FontSize', labelfontsize)
% text(-0.19,-0.16-0.02,'cups','FontSize', labelfontsize)
% text(-0.28,0.04-0.07,'whisk','FontSize', labelfontsize)
% text(-0.40,0.04-0.07,'ladel','FontSize', labelfontsize)
% text(-0.55,0.04-0.07,'spatula','FontSize', labelfontsize)
% text(-0.05,0.66-0.02,'idle','FontSize', labelfontsize)
text(0.16,0.02-0.02+0.3,'pan', 'FontSize', labelfontsize)
text(-0.05,0.14,'bowl','FontSize', labelfontsize)

text(-0.29,0.14,'whisk','FontSize', labelfontsize)
text(-0.40,0.22,'ladel','FontSize', labelfontsize)
text(-0.55,0.3,'spatula','FontSize', labelfontsize)
text(-0.05,0.66-0.02,'idle','FontSize', labelfontsize)
drawnow


%% Algorithm

key_times_list = [1];

stage = 0
substage = 0
for i=1:length(data)
    %i
    x = data(i,1);
    y = data(i,2);
    
%     plot(x,y,'k.','MarkerSize',12)
%     drawnow
%     pause(0.01)
    
    %first cup ------------------------------------------------------------
    if substage == 0
        if (x>area_cups(1) && x<area_cups(3) && y>area_cups(2) && y<area_cups(4))
            display('getting first cup in cup zone, start of pouring stage')
            i
            stage = 1
            substage = 1;
            key_times_list = [key_times_list, i];
        end
    end

    
    if substage == 1
        if (x<area_cups(1) || x>area_cups(3) || y<area_cups(2) || y>area_cups(4))
            display('exit cup zone with first cup')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %second cup
    if substage == 2
        if (x>area_cups(1) && x<area_cups(3) && y>area_cups(2) && y<area_cups(4))
            display('putting back first cup and getting second cup in cup zone')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 3
        if (x<area_cups(1) || x>area_cups(3) || y<area_cups(2) || y>area_cups(4))
            display('exit cup zone with second cup')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
%     %third cup
%     if substage == 4
%         if (x>area_cups(1) && x<area_cups(3) && y>area_cups(2) && y<area_cups(4))
%             display('getting third cup in cup zone')
%             i
%             substage = substage + 1;
%         end
%     end
%     
%     if substage == 5
%         if (x<area_cups(1) || x>area_cups(3) || y<area_cups(2) || y>area_cups(4))
%             display('exit cup zone with third cup')
%             i
%             substage = substage + 1;
%         end
%     end
    
    %finalizing pouring
    if substage == 4
        if (x>area_bowl(1) && x<area_bowl(3) && y>area_bowl(2) && y<area_bowl(4))
            display('pouring last cup')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 5
        if (x<area_bowl(1) || x>area_bowl(3) || y<area_bowl(2) || y>area_bowl(4))
            display('pouring stage finished')
            pouring_end = i
            stage = 2
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %pick up stirrer ------------------------------------------------------
    if substage == 6
        if (x>area_whisk(1) && x<area_whisk(3) && y>area_whisk(2) && y<area_whisk(4))
            display('entering whisk tool zone')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 7
        if (x<area_whisk(1) || x>area_whisk(3) || y<area_whisk(2) || y>area_whisk(4))
            display('exit whisk tool zone with whisk')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %start stirring
    if substage == 8
        if (x>area_bowl(1) && x<area_bowl(3) && y>area_bowl(2) && y<area_bowl(4))
            disp('entering bowl zone with whisk, start stirring')
            stirring_start = i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %end stirring
    if substage == 9
        if (x<area_bowl(1) || x>area_bowl(3) || y<area_bowl(2) || y>area_bowl(4))
            display('exit bowl zone with whisk, stirring finished')
            stirring_end = i
            stirring_time = stirring_end - stirring_start
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %put back stirring tool
    if substage == 10
        if (x>area_whisk(1) && x<area_whisk(3) && y>area_whisk(2) && y<area_whisk(4))
            display('putting back whisk tool')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 11
        if (x<area_whisk(1) || x>area_whisk(3) || y<area_whisk(2) || y>area_whisk(4))
            display('whisk back, stirring stage finished')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %pick up ladel tool
    if substage == 12
        if (x>area_ladel(1) && x<area_ladel(3) && y>area_ladel(2) && y<area_ladel(4))
            display('entering ladel tool zone to pick up tool')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 13
        if (x<area_ladel(1) || x>area_ladel(3) || y<area_ladel(2) || y>area_ladel(4))
            display('exit ladel tool zone with ladel')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %use ladel tool
    if substage == 14
        if (x>area_bowl(1) && x<area_bowl(3) && y>area_bowl(2) && y<area_bowl(4))
            display('entering bowl zone with ladel')
            ladel_start = i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 15
        if (x<area_bowl(1) || x>area_bowl(3) || y<area_bowl(2) || y>area_bowl(4))
            display('exit bowl zone with batter')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 16
        if (x>area_pan(1) && x<area_pan(3) && y>area_pan(2) && y<area_pan(4))
            display('entering pan zone with batter')
            i
            cooking_1_start = i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 17
        if (x<area_pan(1) || x>area_pan(3) || y<area_pan(2) || y>area_pan(4))
            display('exit pan zone with ladel tool, pancake starts cooking')

            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %putting back ladel tool
    if substage == 18
        if (x>area_ladel(1) && x<area_ladel(3) && y>area_ladel(2) && y<area_ladel(4))
            display('entering ladel tool zone with ladel')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 19
        if (x<area_ladel(1) || x>area_ladel(3) || y<area_ladel(2) || y>area_ladel(4))
            display('exit ladel tool zone, tool is back')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %pick up spatula
    if substage == 20
        if (x>area_spatula(1) && x<area_spatula(3) && y>area_spatula(2) && y<area_spatula(4))
            display('entering spatula tool zone to pick up tool')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 21
        if (x<area_spatula(1) || x>area_spatula(3) || y<area_spatula(2) || y>area_spatula(4))
            display('exit spatula tool zone with tool')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %flip pancake
    if substage == 22
        if (x>area_pan(1) && x<area_pan(3) && y>area_pan(2) && y<area_pan(4))
            display('entering pan zone with spatula to flip pancake')
            cooking_1_end = i
            cooking_1_time = cooking_1_end - cooking_1_start
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 23
        if (x<area_pan(1) || x>area_pan(3) || y<area_pan(2) || y>area_pan(4))
            display('exit pan zone with spatula, pancake is flipped')
            cooking_2_start = i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %put back spatula
    if substage == 24
        if (x>area_spatula(1) && x<area_spatula(3) && y>area_spatula(2) && y<area_spatula(4))
            display('entering spatula tool zone to put back tool')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 25
        if (x<area_spatula(1) || x>area_spatula(3) || y<area_spatula(2) || y>area_spatula(4))
            display('exit spatula tool zone, tool is back')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %pick up spatula again to take out pancake
    if substage == 26
        if (x>area_spatula(1) && x<area_spatula(3) && y>area_spatula(2) && y<area_spatula(4))
            display('entering spatula tool zone to pick up tool to remove pancake')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 27
        if (x<area_spatula(1) || x>area_spatula(3) || y<area_spatula(2) || y>area_spatula(4))
            display('exit spatula tool zone with tool')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    %take out pancake, finish cooking
    if substage == 28
        if (x>area_pan(1) && x<area_pan(3) && y>area_pan(2) && y<area_pan(4))
            display('entering pan zone to remove the pancake')
            i
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 29
        if (x<area_pan(1) || x>area_pan(3) || y<area_pan(2) || y>area_pan(4))
            display('exit pan zone with pancake, finish cooking')
            cooking_2_end = i
            cooking_2_time = cooking_2_end - cooking_2_start
            display('cooking ended successfully')
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    
    if substage == 30
        if (x>area_spatula(1) && x<area_spatula(3) && y>area_spatula(2) && y<area_spatula(4))
            display('returning spatula')

            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
    if substage == 31
        if (x<area_spatula(1) || x>area_spatula(3) || y<area_spatula(2) || y>area_spatula(4))
            display('finished returning spatula')
            substage = substage + 1;
            key_times_list = [key_times_list, i];
        end
    end
end

key_times_list;
stage1 = 21+1;
stage2 =22+1;
offset1 = 1;
offset2  = 1;
% 1,8,0,10
% 8,8,10,0
% 8,9,0,1
% 10, 11, 0, 0 
% 11, 13, 0, 9

%8,13,0,0
%22,26,0,0


sec = [13,17,0,0] %pick up spatula
plot(data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),1),data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),2), 'Color' ,'#0000FF', 'LineWidth',1.5)
%sec = [23,24,0,0]  %flip pancake
%end of this is time start
%plot(data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),1),data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),2), 'Color' ,'#0000FF', 'LineWidth',1.5)
sec = [17,23,0,0] %return spatula
plot(data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),1),data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),2), 'Color' ,'#FF0000', 'LineWidth',1.5)
sec = [23,26,0,0] %return spatula
plot(data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),1),data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),2), 'Color' ,'#77AC30', 'LineWidth',1.5)
%sec = [26,27,0,10] %idle
%plot(data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),1),data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),2), 'Color' ,'#FFFF00', 'LineWidth',1.5)
%sec = [27,28, 10,0] %pick up spatula
%plot(data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),1),data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),2), 'Color' ,'#00FFFF', 'LineWidth',1.5)
%sec = [28,29,0,0] %go to hotplate
%plot(data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),1),data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),2), 'Color' ,'#77AC30', 'LineWidth',1.5)
%sec = [29,30,0,0] %remove pancake
% end of this is time end
%plot(data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),1),data(key_times_list(sec(1)+1)-sec(3):key_times_list(sec(2)+1)-sec(4),2), 'Color' ,'#D95319', 'LineWidth',1.5)

legendtext = {'Pick up ladel', 'T\_Cook\_1', 'Return spatula'}
lgd = legend(legendtext)
lgd.NumColumns = 2
lgd.Location = 'north'

% lh = gco
% s = get(lh, 'string'); 
% set(lh, 'string',s(3:9));

%plot(data(key_times_list(stage1)-offset1:key_times_list(stage2)-offset2,1),data(key_times_list(stage1)-offset1:key_times_list(stage2)-offset2,2), 'Color' ,'#A2142F', 'LineWidth',1.5)
dotpoint1 = key_times_list(stage1) -offset1;
dotpoint2 = key_times_list(stage2) -offset2;
%plot(data(dotpoint1,1),data(dotpoint1,2),'r.','MarkerSize',12, 'Marker', 'o')
%plot(data(dotpoint2,1),data(dotpoint2,2),'r.','MarkerSize',40)

dotpoint1 = key_times_list(17+1);
dotpoint2 = key_times_list(23+1);

plot(data(dotpoint1,1),data(dotpoint1,2),'b.','MarkerSize',25, 'DisplayName', 'T\_Cook\_1 timer start')
plot(data(dotpoint2,1),data(dotpoint2,2),'r.','MarkerSize',25, 'DisplayName', 'T\_Cook\_1 timer finish')
[stirring_time cooking_1_time cooking_2_time]
hold off