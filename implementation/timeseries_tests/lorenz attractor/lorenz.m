
sigma = 10;
beta = -3;
rho = 30;
f = @(t,a) [-sigma*a(1) + sigma*a(2); rho*a(1) - a(2) - a(1)*a(3); -beta*a(3) + a(1)*a(2)];
[t,a] = ode45(f,[0 100],[5 5 5]);     % Runge-Kutta 4th/5th order ODE solver
%plot(a(3))