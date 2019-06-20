t = -250:1:250; % from -250s to 250s
% t = 0 is defined as highest elevation angle

c = 299792.458; % speed of light in km/s
R = 6371; %Earth's radius in km
h = 500; % orbital altitude in km
r = R + h; 
g = 0.0098; %gravitational acceleration in km/s^2

V = (R^2 * g / r)^0.5; % velocity
gamma = V * t ./ r; % angular velocity

s = (R^2 + r^2 - 2*R*r*cos(gamma)).^0.5;
% theta = pi/2 - V * t ./ s; % angle of elevation
theta = acos(r .* sin(gamma) ./ s);

 
f_c = 1000000; % carrier frequency in Hz
f_d = V * f_c * cos(theta) ./ c; % Doppler shift in Hz


plot(t,s, 'LineWidth', 1.5, 'Color', 'black');
xlabel('time (s)', 'Interpreter','latex');
ylabel('distance from ground station (km)', 'Interpreter','latex');
set(gca, 'FontName','Latin Modern Math');
saveas(gcf, 'distance.png');

figure;
plot(t, f_d, 'LineWidth', 1.5, 'Color', 'black');
xlabel('time (s)', 'Interpreter','latex');
ylabel('Doppler shift (Hz)', 'Interpreter','latex');
set(gca, 'FontName','Latin Modern Math');
saveas(gcf, 'doppler_shift.png');

dfdt = gradient(f_d(:)) ./ gradient(t(:));
plot(t, dfdt, 'LineWidth', 1.5, 'Color', 'black');
xlabel('time (s)', 'Interpreter','latex');
ylabel('Doppler shift rate (Hz/s)', 'Interpreter','latex');
set(gca, 'FontName','Latin Modern Math');
saveas(gcf, 'doppler_shift_rate.png');
