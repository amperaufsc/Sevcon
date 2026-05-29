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

| Parâmetro | Configurado | Por quê |
|---|---|---|
| Im min = Im max | **102.4 A** | Im é fixo em 102.4 A (seção 2.3), então o map cobre apenas esse ponto |

### 2.8 Speed Limits (cadeia em camadas)

| Parâmetro | Configurado | Por quê |
|---|---|---|
| Local Motor Limits → Max motor speed | **6000 RPM mech** | S2 max do motor |
| Overspeed Limit [0x4624,0] | **7200 RPM mech** | Trip duro. Margem 20% sobre Max motor speed pra absorver o erro do encoder (modulação ±29% por phase shift ±20°) |

