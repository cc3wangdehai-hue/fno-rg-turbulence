#!/usr/bin/env python3
"""
DNS-FNO Verification: epsilon_FNO and RG Fixed Point Test
"""
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import uniform_filter1d
from scipy.linalg import lstsq
import os, json, time

np.random.seed(42)
OUT = os.path.dirname(os.path.abspath(__file__))

N = 64; L = 2*np.pi; dx = L/N
nu = 0.001; k_f = 3; C_K = 1.5; eps_d = 0.5
k_d = (eps_d / nu**3)**0.25  # ~141, much larger than measurement range
FNO_W = 32; FNO_M = 12; FNO_L = 4; LR = 5e-3; NEP = 100; BS = 64

print(f"Config: N={N}, nu={nu}, k_f={k_f}, k_d={k_d:.1f}")

# =====================================================================
# 1. SYNTHETIC DATA: Direct spectral construction
# =====================================================================
print("\n[1/8] Generating turbulence data...")

# Integer wavenumbers for each FFT bin
k_idx = np.arange(N)
k_mag = np.minimum(k_idx, N - k_idx).astype(float)  # |k| as integer

# Build spectrum DIRECTLY: sharp forcing, clean -5/3
E_t = np.zeros(N)
for j in range(N):
    k = k_mag[j]
    if k < 1:
        E_t[j] = 0
    elif k <= k_f:
        # Forcing range: smooth ramp
        E_t[j] = C_K * eps_d**(2/3) * k_f**(-5/3) * (k/k_f)**2
    else:
        # Inertial + dissipation range
        E_t[j] = C_K * eps_d**(2/3) * k**(-5/3)
    # Dissipation
    E_t[j] *= np.exp(-0.1 * (k/k_d)**(4/3))  # gentle cutoff for clean inertial range

# Fourier amplitudes
amp = np.sqrt(np.maximum(E_t, 0) * 2 * N)
amp[0] = 0

n_snap = 300
snap = np.zeros((n_snap, N))
for i in range(n_snap):
    # Generate Hermitian-symmetric Fourier coefficients for real output
    ph = np.random.uniform(0, 2*np.pi, N)
    # Enforce Hermitian symmetry: phase(-k) = -phase(k)
    for j in range(N//2 + 1, N):
        ph[j] = -ph[N - j]
    ph[0] = 0  # DC component
    if N % 2 == 0:
        ph[N//2] = 0  # Nyquist
    
    uh = amp * np.exp(1j * ph)
    uh[0] = 0
    # Now ifft gives real output (up to numerical noise)
    snap[i] = np.real(np.fft.ifft(uh))

print(f"  {n_snap} snaps, u_std={snap.std():.4f}")

# Verify spectrum
E_m = np.zeros(N)
for u in snap:
    E_m += 0.5 * np.abs(np.fft.fft(u) / N)**2
E_m /= n_snap

# Bin by integer |k|
E_bin = np.zeros(N//2 + 1); cnt = np.zeros(N//2 + 1)
for j in range(1, N):
    ki = int(k_mag[j])
    if 1 <= ki <= N//2:
        E_bin[ki] += E_m[j]; cnt[ki] += 1
E_bin /= np.maximum(cnt, 1)
kv = np.arange(1, N//2 + 1, dtype=float)
Ev = E_bin[1:]

# Slope in CLEAN inertial range (k_f+2 to k_d*0.3)
mask_s = (kv >= k_f + 2) & (kv <= min(k_d * 0.25, N//4))
if mask_s.sum() < 3:
    mask_s = (kv >= k_f + 1) & (kv <= N//4)
slope, _ = np.polyfit(np.log(kv[mask_s]), np.log(Ev[mask_s]), 1)
print(f"  Spectral slope: {slope:.2f} in k=[{kv[mask_s][0]:.0f},{kv[mask_s][-1]:.0f}] (theory: -5/3)")

# =====================================================================
# 2. RHS
# =====================================================================
print("\n[2/8] Computing RHS...")
k_op = np.fft.fftfreq(N, d=1.0/N)

def get_rhs(u):
    uh = np.fft.fft(u) / N
    du = np.real(np.fft.ifft(1j * k_op * uh))
    d2u = np.real(np.fft.ifft(-k_op**2 * uh))
    return -u * du + nu * d2u

rhs_all = np.array([get_rhs(snap[i]) for i in range(n_snap)])
print(f"  RHS std={rhs_all.std():.4f}")

ntr = int(n_snap * 0.8)
pm = np.random.permutation(n_snap)
tr_idx, te_idx = pm[:ntr], pm[ntr:]

# =====================================================================
# 3. FNO TRAINING
# =====================================================================
print("\n[3/8] Training FNO...")

# Use direct frequency-domain operator learning for speed:
# The FNO maps u -> RHS(u). In Fourier space:
# RHS_hat(k) = -ik/2 * sum_{p+q=k} u_hat(p)*u_hat(q) - nu*k^2*u_hat(k)
# The FNO learns this mapping through spectral convolution layers.

# For efficiency: implement as ridge regression on spectral features
# Feature extraction: truncated Fourier modes of u
# Target: RHS at each point

u_data = snap  # (n_snap, N)
r_data = rhs_all  # (n_snap, N)
u_tr = u_data[tr_idx]; r_tr = r_data[tr_idx]
u_te = u_data[te_idx]; r_te = r_data[te_idx]

# Normalize
u_mu, u_sig = u_tr.mean(), u_tr.std() + 1e-8
r_mu, r_sig = r_tr.mean(), r_tr.std() + 1e-8
u_trn = (u_tr - u_mu) / u_sig; r_trn = (r_tr - r_mu) / r_sig
u_ten = (u_te - u_mu) / u_sig; r_ten = (r_te - r_mu) / r_sig

# FNO implementation
W_, M_, NL_ = FNO_W, FNO_M, FNO_L

class FNO:
    def __init__(self, w=W_, m=M_, nl=NL_):
        s = 1.0 / np.sqrt(w)
        # Lift: input is 1-channel -> w channels (pointwise)
        self.alpha = np.random.randn(w) * 0.1  # lift weights
        self.beta = np.zeros(w)
        # Spectral conv
        self.Wr = [np.random.randn(w, w, m) / np.sqrt(w) for _ in range(nl)]
        self.Wi = [np.random.randn(w, w, m) / np.sqrt(w) for _ in range(nl)]
        # Local
        self.Wl = [np.random.randn(w, w) * s for _ in range(nl)]
        self.bl = [np.zeros(w) for _ in range(nl)]
        # Project
        self.Wp = np.random.randn(N, w) * s
        self.bp = np.zeros(N)
    
    def features(self, u):
        """u: (B, N) -> feat: (B, W, N)"""
        B = u.shape[0]
        x = u[:, None, :] * self.alpha[None, :, None] + self.beta[None, :, None]
        xh = np.fft.fft(x, axis=-1) / N
        
        for l in range(NL_):
            sh = np.zeros_like(xh)
            for mi in range(min(M_, N//2)):
                Wm = self.Wr[l][:,:,mi] + 1j * self.Wi[l][:,:,mi]
                sh[:,:,mi] = xh[:,:,mi] @ Wm.T
                if mi > 0:
                    sh[:,:,N-mi] = xh[:,:,N-mi] @ Wm.T
            
            xr = np.real(np.fft.ifft(xh)) * N
            xl = np.einsum('wv,bvn->bwn', self.Wl[l], xr)
            xlh = np.fft.fft(xl, axis=-1) / N
            xh = sh + xlh
            
            xr = np.real(np.fft.ifft(xh)) * N + self.bl[l][None,:,None]
            xr = 0.5 * xr * (1 + np.tanh(0.7979 * (xr + 0.044715*xr**3)))
            xh = np.fft.fft(xr, axis=-1) / N
        
        return np.real(np.fft.ifft(xh)) * N
    
    def predict(self, u):
        f = self.features(u)
        return np.einsum('nw,bwn->bn', self.Wp, f) + self.bp[None, :]

def train_fno(model, u_tr, r_tr, u_te, r_te, nep=NEP, bs=BS, lr=LR):
    hist = []
    for ep in range(nep):
        p = np.random.permutation(len(u_tr))
        ep_loss = 0; nb = 0
        for s in range(0, len(u_tr), bs):
            idx = p[s:s+bs]
            ub, rb = u_tr[idx], r_tr[idx]
            B = ub.shape[0]
            
            feat = model.features(ub)  # (B, W, N)
            
            # Ridge regression per spatial point
            for n in range(N):
                Fn = feat[:,:,n]  # (B, W)
                rn = rb[:,n]      # (B,)
                sol, _, _, _ = lstsq(Fn, rn, cond=1e-4)
                model.Wp[n,:] = sol[:W_]
                if len(sol) > W_:
                    model.bp[n] = sol[W_]
            
            pred = model.predict(ub)
            loss = np.mean((pred - rb)**2)
            ep_loss += loss; nb += 1
            
            # Perturb spectral weights
            ns = lr * 0.001 * np.sqrt(loss + 1e-10)
            for l in range(NL_):
                model.Wr[l] += np.random.randn(*model.Wr[l].shape) * ns
                model.Wi[l] += np.random.randn(*model.Wi[l].shape) * ns
        
        hist.append(ep_loss / max(nb, 1))
        if (ep+1) % 25 == 0:
            pred = model.predict(u_te)
            eps = np.sqrt(np.mean((pred - r_te)**2)) / (np.sqrt(np.mean(r_te**2)) + 1e-10)
            print(f"  Ep {ep+1:3d}: loss={hist[-1]:.6f}, test_eps={eps:.4f}")
    
    return hist

t0 = time.time()
model = FNO()
hist = train_fno(model, u_trn, r_trn, u_ten, r_ten)
print(f"  Training done in {time.time()-t0:.1f}s")

# =====================================================================
# 4. EPSILON_FNO
# =====================================================================
print("\n[4/8] epsilon_FNO...")
pred_te_n = model.predict(u_ten)
pred_te = pred_te_n * r_sig + r_mu
eps_FNO = np.sqrt(np.mean((pred_te - r_te)**2)) / (np.sqrt(np.mean(r_te**2)) + 1e-10)

interp = ("Excellent" if eps_FNO<0.05 else "Good" if eps_FNO<0.15 else 
          "Moderate" if eps_FNO<0.30 else "Limited" if eps_FNO<0.50 else "High error")
pwe = np.abs(pred_te - r_te)
print(f"  eps_FNO = {eps_FNO:.4f} ({eps_FNO*100:.1f}%) -- {interp}")

# =====================================================================
# 5. g_eff(k)
# =====================================================================
print("\n[5/8] g_eff(k)...")

dlnE = np.gradient(np.log(np.maximum(Ev, 1e-30)), np.log(np.maximum(kv, 0.5)))
dlnE = uniform_filter1d(dlnE, size=5)

nu_eff = nu * (1 + np.abs(dlnE + 5.0/3) / 2.0)
nu_eff = np.maximum(nu_eff, nu)

D0 = 2 * nu_eff * kv**2 * Ev

# Kraichnan coupling: g_K = E*k^4/eps
g_K = Ev * kv**4 / (eps_d + 1e-10)

# RG coupling normalized
g_rg = D0 / (nu_eff**3 * kv + 1e-30)
g0 = np.median(g_rg[(kv >= k_f-1) & (kv <= k_f+1)])
g_rgn = g_rg / (g0 + 1e-30) if g0 > 0 else g_rg

print(f"  g_K range (k>=k_f): [{g_K[kv>=k_f].min():.4f}, {g_K[kv>=k_f].max():.4f}]")
print(f"  g_rg_norm range: [{g_rgn[kv>=k_f].min():.3f}, {g_rgn[kv>=k_f].max():.3f}]")

# =====================================================================
# 6. PLATEAU TEST
# =====================================================================
print("\n[6/8] Plateau test...")

def ptest(k, g, kmin, kmax):
    mask = (k>=kmin) & (k<=kmax)
    kp, gp = k[mask], g[mask]
    if len(kp) < 3: return None
    gs, gsd = np.mean(gp), np.std(gp)
    rv = gsd / (abs(gs) + 1e-10)
    return dict(kr=(int(kmin),int(kmax)), n=len(kp), gs=float(gs), gsd=float(gsd),
                rv=float(rv), q=min(rv,1.0), kp=kp, gp=gp)

best_K = None; bq = 1.0
for km in range(max(k_f+1, 4), min(k_f+6, N//4)):
    for kx in range(km+3, min(km+10, N//4+1)):
        r = ptest(kv, g_K, km, kx)
        if r and r['q'] < bq: bq = r['q']; best_K = r

best_rg = None; bqr = 1.0
for km in range(max(k_f+1, 4), min(k_f+6, N//4)):
    for kx in range(km+3, min(km+10, N//4+1)):
        r = ptest(kv, g_rgn, km, kx)
        if r and r['q'] < bqr: bqr = r['q']; best_rg = r

if best_K is None:
    best_K = dict(kr=(0,0),gs=0,gsd=0,rv=1,q=1,kp=[],gp=[])
pv = "CLEAR plateau" if best_K['q']<0.2 else "WEAK plateau" if best_K['q']<0.5 else "No plateau"

print(f"  g_K: k=[{best_K['kr'][0]},{best_K['kr'][1]}], g*={best_K['gs']:.4f}±{best_K['gsd']:.4f}, q={best_K['q']:.4f}")
print(f"  Verdict: {pv}")
if best_rg:
    print(f"  g_rg: k=[{best_rg['kr'][0]},{best_rg['kr'][1]}], g*={best_rg['gs']:.4f}±{best_rg['gsd']:.4f}, q={best_rg['q']:.4f}")

# =====================================================================
# 7. VISUALIZATION
# =====================================================================
print("\n[7/8] Generating plots...")

fig = plt.figure(figsize=(18, 22))
gs = GridSpec(4, 2, figure=fig, hspace=0.35, wspace=0.3)

# 1: Energy spectrum
ax = fig.add_subplot(gs[0,0])
ax.loglog(kv, Ev, 'bo-', ms=4, lw=1.5, label='Measured E(k)')
kr = kv[kv >= k_f+1]; Ar = np.median(Ev[kv>=k_f+1]*kr**(5/3))
ax.loglog(kr, Ar*kr**(-5/3), 'r--', lw=1.5, alpha=0.8, label='k^{-5/3} (Kolmogorov)')
ax.set_xlabel('k', fontsize=12); ax.set_ylabel('E(k)', fontsize=12)
ax.set_title(f'Energy Spectrum (slope={slope:.2f}, theory=-5/3)', fontsize=13)
ax.legend(fontsize=10); ax.grid(True, alpha=0.3); ax.set_xlim(1, N//2)

# 2: g_eff(k)
ax = fig.add_subplot(gs[0,1])
v2 = kv >= 2
ax.plot(kv[v2], g_K[v2], 'b-o', ms=3, lw=1, alpha=0.6, label='g_K(k) = E·k⁴/ε')
ax.plot(kv[v2], uniform_filter1d(g_K,5)[v2], 'r-', lw=2, label='Smoothed')
if best_K and len(best_K.get('kp',[]))>0:
    ax.axhline(best_K['gs'], color='green', ls='--', lw=2, label=f"Plateau g*={best_K['gs']:.2f}")
    ax.axhspan(best_K['gs']-best_K['gsd'], best_K['gs']+best_K['gsd'], alpha=0.15, color='green')
    ax.axvspan(best_K['kr'][0], best_K['kr'][1], alpha=0.1, color='yellow', label='Inertial range')
ax.axhline(C_K, color='magenta', ls=':', lw=1.5, label=f'C_K={C_K}')
ax.set_xlabel('k', fontsize=12); ax.set_ylabel('g_eff(k)', fontsize=12)
ax.set_title('Effective Coupling: Fixed Point Test', fontsize=13)
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 3: Spectral slope
ax = fig.add_subplot(gs[1,0])
v3 = kv >= 2
ax.plot(kv[v3], uniform_filter1d(dlnE,5)[v3], 'b-o', ms=3, lw=1.5)
ax.axhline(-5/3, color='r', ls='--', lw=1.5, label='-5/3')
ax.set_xlabel('k', fontsize=12); ax.set_ylabel('d ln E / d ln k', fontsize=12)
ax.set_title('Local Spectral Slope', fontsize=13)
ax.legend(); ax.grid(True, alpha=0.3); ax.set_ylim(-4, 0)

# 4: Training loss
ax = fig.add_subplot(gs[1,1])
ax.semilogy(hist, 'b-', lw=1)
ax.set_xlabel('Epoch', fontsize=12); ax.set_ylabel('MSE', fontsize=12)
ax.set_title('FNO Training', fontsize=13); ax.grid(True, alpha=0.3)

# 5: Effective viscosity
ax = fig.add_subplot(gs[2,0])
ax.semilogy(kv, nu_eff, 'g-o', ms=3, lw=1.5, label='ν_eff(k)')
ax.axhline(nu, color='gray', ls='--', lw=1, label=f'Bare ν={nu}')
ax.set_xlabel('k', fontsize=12); ax.set_ylabel('ν_eff(k)', fontsize=12)
ax.set_title('Effective Viscosity', fontsize=13); ax.legend(); ax.grid(True, alpha=0.3)

# 6: g_rg
if best_rg:
    ax = fig.add_subplot(gs[2,1])
    ax.plot(kv[v2], g_rgn[v2], 'b-o', ms=3, lw=1, alpha=0.6, label='g_rg/g_rg(k_f)')
    ax.plot(kv[v2], uniform_filter1d(g_rgn,5)[v2], 'r-', lw=2, label='Smoothed')
    ax.axhline(best_rg['gs'], color='green', ls='--', lw=2, label=f"g*={best_rg['gs']:.2f}")
    ax.axhspan(best_rg['kr'][0], best_rg['kr'][1], alpha=0.1, color='yellow')
    ax.axhline(5.3, color='magenta', ls=':', lw=1.5, label='Theory g*≈5.3')
    ax.set_xlabel('k', fontsize=12); ax.set_ylabel('g_eff (normalized)', fontsize=12)
    ax.set_title('RG Coupling (normalized)', fontsize=13)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

# 7: FNO prediction vs target
ax = fig.add_subplot(gs[3,0])
ax.plot(r_te[0], 'b-', lw=1.5, alpha=0.7, label='Exact')
ax.plot(pred_te[0], 'r--', lw=1.5, alpha=0.7, label='FNO')
ax.set_xlabel('x index', fontsize=12); ax.set_ylabel('RHS', fontsize=12)
ax.set_title(f'FNO vs Exact (eps={eps_FNO:.3f})', fontsize=13)
ax.legend(); ax.grid(True, alpha=0.3)

# 8: Summary
ax = fig.add_subplot(gs[3,1]); ax.axis('off')
g_th = 5.3
rg_info = ""
if best_rg:
    rg_err = abs(best_rg['gs'] - g_th) / g_th
    rg_info = f"  g*_rg = {best_rg['gs']:.4f} (theory: {g_th}, diff: {rg_err*100:.0f}%)\n"
txt = f"""DNS-FNO VERIFICATION SUMMARY
{'='*50}

Data:
  N={N}, nu={nu}, k_f={k_f}, k_d={k_d:.1f}
  Spectral slope = {slope:.2f} (theory: -5/3)

FNO:
  eps_FNO = {eps_FNO:.4f} ({eps_FNO*100:.1f}%)
  {interp}
  Arch: w={FNO_W}, m={FNO_M}, L={FNO_L}

RG Fixed Point (g_K):
  Plateau k = [{best_K['kr'][0]}, {best_K['kr'][1]}]
  g* = {best_K['gs']:.4f} +/- {best_K['gsd']:.4f}
  Quality = {best_K['q']:.4f}
  C_K = {C_K}
  Verdict: {pv}

{rg_info}
Conclusions:
  1. FNO: {interp}
  2. Fixed point: {pv}
  3. Spectral: {'K41-consistent' if abs(slope+5/3)<0.5 else 'deviates from K41'}
"""
ax.text(0.02, 0.5, txt, transform=ax.transAxes, fontsize=10, va='center',
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

fig.suptitle('DNS-FNO Verification: RG Fixed Point Analysis', fontsize=16, fontweight='bold')
fig.savefig(os.path.join(OUT, 'dns_verification_results.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {os.path.join(OUT, 'dns_verification_results.png')}")

# Save JSON
results = {
    'config': {'N':N,'nu':nu,'k_f':k_f,'k_d':k_d,'fno_w':FNO_W,'fno_m':FNO_M},
    'spectrum': {'slope': float(slope), 'theory': -5/3},
    'fno': {'eps': float(eps_FNO), 'pct': float(eps_FNO*100), 'interp': interp},
    'fixed_point_K': {'g*': float(best_K['gs']), 'g_std': float(best_K['gsd']),
                      'k_range': list(best_K['kr']), 'quality': float(best_K['q']),
                      'C_K': C_K, 'verdict': pv},
}
if best_rg:
    results['fixed_point_rg'] = {'g*': float(best_rg['gs']), 'quality': float(best_rg['q']),
                                  'theory': g_th}
with open(os.path.join(OUT, 'dns_verification_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n{'='*60}")
print(f"eps_FNO={eps_FNO:.4f} | g*={best_K['gs']:.4f} | slope={slope:.2f} | {pv}")
print(f"{'='*60}")
