from machine import Pin, PWM
import time

 # Pin do LED onboard no Raspberry Pi Pico
led = PWM(Pin('LED'))
push_button = Pin(14, Pin.IN, Pin.PULL_UP)

# Configura o PWM no GP1
pwm_pin = PWM(Pin(1))

# Define a frequencia do PWM
pwm_pin.freq(1000)

# Define o ciclo de trabalho (duty cicle) de 0 a 65535
# 0 = desligado, 32767 = 50%, 65535 = 100%
pwm_pin.duty_u16(32767) # 50%

time.sleep(2)

while True:
    # led.toggle()  # Alterna o estado do LED (liga/desliga)
    if push_button.value() == 0:
        # Deixa o LED apagado por 1s
        led.duty_u16(0)
        time.sleep(1)
       
       # Deixa o LED aceso com metade da potência por 1s
        led.duty_u16(32767)
        time.sleep(1)
        
        # Deixa o LED aceso com toda potência por 1.5s
        led.duty_u16(65535)
        time.sleep(1.5)

    else:
        # Botão não pressionado
        led.duty_u16(0) # Desliga o LED se o botão não estiver pressionado
        pass
    time.sleep(0.3) # Pequeno atraso para não sobrecarregar