# Sevcon Gen5 Size 9 — Configuração Ampera Racing

> **Status:** ✅ FUNCIONANDO
> **DCF de referência:** `funciona_29-05.dcf`
> **Data:** 28-29/05/2026

---

## 1. Hardware

### Inversor
- **Modelo:** BorgWarner Gen5 Size 9
- **Algoritmo:** Induction Vector Control - Torque Mode
- **Bus DC nominal:** 144 V
- **Bus DC máximo:** 168 V

### Motor — Hercules 610000379

| Parâmetro | Valor |
|---|---|
| Potência nominal / pico | 11 kW / 28 kW |
| Tensão nominal (Vca) | 102 V (ligação estrela) |
| Frequência nominal | 103 Hz |
| Corrente nominal / vazio / máx | 133 A / 114 A / 257 A |
| Rotação nominal / máxima S2 | 3000 / 6000 RPM |
| Torque nominal / pico | 34.85 / 94 Nm |
| Polos / pares de polos | 4 / 2 |
| Fator de potência (carga plena) | 0.54 |
| Momento de inércia | 0.0696 kg·m² |
| Regime de serviço | S2, 60 min |

#### Parâmetros elétricos (fabricante)
| Parâmetro | Valor |
|---|---|
| Stator Resistance (Rs) | 14.3 mΩ |
| Rotor Resistance (Rr) | 13.8 mΩ |
| Magnetizing Inductance (Lm) | 772 µH |
| Stator Leakage Inductance (Lls) | 90.7 µH |
| Rotor Leakage Inductance (Llr) | 111.2 µH |

### Encoder — BMO-6204/048S2/UA108A (SKF)
- Tipo: AB incremental magnético, integrado em rolamento
- PPR: 48
- Phase shift A↔B: 90° ±20°
- Period accuracy: ±3%

---

## 2. Configurações Alteradas

### 2.1 Speed Regulator [aba Speed Regulator]

| Parâmetro | Default | Configurado | Por quê |
|---|---|---|---|
| Speed regulator Kp | 0.0 | **0.01 Nm/RPM** | Em zero, cutback de speed limit em torque mode não atua |
| Speed regulator Ki | 0.0 | **0.001 Nm/RPM/s** | Componente integral do mesmo loop |
| Accel Limit | 0.0 | **5000 RPM/s** | Limita aceleração comandada |
| Decel Limit | 0.0 | **5000 RPM/s** | Limita desaceleração comandada |

### 2.2 Modulation Index Control [aba Modulation Index]

| Parâmetro | Default | Configurado | Por quê |
|---|---|---|---|
| Mod index control Kp | 0.125 | **2.0** | Default 16× menor que recomendado — FW loop muito lento |
| Mod index control Ki | 0.0625 | **1.0** | Idem componente integral |

### 2.3 Corrente de Magnetização [0x4641]

> ⚠️ **Superado em 06/07/2026** — ver seção 3 (Flux Map variável). Mantido aqui como histórico do baseline.

| Parâmetro | Configurado | Por quê |
|---|---|---|
| **Im min = Im max = Im rated** | **102.4 A** | Não temos curva de saturação real do motor. Sem dados, FW dinâmico usaria estimativa não calibrada do DVT — preferimos Im fixo |

### 2.4 Battery Limits / DC Link Voltage Setup

| Parâmetro | Configurado | Por quê |
|---|---|---|
| Minimum Capacitor Voltage | **100 V** | Antes vazio |
| Maximum Capacitor Voltage | **168 V** | Antes vazio. Bus máximo |
| Nominal Capacitor Voltage | **144 V** | Antes vazio. Tensão nominal do bus |
| Capacitor Cutback Range | **10 V** | Antes vazio. Faixa de transição gradual |

Após preencher, executar **"Calculate / Write voltage cutbacks"**.

### 2.5 Speed Limit Ramp Rates [Baseline Profile 0x2920]

| Parâmetro | Default | Configurado | Por quê |
|---|---|---|---|
| Speed limit ramp down rate (torque mode) | 200 RPM/s | **50000 RPM/s** | Inércia super baixa do motor exige cutback rápido |
| Speed limit ramp up rate (torque mode) | 200 RPM/s | **50000 RPM/s** | Consistência |

### 2.6 Encoder Tracking PLL [0x4631]

| Parâmetro | Default | Configurado | Por quê |
|---|---|---|---|
| Primary encoder tracking loop PLL gain | 40000 | **13000** | Encoder ±20° phase shift causa oscilação periódica — banda menor filtra |
| Primary encoder tracking loop K1 | 65000 | **22000** | Mantém damping ζ≈1 com ωn menor |
| Primary encoder tracking loop K2 | 40000 | **4500** | Define ωn ~80-100 Hz |
| Encoder speed filter | 1000 Hz | **100 Hz** | Filtragem adicional na saída do PLL |

### 2.7 Saturation Map [0x4614]

> ⚠️ **Superado em 06/07/2026** — ver seção 3.3. Com o flux map variável, o saturation map precisa cobrir a faixa 30–102 A.

| Parâmetro | Configurado | Por quê |
|---|---|---|
| Im min = Im max | **102.4 A** | Im é fixo em 102.4 A (seção 2.3), então o map cobre apenas esse ponto |

### 2.8 Speed Limits (cadeia em camadas)

| Parâmetro | Configurado | Por quê |
|---|---|---|
| Local Motor Limits → Max motor speed | **6000 RPM mech** | S2 max do motor |
| Overspeed Limit [0x4624,0] | **7200 RPM mech** | Trip duro. Margem 20% sobre Max motor speed pra absorver o erro do encoder (modulação ±29% por phase shift ±20°) |

### 2.9 Low Speed Regulator [aba Low Speed Reg]

| Parâmetro | Default | Configurado | Por quê |
|---|---|---|---|
| Hi-Res speed threshold | 0.0 RPM | **1500.0 RPM** | Mantém o laço de alta resolução ativo até 1500 RPM para evitar o ruído ruidoso/vibratório do encoder de 48 PPR em rotações baixas. |
| Hi-Res speed threshold delta | 0.0 % | **30.0 %** | Faixa de transição suave de 1500 RPM a 1950 RPM (1500 + 30%), evitando ressonâncias e trancos na mudança de laço. |
| Hi-Res speed regulator Kp | 0.0 | **0.005 Nm/RPM** | Ganho proporcional conservador para evitar oscilações na arrancada e em baixas velocidades. |
| Hi-Res speed regulator Ki | 0.0 | **0.0005 Nm/RPM/s** | Ganho integral conservador para eliminar erros de regime sem induzir oscilações lentas. |

---

## 3. Flux Map variável — anti-tranco em repouso (06/07/2026)

### 3.1 Problema

Com o carro **no chão, ligado e parado** (torque request = 0), o motor vibra continuamente de um lado pro outro. No cavalete o sintoma quase não aparece (um tranco só e para). Girando o eixo na mão com o inversor habilitado, ele "puxa de volta" como uma mola.

**Causa raiz:** com Im fixo (seção 2.3), o motor mantém **102,4 A de magnetização mesmo parado com pedal solto**. O encoder de 48 PPR (192 contagens/volta) atualiza o ângulo em saltos discretos de ~1,9° mecânicos; cada salto desorienta momentaneamente o vetor de corrente e uma parte do Id "vaza" pro eixo de torque → pulso de torque a cada borda de pulso. No chão, a elasticidade pneu+corrente devolve o rotor através da mesma borda → ciclo-limite sustentado. No cavalete, a roda livre assenta entre duas bordas e o ciclo morre.

O pulso de torque parasita escala com o Id — reduzir a magnetização em repouso ataca a fonte do problema.

### 3.2 Motor Flux Map [0x4610]

Mapa torque demandado → corrente de magnetização (antes: 102,41 A em todas as linhas, e a tabela só cobria 46–94 Nm):

| Torque (Nm) | Mag Current (A) |
|---|---|
| 94 | 102.41 |
| 94 | 102.41 |
| 80 | 102.41 |
| 60 | 102.41 |
| 40 | 90 |
| 25 | 75 |
| 12 | 55 |
| 5 | 40 |
| 0 | 30 |

**Como a curva foi construída** (heurística de engenharia, não dado do fabricante — só temos o Im nominal):

1. **Platô (T ≥ 60 Nm → 102,41 A):** torque ≈ k·Id·Iq e o Iq tem teto (Is max = 257 A). Torque de pico exige campo pleno — nessa faixa **nada mudou**, performance de largada intacta.
2. **Meio (descida ~√T, com folga pra cima):** a divisão eficiente entre Id e Iq segue Id ∝ √T. Os valores ficaram deliberadamente **acima** da curva ótima de eficiência: campo extra = menos tempo re-fluxando quando pisa = melhor resposta. Priorizado resposta sobre eficiência.
3. **Piso (0 Nm → 30 A, ~30% do nominal):** não zerar o fluxo em repouso mantém o motor "pré-armado" pra primeira mordida de torque e o controle vetorial estável. 25–35% do Id nominal é faixa típica de idle flux em drives de tração. 30 A corta o torque parasita em ~70%.

⚠️ **Não usar a caixa "Set magnetising current to fixed value" com 0** — zera a tabela inteira e o motor não produz torque.

### 3.3 Saturation Map [0x4614] — atualização obrigatória

Com Id variando de 30 a 102 A, o map de ponto único (seção 2.7) não serve mais:

| Parâmetro | Configurado | Por quê |
|---|---|---|
| Im min | **30 A** | Piso do flux map |
| Im max | **102 A** | Im nominal |
| Perfil | **Calculate map** (gerador genérico) | Aproximado, mas melhor que Lm constante com Id variável |

### 3.4 Trade-off e validação

Custo teórico: ao pisar fundo do repouso, o fluxo sobe de 30→102 A com a constante de tempo do rotor (~dezenas a 200 ms). Na prática é mascarado pela rampa de torque de 150 Nm/s: em 0,2 s a demanda é só ~30 Nm, que o fluxo parcial entrega.

Checklist de validação:
1. Tranco em repouso no chão deve cair drasticamente.
2. Lançamento cronometrado antes × depois — não deve haver diferença mensurável.
3. Truque de pista: leve pré-aperto no pedal contra o freio na fila re-fluxa o motor antes do sinal.

Knobs de ajuste empírico:
- **Piso (linha 0 Nm):** ainda treme parado → desce até ~20 A; largada "borrachuda" no primeiro décimo → sobe pra 40–50 A.
- **Joelho (60 Nm):** só mexer se otimizar eficiência/térmica em torque parcial (endurance) — não afeta o tranco.

Bônus: −70 A parados = menos calor no motor/inversor e menos dreno do pack na fila/grid.


