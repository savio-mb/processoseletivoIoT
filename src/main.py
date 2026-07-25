import machine
import time


ldr_pin = machine.ADC(machine.Pin(34))
ldr_pin.atten(machine.ADC.ATTN_11DB)


btn_pin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

contador = 0
estado_bloqueado = False
tempo_bloqueio_inicio = 0
alerta_emitido = False


LIMIAR_ADC = 1600

ultimo_estado_btn = btn_pin.value()
estado_btn_valido = ultimo_estado_btn
ultimo_tempo_debounce = 0

ATRASO_DEBOUNCE = 50

print("Contador de Producao Inicializado")


while True:
    tempo_atual = time.ticks_ms()

    leitura_btn = btn_pin.value()

    if leitura_btn != ultimo_estado_btn:
        ultimo_tempo_debounce = tempo_atual

    if time.ticks_diff(tempo_atual, ultimo_tempo_debounce) > ATRASO_DEBOUNCE:
        if leitura_btn != estado_btn_valido:
            estado_btn_valido = leitura_btn

            if estado_btn_valido == 0:
                contador = 0
                estado_bloqueado = False
                alerta_emitido = False

                print("Turno resetado com sucesso. Contadores zerados.")

    ultimo_estado_btn = leitura_btn

    adc_val = ldr_pin.read()

    luz_bloqueada = adc_val > LIMIAR_ADC

    if luz_bloqueada:
        if not estado_bloqueado:
            estado_bloqueado = True
            tempo_bloqueio_inicio = tempo_atual
            alerta_emitido = False
        else:
            if not alerta_emitido and time.ticks_diff(tempo_atual, tempo_bloqueio_inicio) >= 5000:
                print("Alerta: Micro-parada detectada!")
                alerta_emitido = True
    else:
        if estado_bloqueado:
            estado_bloqueado = False
            contador += 1
            print("Peca detectada! Total: " + str(contador))
            alerta_emitido = False

    time.sleep_ms(10)
