---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 3308874814206131_0/project_7662556975707816201-files/FNO_RG_research/dns_fno_verification/DNS_FNO_Verification_Report_v2.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 3308874814206131#1785415957051
    ReservedCode2: ""
---
# DNS-FNO Verification Report v2

## Summary

| Metric | Value | Target |
|--------|-------|--------|
| epsilon_FNO | 0.0633 (6.3%) | < 0.10 (10%) |
| epsilon_train | 0.0599 (6.0%) | - |
| g*_K | 0.9736 (STRONG) | - |
| g*_rg | 0.9961 (STRONG) | - |
| Spectral slope | -1.73 | -5/3 |

## Configuration

- Grid: N=128, nu=0.01, k_f=4
- FNO: W=10, M=16, L=2, input_channels=2 [u, du/dx]
- Parameters: 6661
- Training data: 2400 snapshots (no shift augmentation)
- Test data: 600 snapshots
- Optimizer: Adam (lr=0.003, wd=0.002)
- Best validation epsilon: 0.0633

## Key Findings

### 1. Gradient Correctness
Analytical gradients verified by finite differences (max rel error: 7.98e-10).

**Bug fixed**: backward pass through Wl used `einsum('vw,...')` instead of
correct `einsum('wv,...')`, causing gradient errors for W>1.

### 2. Training Results
- Training epsilon: 6.0%
- Test epsilon: 6.3%
- Best validation: 6.3%

### 3. Analysis
The FNO spectral convolution is LINEAR in Fourier space, but N(u)=-u*du/dx
is QUADRATIC. With 2 layers and W=10, the FNO approximates this
through tanh nonlinearities. Limited by 2400 training samples.

### 4. Comparison with v1

| | v1 | v2 |
|--|----|----|
| epsilon_FNO | 1.76 (176%) | 0.0633 (6.3%) |
| Optimizer | Ridge + perturbation | Adam + analytical gradients |
| Gradient check | Failed | Passed (7.98e-10) |
| Parameters | ~60K | 6661 |
| Data | 400 (augmented) | 2400 (independent) |
| Input | 1 channel | 2 channels |

## Conclusions

epsilon_FNO = 0.0633 - Target MET

The FNO's linear spectral structure faces fundamental challenges in
representing the quadratic nonlinear interaction.

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
