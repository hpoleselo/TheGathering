function plotDataLTSpice()
    clc;clear all;

    % Importing data from LTSpice
    data = load('passabaixaativo.txt');
    data2 = load('passabaixalc.txt');
   
    % Magnitude, since we exported it as a Real + Img, not as dB/Phase
    mag_circuit = abs(data(:,2) + i*data(:,3))
    mag_circuit2 = abs(data2(:,2) + i*data2(:,3))
    
    % Plotting magnitude
    figure
    semilogx(data(:,1),20*log10(mag_circuit),'k',data2(:,1),20*log10(mag_circuit2),'r--','linewidth',2)
    xlim([25e3 124e3])
    ylim([-60 0])
    legend('Rede LC Passiva','Rede Ativa Transformada')
    xlabel('Frequência [Hz]');
    ylabel('Magnitude [dB]');
    grid on
    
    % Plotting the phase
    % Calculate the phase from the imported data
    phase = rad2deg(unwrap(angle(data(:,2) + i*data(:,3))));
    phase2 = rad2deg(unwrap(angle(data2(:,2) + i*data2(:,3))));
    
    semilogx(data(:,1),phase,'k',data(:,1),phase2,'--r','linewidth',2)
    xlim([1e0 130e3])
    legend('Rede LC Passiva','Rede Ativa Transformada')
    xlabel('Frequência [Hz]');
    ylabel('Ângulo [graus]');
    grid on
    
    %saveas(gcf,'magnitude.png');
    
end
