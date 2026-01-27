from machine import Pin, I2C
import ssd1306
import time

# --- 1. CONFIGURAÇÃO DO HARDWARE ---
# I2C para a tela OLED (GP4 e GP5)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Botão Verde (GP15)
btn_trigger = Pin(15, Pin.IN, Pin.PULL_UP)

# Encoder (GP10 e GP11)
clk = Pin(10, Pin.IN, Pin.PULL_UP)
dt = Pin(11, Pin.IN, Pin.PULL_UP)

# --- 2. VARIÁVEIS DE ESTADO ---
counter = 0
last_clk_status = clk.value()

print("NERVE SYSTEM (MicroPython) Online")

while True:
    # --- LÓGICA DO ENCODER (Hype Dial) ---
    clk_status = clk.value()
    if clk_status != last_clk_status and clk_status == 0:
        if dt.value() != clk_status:
            counter = min(100, counter + 5) # Trava no 100
        else:
            counter = max(0, counter - 5)   # Trava no 0
    last_clk_status = clk_status

    oled.fill(0)
    oled.text("THE NERVE v1.0", 10, 0)
    oled.hline(0, 15, 128, 1) # Linha de separação
    
    # Barra de Progresso Cinematográfica
    oled.rect(10, 30, 100, 10, 1) # Moldura da barra
    fill_width = int((counter / 100) * 98)
    oled.fill_rect(11, 31, fill_width, 8, 1) # Preenchimento
    
    oled.text(f"O valor do HYPE: {counter}%", 30, 45)

    if btn_trigger.value() == 0:
        oled.fill(1) # Flash de "REC"
        oled.text("RENDERING...", 20, 30, 0)
        oled.show()
        time.sleep(0.5) # Mantém o flash por meio segundo

    oled.show()

    # Exibe o nível de Hype
    oled.text("HYPE LEVEL:", 5, 25)
    oled.text(str(counter), 95, 25)
    
    # Define o modo
    mode = "LOFI"
    if counter > 10: mode = "EDIT"
    if counter > 20: mode = "CINEMA"
    oled.text(f"MODE: {mode}", 25, 45)

    # --- LÓGICA DO BOTÃO (Trigger) ---
    if btn_trigger.value() == 0: # Botão pressionado
        oled.fill(1) # Inverte a tela toda (Flash!)
        oled.text("ENVIANDO...", 25, 30, 0) # Texto preto no fundo branco
        print("Ação Disparada!")

    oled.show()
    # time.sleep(0.01) # Pequena pausa para estabilidade