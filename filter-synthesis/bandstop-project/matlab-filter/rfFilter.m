% Work for Circuit Synthesis
% Professor: Maicon Pereira
% Author: Henrique Poleselo

function rfFilter()

    % Project Parameters / Requirements:
    % Stopband filter from 35kHz to 80kHz
    % Passband from 500Hz to 20MHz
    wp = [35e3 80e3]*2*pi;
    ws = [500 20e6]*2*pi;
    Amax = 0.2; % dB
    Amin = 40;  % dB

    % Obtaining the approximation for the filter using Butterworth aprox.
    [n wn] = buttord(wp, ws, Amax, Amin,'s');
   
    % 's' has to be passed, otherwise it will consider it's a digital
    % filter
    [b,a] = butter(n,wn,'stop','s');
    
    % logspace(10^2, 10^7, 10^5 points), which is the boundary of our
    % filter
    w = logspace(2,7,1e5)*(2*pi);
    
    w1 = w/(2*pi);
    
    % Returns complex freq response vector H, in rad/s
    [h] = freqs(b,a,w);
   
    % Constrution of continuous transfer function 
    y = tf(b,a);

    % Obtaining poles and zeroes from TF, kn is the gain
    [zn,pn,kn] = tf2zp(b,a);
    

    % Extracting the Biquads from the poles and zeroes, i.e, converting the
    % roots to a polynomial form
    B1n=poly([zn(1),zn(2)]);
    B1d=poly([pn(1),pn(2)]);
    B2n=poly([zn(3),zn(4)]);
    B2d=poly([pn(3),pn(4)]);
    B1=tf(B1n,B1d);
    B2=tf(B2n,B2d);
    
    % Display our biquads so we can implement estimate the components's
    % values
    display(B1)
    display(B2)
    
    % Plotting
    subplot(2,1,1);
    y1 = 20*log(abs(h));
    semilogx(w1,y1);
    title('Amplitude');
    xlabel('Frequency [Hz]');
    ylabel('Amplitude [dB]');
    grid;

    subplot(2,1,2);
    y2 = angle(h);
    
    % unwrap to eliminate the discontinuity on the phase graph 
    %unwrap(y2);
    semilogx(w1,y2);
    title('Phase');
    xlabel('Frequency [Hz]');
    ylabel('Phase [Rad]');
    grid;
    
    % Export graphs
    %saveas(gcf,'freq.png');
    
    % Importing data from LTSpice
    data = load('ltspiceexport.txt')
    
    % Magnitude, since we exported it as a Real + Img, not as dB/Phase
    mag_circuit = abs(data(:,2) + i*data(:,3))
    
    % Plotting data to compare ltspice simulated and from matlab's
    figure
    semilogx(data(:,1),20*log10(mag_circuit),'k',w1,20*log10(abs(h)),'r--','linewidth',2)
    xlim([1e2 100e5])
    ylim([-250 10])
    legend('Circuito','Aproximacao')
    xlabel('Frequency [Hz]');
    ylabel('Magnitude [dB]');
    grid on
    
    figure
    
    % Plotting the phase
    % Calculate the phase from the imported data
    phase = angle(data(:,2) + i*data(:,3));
    
    semilogx(data(:,1),phase,'k',w1,y2,'--r','linewidth',2)
    legend('Circuito','Aproximacao')
    xlabel('Frequency [Hz]');
    ylabel('Angle [rad/s]');
    grid on
    
    saveas(gcf,'phase.png');
end