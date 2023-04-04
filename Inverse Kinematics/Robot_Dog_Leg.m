clc
clear
clf

% First half of leg movement
% Path curve function: Step forward
stepL = 8;
xpos = linspace(0,stepL,11);
ypos = [0 1 3 4 4 4 4 4 3 1 0];
cs = spline(xpos,[0 ypos 0]);
% the path where the foot is at (0,0)
steps = 30; % number of intervals wanna take
x = linspace(0,stepL,steps);
yy = ppval(cs,x);
% the path where the foot is at (0,-16)
y = yy-16;
figure(1)
plot(xpos,ypos,'o',x,yy,'-')
ylim([0 16])
xlabel('x displacement(cm)')
ylabel('y displacement(cm)')
title('Leg Path')

% Second half of leg movement
% Adding backward movement
x = [x linspace(stepL,0,steps)];
y = [y zeros(1,steps)-16];

% Leg
L1 = 10;
L2 = 10;

% IK loop
for i = 1:length(x)
    
    % IK
    L3=sqrt(x(i)^2+y(i)^2);
    b1 = (-(L2^2-L1^2-L3^2)/(2*L1*L3));
    a1 = atan2(sqrt(1-b1^2),b1);
    theta1(i) = (atan2(y(i),x(i))-a1)*(180/pi);
    b2 = (-(L3^2-L1^2-L2^2)/(2*L1*L2));
    a2 = atan2(sqrt(1-b2^2),b2);
    theta2(i) = (pi-a2)*(180/pi);

    % Angles for motor movement
    if i > 1
        theta11(i) = theta1(i)-theta1(i-1);
        theta22(i) = theta2(i)-theta2(i-1);
    end
    theta11(1) = theta1(1);
    theta22(1) = theta2(1);

    % Animation
    figure(2)
    clf
    X = [0 L1*cos(theta1(i)*(pi/180)) x(i)];
    Y = [0 L1*sin(theta1(i)*(pi/180)) y(i)];
    xlim([-16 16])
    ylim([-16 16])
    hold on
    plot(X,Y)

%     % Debugging stuff
%     L1_1 = sqrt((L1*cos(theta1(i)*(pi/180)))^2+(L1*sin(theta1(i)*(pi/180)))^2);
%     L2_1 = sqrt((x(i)-L1*cos(theta1(i)*(pi/180)))^2+(y(i)-L1*sin(theta1(i)*(pi/180)))^2);
%     fprintf('Theta1 %5.2f\n', theta1(i))
%     fprintf('Theta2 %5.2f\n', theta2(i))
%     fprintf('L1 %3.2f\n', L1_1)
%     fprintf('L2 %3.2f\n', L2_1)
%     fprintf('--------------------\n')

    pause(0.1)
end

writematrix(theta11,'Theta1.txt')
writematrix(theta22,'Theta2.txt')
writematrix(theta1,'Theta_1.txt')
writematrix(theta2,'Theta_2.txt')