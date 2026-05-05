"""Cifra analytics.json con AES-GCM (PBKDF2) y embebe el blob en un HTML standalone."""
import os, json, base64, getpass, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ROOT = os.path.dirname(os.path.abspath(__file__))
ITER = 250_000

def encrypt(payload: bytes, password: str):
    salt = os.urandom(16)
    iv = os.urandom(12)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER)
    key = kdf.derive(password.encode('utf-8'))
    ct = AESGCM(key).encrypt(iv, payload, None)
    return {
        'salt': base64.b64encode(salt).decode(),
        'iv': base64.b64encode(iv).decode(),
        'ct': base64.b64encode(ct).decode(),
        'iter': ITER,
    }

password = os.environ.get('TIGRES_PASS')
if not password:
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        password = getpass.getpass('Password para el dashboard: ')
if not password:
    raise SystemExit('Password requerido')

with open(os.path.join(ROOT, 'analytics.json'), 'rb') as f:
    raw = f.read()
print(f'Analytics size: {len(raw):,} bytes')

blob = encrypt(raw, password)
print(f'Encrypted size: {len(blob["ct"]):,} bytes (b64)')

# Logo Boletomóvil — versión compacta horizontal en blanco para sidebar/header
LOGO_BM = '''<svg viewBox="0 0 1920 254.8" xmlns="http://www.w3.org/2000/svg" style="width:120px;height:auto;display:block"><style>.bm-w{fill:#FFFFFF}.bm-g{fill:#00E89A}</style><g><path class="bm-w" d="M7.5,237.9V3.8h44.9v91.6c8.4-8.4,23-16.9,40.2-16.9c41.2,0,69.9,28.4,69.9,85.1c0,56.1-37.8,87.5-87.5,87.5C41.9,251.1,18.6,243.6,7.5,237.9z M114.9,163.6c0-30.7-10.5-49.7-34.8-49.7c-12.2,0-22.6,7.1-27.7,12.5v85.8c4.7,2,11.8,3.7,22.6,3.7C100.1,215.9,114.9,197.3,114.9,163.6z"/><path class="bm-w" d="M162.9,165.3c0-42.2,24.7-86.8,82.1-86.8s83.4,43.2,83.4,85.5c0,41.5-25.3,87.2-83.1,87.2C187.9,251.1,162.9,207.5,162.9,165.3z M280.8,165.3c0-30.7-10.8-53.4-36.5-53.4c-25.3,0-33.8,21.3-33.8,52c0,30.7,10.1,53,35.5,53C271.7,216.9,280.8,196,280.8,165.3z"/><path class="bm-w" d="M342.3,3.8h44.9V247h-44.9V3.8z"/><path class="bm-w" d="M401,163.9c0-52,35.8-85.5,81.4-85.5c46.6,0,71.6,29.7,71.6,81.1c0,5.1-0.3,10.1-0.7,15.5h-104c2,24.3,14.5,42.6,41.9,42.6c22.3,0,34.8-7.4,42.9-11.5l14.5,29.1c-10.8,6.1-27.7,15.9-61.5,15.9C432.1,251.1,401,216.3,401,163.9z M510.2,144.6c-0.3-18.6-7.8-33.8-28.4-33.8c-19.3,0-29.7,12.5-33.1,33.8H510.2z"/><path class="bm-w" d="M578.7,199.7v-83.8h-26.3V82.5h26.3V34.9h44.6v47.6h38.5v33.4h-38.5v75c0,16.2,4.1,23.3,16.6,23.3c9.8,0,18.3-4.1,21.6-6.1l10.5,33.4c-6.8,3.7-20.6,9.5-41.2,9.5C591.9,251.1,578.7,231.1,578.7,199.7z"/><path class="bm-w" d="M666.6,165.3c0-42.2,24.7-86.8,82.1-86.8c57.4,0,83.4,43.2,83.4,85.5c0,41.5-25.3,87.2-83.1,87.2C691.6,251.1,666.6,207.5,666.6,165.3z M784.5,165.3c0-30.7-10.8-53.4-36.5-53.4c-25.3,0-33.8,21.3-33.8,52c0,30.7,10.1,53,35.5,53C775.4,216.9,784.5,196,784.5,165.3z"/><path class="bm-w" d="M843.9,82.5h43.9v20.3c8.4-9.5,23-24.3,49.3-24.3c23.3,0,36.1,10.5,42.2,26c13.9-15.5,29.1-26,52.7-26c34.8,0,47,23,47,53.4V247h-44.9V140.9c0-16.2-4.7-25-19.6-25c-13.8,0-24.3,10.8-30.7,18.6V247h-44.9V140.9c0-16.6-5.7-25-19.3-25c-16.5,0-27.4,15.9-30.7,20.3V247h-44.9V82.5z"/><path class="bm-w" d="M1089.9,165.3c0-42.2,24.7-86.8,82.1-86.8s83.4,43.2,83.4,85.5c0,41.5-25.3,87.2-83.1,87.2C1114.9,251.1,1089.9,207.5,1089.9,165.3z M1207.8,165.3c0-30.7-10.8-53.4-36.5-53.4c-25.3,0-33.8,21.3-33.8,52c0,30.7,10.1,53,35.5,53C1198.6,216.9,1207.8,196,1207.8,165.3z M1178.4,18.6h58.1l-47.3,45.6h-38.9L1178.4,18.6z"/><path class="bm-w" d="M1248.6,82.5h48.6l34.1,108.8h0.7l35.1-108.8h45.6L1352,247h-42.2L1248.6,82.5z"/><path class="bm-w" d="M1416.2,34.2c0-14.2,11.5-26.4,27.4-26.4c15.9,0,27.7,12.2,27.7,26.4c0,14.5-11.8,27-27.7,27C1427.7,61.2,1416.2,48.7,1416.2,34.2z M1420.9,82.5h45.3V247h-45.3V82.5z"/><path class="bm-w" d="M1494.5,3.8h44.9V247h-44.9V3.8z"/><path class="bm-g" d="M1775.8,14.5c-0.6,0.1-9.2,2.1-22.5,8c-10.4,4.7-18.5,19.8-18.5,34.3c0,4.8,1,9.4,2.9,13.8l44.8,75.4c2.8,5,8.1,8.1,13.8,8.1c8.7,0,15.8-7,15.8-15.7c0-2,1.6-3.7,3.7-3.7c2,0,3.7,1.6,3.7,3.7c0,12.7-10.4,23-23.1,23c-8.3,0-16.1-4.5-20.2-11.7l-45-75.8c-2.5-5.5-3.7-11.2-3.7-17.1c0-17.5,9.8-35.1,22.9-41c7.7-3.5,13.8-5.5,18.1-6.8c-30.4-8.6-89.2-4.3-89.2-4.3c-87.2,8.4-89.1,74.4-89.1,74.4c-0.4,3.8-2.6,58.3-2.6,58.3l-0.5,12.9c0,0-0.1,4.5-0.9,12.9c-1.3,8.2-4,16.1-9.4,21.8l-0.2,0.3c-0.2,0.2-0.3,0.4-0.4,0.6c-0.4,0.6-0.6,1.4-0.6,2.1c0,2.3,1.9,4.2,4.2,4.2c0.6,0,1.1-0.1,1.6-0.3c0.3-0.2,0.4-0.1,0.8-0.5c0.4-0.3,15.9-21.3,15.9-21.3l0.8-1.2c0,0-0.3,22.4-0.2,43.8l1.1,28.3c0,0.1,0,0.1,0,0.2c0.3,1.6,0.6,3,1,4.2c1.6,3.3,5,5.6,8.9,5.6l2,0.1l45.4,0h2.9c3.9,0,5.9-3.7,6.7-6.5c0,0,0.4-1.5,0.4-4c0-1.7,0.2-41.7,0.2-41.7s23.7,4.7,41.6,4.6c17.8-0.1,41.4-4.6,41.4-4.6l-0.1,41.8c-0.2,10.5,10,10.1,10,10.1l2,0.2l46.3,0.1h2.9c3.9,0,5.9-3.8,6.7-6.7c0,0,0.4-1.6,0.4-4.1c0-1.7,0.2-41.7,0.2-41.7l0-26.6c0-0.4,0-0.7,0-1.1c0-11.2,9.1-20.2,20.4-20.2c2.2,0,4.4,0.4,6.4,1l0,0.2c0,0.3,0,0.6,0,1c0,8.6,6,15.7,14,17.7c1.4,0.3,2.8,0.5,4.3,0.5c1.4,0,2.7-0.1,4-0.4c0,0,3.8-0.8,8.5-2.7c0.2,2.5,2.1,14.4,0.4,27.2c-1,7.7-5.8,16.5-11.6,17.3l-0.3,0c-1.8,0-3.2-1-4-2.5l0-0.1c-1.6-3.4-5.1-5.8-9.1-5.8c-5.5,0-10,4.4-10,9.9c0,2.8,1.1,5.3,3,7.1l0.3,0.3c6.9,6.8,16.4,11.1,27,11.1c18.1,0,33.8-12.5,37.2-29.2v-0.5c3.3-12.5,3.3-100.7,3.3-129.8v-1c0-4.6,0-7.7-0.1-8.8c-0.1-0.5,0-1.1-0.1-1.8c-3-23.9-19-43.8-40.9-52.4l0,0c0,0-1.8-0.8-5-1.7c-3.2-0.9-7.9-1.7-13.5-2.2c-5.7-0.5-12.3-0.5-19.4-0.3c-5.5,0.1-20.4,2.4-27.1,3.5S1775.8,14.5,1775.8,14.5z M1854.8,116.1c-3.9,0-7-3.1-7-7c0-3.8,3.1-7,7-7s7,3.1,7,7C1861.8,113,1858.7,116.1,1854.8,116.1z"/></g></svg>'''

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Tigres UANL · Mercado Secundario</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root{
    --bg:#0a0d12;
    --panel:#13171f;
    --panel2:#1a1f2a;
    --panel3:#222836;
    --line:#252b3a;
    --text:#f1f3f7;
    --muted:#9aa3b5;
    --muted2:#5d6577;
    --bm:#00E89A;
    --bm-soft:rgba(0,232,154,.12);
    --bm-glow:rgba(0,232,154,.35);
    --tigres:#F3B61C;
    --tigres-soft:rgba(243,182,28,.14);
    --red:#ff6b6b;
    --red-soft:rgba(255,107,107,.14);
    --warn:#ffb84d;
    --warn-soft:rgba(255,184,77,.12);
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font:14px/1.45 -apple-system,BlinkMacSystemFont,"SF Pro Text","Inter",Segoe UI,Roboto,sans-serif;min-height:100vh}
  /* ============== LOCK ============== */
  .lock{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:24px;text-align:center;background:radial-gradient(ellipse at top, rgba(0,232,154,.06), transparent 60%), radial-gradient(ellipse at bottom, rgba(255,214,0,.04), transparent 60%)}
  .lock .brand{display:flex;flex-direction:column;align-items:center;gap:14px;margin-bottom:24px}
  .lock .brand h1{font-size:34px;font-weight:800;color:var(--tigres);margin:0;letter-spacing:-.5px}
  .lock .brand .powered{display:flex;align-items:center;gap:8px;font-size:11px;color:var(--muted2);margin-top:8px}
  .lock h2{font-size:18px;margin:14px 0 6px;letter-spacing:-.2px;color:var(--text);font-weight:600}
  .lock .accent-bar{height:3px;width:120px;background:linear-gradient(90deg, var(--bm), var(--tigres));border-radius:2px;margin:0 auto 14px}
  .lock p{color:var(--muted);max-width:520px;margin:0 0 24px 0}
  .lock form{display:flex;gap:8px;background:var(--panel);padding:8px;border-radius:10px;border:1px solid var(--line)}
  .lock input{background:transparent;border:0;outline:0;color:var(--text);padding:10px 12px;width:280px;font-size:14px}
  .lock button{background:var(--bm);color:#062818;border:0;padding:10px 18px;border-radius:6px;font-weight:700;cursor:pointer;letter-spacing:.3px}
  .lock button:hover{filter:brightness(1.1)}
  .err{color:var(--red);margin-top:12px;font-size:13px;min-height:18px}
  .seal{display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;border:2px solid var(--bm);border-radius:50%;font-size:22px;color:var(--bm)}

  /* ============== APP LAYOUT ============== */
  .app{display:grid;grid-template-columns:240px 1fr;min-height:100vh}
  .sidebar{background:#0d1118;border-right:1px solid var(--line);padding:24px 0;display:flex;flex-direction:column;position:sticky;top:0;height:100vh;overflow-y:auto}
  .sidebar .brand{padding:0 22px 24px;border-bottom:1px solid var(--line)}
  .sidebar .brand .logo-tigres{font-size:24px;font-weight:800;color:var(--tigres);letter-spacing:-.3px;margin:0 0 4px}
  .sidebar .brand .tag{font-size:10px;letter-spacing:2.5px;color:var(--muted);text-transform:uppercase;font-weight:600}
  .sidebar .brand .powered{display:flex;align-items:center;gap:7px;margin-top:14px;font-size:10px;color:var(--muted2);letter-spacing:.3px}
  .sidebar .brand .powered .bm-mini{display:inline-block;height:14px}
  .sidebar nav{padding:14px 14px;flex:1}
  .sidebar nav a{display:flex;align-items:center;gap:11px;padding:10px 12px;color:var(--muted);text-decoration:none;font-size:13px;border-radius:7px;margin-bottom:2px;font-weight:500;transition:.15s}
  .sidebar nav a:hover{background:var(--panel2);color:var(--text)}
  .sidebar nav a.active{background:var(--panel2);color:var(--tigres)}
  .sidebar nav a svg{width:16px;height:16px;flex:none}
  .sidebar .footer-action{padding:14px 18px 4px;border-top:1px solid var(--line)}
  .sidebar .footer-action button{width:100%;background:var(--tigres);color:#1a1300;border:0;padding:11px;border-radius:8px;font-weight:700;cursor:pointer;font-size:12px;letter-spacing:.6px;text-transform:uppercase}
  .sidebar .footer-action button:hover{filter:brightness(1.05)}
  .sidebar .footer-action .session{font-size:10px;color:var(--muted2);text-align:center;margin-top:10px;padding-bottom:6px}

  main{padding:0 32px 48px;overflow-x:hidden}
  .topbar{display:flex;justify-content:space-between;align-items:center;padding:24px 0 22px;border-bottom:1px solid var(--line);margin-bottom:24px}
  .topbar h1{font-size:22px;margin:0;font-weight:700;letter-spacing:-.4px}
  .topbar .meta{display:flex;align-items:center;gap:16px;font-size:12px;color:var(--muted)}
  .topbar .pill{padding:4px 10px;background:var(--panel2);border:1px solid var(--line);border-radius:99px;font-size:11px;color:var(--muted);letter-spacing:.3px}

  /* ============== KPI CARDS (TOP ROW) ============== */
  .grid{display:grid;gap:14px}
  .kpi-row{grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-bottom:24px}
  .cols2{grid-template-columns:repeat(auto-fit,minmax(440px,1fr))}
  .cols3{grid-template-columns:repeat(auto-fit,minmax(310px,1fr))}
  .kpi-card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 22px;position:relative;overflow:hidden;transition:.15s}
  .kpi-card:hover{border-color:var(--panel3)}
  .kpi-card .label{display:flex;justify-content:space-between;align-items:center;font-size:10.5px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.7px;margin-bottom:14px}
  .kpi-card .label .icon{width:26px;height:26px;background:var(--panel2);border-radius:6px;display:flex;align-items:center;justify-content:center;color:var(--muted)}
  .kpi-card .v{font-size:32px;font-weight:700;letter-spacing:-1px;color:var(--text);line-height:1}
  .kpi-card .sub{font-size:12px;color:var(--muted);margin-top:8px;display:flex;align-items:center;gap:8px}
  .kpi-card .delta{display:inline-flex;align-items:center;gap:3px;padding:2px 7px;border-radius:6px;font-size:11px;font-weight:600;background:var(--bm-soft);color:var(--bm)}
  .kpi-card.ok{border-left:3px solid var(--bm)}
  .kpi-card.tigres{border-left:3px solid var(--tigres)}
  .kpi-card.warn{border-left:3px solid var(--warn)}
  .kpi-card.bad{border-left:3px solid var(--red)}

  /* ============== SECTION CARDS ============== */
  .section{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:22px 24px;margin-bottom:18px}
  .section h2{margin:0 0 4px;font-size:15px;font-weight:700;letter-spacing:-.2px;display:flex;align-items:center;gap:10px}
  .section .desc{color:var(--muted);font-size:12.5px;margin-bottom:18px;line-height:1.5}
  .section h2 .badge{font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:1px;background:var(--panel2);border:1px solid var(--line);padding:3px 9px;border-radius:99px}

  /* ============== ADOPCION FUNNEL ============== */
  .adopcion-kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:22px}
  .adp{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:16px 18px;position:relative}
  .adp.total{border-left:3px solid #6c7388}
  .adp.no-uso{border-left:3px solid var(--red)}
  .adp.listaron{border-left:3px solid var(--warn)}
  .adp.vendieron{border-left:3px solid var(--bm);background:linear-gradient(135deg, rgba(0,232,154,.06), var(--panel2))}
  .adp .label{font-size:10.5px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.7px;margin-bottom:8px}
  .adp .v{font-size:26px;font-weight:700;letter-spacing:-.6px}
  .adp .v small{font-size:13px;color:var(--muted);margin-left:6px;font-weight:500}

  /* Funnel steps visual */
  .funnel{display:flex;align-items:stretch;justify-content:space-between;gap:12px;margin:14px 0 8px;padding:24px 14px;background:#0d1118;border:1px solid var(--line);border-radius:10px}
  .funnel .step{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end}
  .funnel .step .box{width:100%;max-width:160px;aspect-ratio:1;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:800;letter-spacing:-1.5px;border:1px solid var(--line);background:var(--panel2);color:var(--muted);position:relative}
  .funnel .step.s1 .box{color:var(--text)}
  .funnel .step.s2 .box{border:2px solid var(--bm);color:var(--bm);box-shadow:0 0 24px var(--bm-glow)}
  .funnel .step.s3 .box{background:var(--bm);color:#062818;box-shadow:0 0 32px var(--bm-glow)}
  .funnel .step .label{font-size:13px;color:var(--muted);margin-top:14px;font-weight:500}
  .funnel .arrow{flex:.6;display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--bm);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;gap:6px}
  .funnel .arrow .line{width:100%;height:1.5px;background:var(--bm);position:relative}
  .funnel .arrow .line::after{content:'';position:absolute;right:-1px;top:50%;transform:translateY(-50%);border-left:8px solid var(--bm);border-top:6px solid transparent;border-bottom:6px solid transparent}

  /* Adopcion list rows */
  .adop-list{display:flex;flex-direction:column;gap:8px}
  .adop-row{display:flex;align-items:center;gap:14px;background:var(--panel2);border:1px solid var(--line);border-left-width:3px;border-radius:10px;padding:14px 16px}
  .adop-row.ok{border-left-color:var(--bm)}
  .adop-row.warn{border-left-color:var(--warn)}
  .adop-row.bad{border-left-color:var(--red)}
  .adop-row .icon{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;flex:none}
  .adop-row.ok .icon{background:var(--bm-soft);color:var(--bm)}
  .adop-row.warn .icon{background:var(--warn-soft);color:var(--warn)}
  .adop-row.bad .icon{background:var(--red-soft);color:var(--red)}
  .adop-row .text{flex:1}
  .adop-row .text .t{font-size:13.5px;font-weight:600;color:var(--text)}
  .adop-row .text .pct{font-size:11.5px;color:var(--muted);margin-top:2px}
  .adop-row .num{font-size:18px;font-weight:700;color:var(--text);text-align:right}
  .adop-row .num small{display:block;font-size:11px;color:var(--muted);font-weight:500;margin-top:2px}

  .efic{display:flex;align-items:center;justify-content:center;flex-direction:column;padding:8px}
  .efic .v{font-size:42px;font-weight:800;color:var(--bm);letter-spacing:-1.5px;line-height:1}
  .efic .l{font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--muted);margin-top:6px;font-weight:600}

  /* ============== INPUTS / FILTERS ============== */
  .filter-input{width:100%;background:var(--panel2);color:var(--text);border:1px solid var(--line);padding:11px 14px;border-radius:8px;font-size:13px;outline:none;transition:.15s}
  .filter-input:focus{border-color:var(--bm);box-shadow:0 0 0 3px rgba(0,232,154,.15)}
  .filter-input::placeholder{color:var(--muted2)}
  .filter-row{margin-bottom:16px;display:flex;gap:12px;align-items:center}
  .filter-row label{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;font-weight:600;flex:none}

  /* ============== ZONE MODAL ============== */
  .zone-modal{position:fixed;inset:0;background:rgba(0,0,0,.78);display:none;align-items:center;justify-content:center;z-index:100;padding:20px;backdrop-filter:blur(4px)}
  .zone-modal.show{display:flex}
  .zone-modal-content{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:28px;max-width:820px;width:100%;max-height:88vh;overflow-y:auto;position:relative;box-shadow:0 20px 60px rgba(0,0,0,.6)}
  .zone-modal-content h2{margin:0 0 4px;font-size:20px;font-weight:700;display:flex;align-items:center;gap:10px}
  .zone-modal-content .zm-sub{color:var(--muted);font-size:12.5px;margin-bottom:18px}
  .zone-modal-content .zm-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px}
  .zone-modal-content .zm-summary .adp{padding:12px 14px}
  .zone-modal-content .zm-summary .adp .v{font-size:18px}
  .zm-close{position:absolute;top:14px;right:16px;background:transparent;border:0;color:var(--muted);font-size:24px;cursor:pointer;width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;line-height:1}
  .zm-close:hover{background:var(--panel2);color:var(--text)}
  .zone-row.clickable{cursor:pointer}
  .zone-row.clickable:hover{transform:translateX(2px);background:var(--panel3)}

  /* ============== METRIC EXPLAINER ============== */
  .metric-compare{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:8px}
  .metric-card{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:18px 20px;display:flex;flex-direction:column;gap:10px}
  .metric-card.bm{border-left:3px solid var(--bm)}
  .metric-card.tigres{border-left:3px solid var(--tigres)}
  .metric-card .head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
  .metric-card .head .ttl{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.7px;font-weight:600;line-height:1.4}
  .metric-card .head .pct{font-size:32px;font-weight:800;letter-spacing:-1px;line-height:1}
  .metric-card.bm .head .pct{color:var(--bm)}
  .metric-card.tigres .head .pct{color:var(--tigres)}
  .metric-card .formula{font-size:11.5px;color:var(--muted);background:#0d1118;border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-family:SF Mono,Monaco,monospace}
  .metric-card .formula b{color:var(--text);font-weight:600}
  .metric-card .what{font-size:12.5px;color:var(--text);line-height:1.5}
  .metric-card .ex{font-size:11.5px;color:var(--muted);line-height:1.5;border-top:1px dashed var(--line);padding-top:10px}
  .metric-card .ex b{color:var(--text)}
  .metric-warn{margin-top:14px;background:linear-gradient(135deg, rgba(255,184,77,.06), var(--panel2));border:1px solid rgba(255,184,77,.3);border-radius:10px;padding:14px 18px;font-size:12.5px;color:var(--text);line-height:1.6}
  .metric-warn b{color:var(--warn)}
  @media(max-width:760px){.metric-compare{grid-template-columns:1fr}}

  /* ============== ZONE BREAKDOWN (mockup-inspired) ============== */
  .zone-legend{display:flex;gap:18px;font-size:11.5px;color:var(--muted);margin-bottom:16px;align-items:center;flex-wrap:wrap}
  .zone-legend .dot{display:inline-block;width:9px;height:9px;border-radius:50%;vertical-align:middle;margin-right:6px}
  .zone-legend .dot.bad{background:var(--red)}
  .zone-legend .dot.warn{background:var(--warn)}
  .zone-legend .dot.ok{background:var(--bm)}
  .zone-list{display:flex;flex-direction:column;gap:6px}
  .zone-row{display:grid;grid-template-columns:160px 1fr 130px;gap:18px;align-items:center;padding:14px 18px;border-radius:10px;background:var(--panel2);border-left:3px solid var(--line);transition:.15s}
  .zone-row:hover{background:var(--panel3)}
  .zone-row.bad{border-left-color:var(--red);background:linear-gradient(90deg, rgba(255,107,107,.06), var(--panel2) 60%)}
  .zone-row.warn{border-left-color:var(--warn)}
  .zone-row.ok{border-left-color:var(--bm)}
  .zone-row .zname{font-weight:700;font-size:13.5px;display:flex;align-items:center;gap:8px}
  .zone-row.bad .zname{color:var(--red)}
  .zone-row .zname .alert{font-size:11px;background:var(--red-soft);color:var(--red);padding:1px 6px;border-radius:99px;font-weight:600}
  .zone-row .bar-wrap{display:flex;flex-direction:column;gap:4px}
  .zone-row .bar-label{font-size:11.5px;color:var(--muted);display:flex;justify-content:space-between}
  .zone-row .bar-label b{color:var(--text);font-weight:600}
  .zone-row .bar{height:7px;background:#252b3a;border-radius:4px;overflow:hidden;position:relative}
  .zone-row .bar i{display:block;height:100%;background:var(--bm);border-radius:4px;transition:width .4s}
  .zone-row.bad .bar i{background:var(--red)}
  .zone-row.warn .bar i{background:var(--warn)}
  .zone-row .zmeta{text-align:right}
  .zone-row .zmeta .v{font-size:15px;font-weight:700;letter-spacing:-.3px}
  .zone-row .zmeta .l{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;margin-top:2px;font-weight:600}
  .zone-row .zmeta .l.high{color:var(--tigres)}
  .zone-row .zmeta .l.mid{color:var(--muted)}

  /* ============== TABLES ============== */
  table{width:100%;border-collapse:collapse;font-size:12.5px}
  th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line)}
  th{font-size:10.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;font-weight:600;background:#10141c;position:sticky;top:0;z-index:1}
  th.sortable:hover{color:var(--tigres);background:#161a23}
  td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
  tr:hover td{background:var(--panel2)}
  .scroll{max-height:520px;overflow:auto;border-radius:8px;border:1px solid var(--line)}
  .conv-bar{display:inline-block;height:6px;background:var(--panel3);border-radius:3px;width:60px;vertical-align:middle;margin-right:8px;overflow:hidden}
  .conv-bar i{display:block;height:100%;background:var(--bm);border-radius:3px}
  .conv-bar.low i{background:var(--red)}
  .conv-bar.mid i{background:var(--warn)}

  /* ============== CHARTS ============== */
  .chart-wrap{position:relative;height:280px}
  .chart-wrap.tall{height:380px}

  section.tab{display:none}
  section.tab.active{display:block}

  .footer-credits{color:var(--muted2);font-size:11px;text-align:center;padding:32px 0;border-top:1px solid var(--line);margin-top:30px}

  .hidden{display:none}

  @media(max-width:900px){
    .app{grid-template-columns:1fr}
    .sidebar{position:relative;height:auto;flex-direction:row;align-items:center;padding:14px;overflow-x:auto}
    .sidebar .brand{padding:0 16px 0 6px;border-right:1px solid var(--line);border-bottom:none;flex:none}
    .sidebar nav{display:flex;padding:0 14px;flex:1}
    .sidebar nav a{margin-right:4px;margin-bottom:0;white-space:nowrap}
    .sidebar .footer-action{display:none}
    main{padding:0 16px 32px}
    .adopcion-kpis{grid-template-columns:repeat(2,1fr)}
    .funnel .step .box{font-size:24px}
  }
</style>
</head>
<body>

<div id="lock" class="lock">
  <div class="brand">
    <h1>Tigres UANL</h1>
    <div class="powered"><span>Powered by</span> __LOGO_BM__</div>
  </div>
  <div class="seal">🔒</div>
  <h2>Reporte confidencial</h2>
  <div class="accent-bar"></div>
  <p>Mercado Secundario · Información restringida a stakeholders autorizados. Ingresa la contraseña para descifrar el reporte.</p>
  <form id="lockForm" autocomplete="off">
    <input id="pwd" type="password" placeholder="Contraseña" autofocus />
    <button type="submit">Descifrar</button>
  </form>
  <div id="err" class="err"></div>
  <p style="font-size:11px;margin-top:30px;opacity:.6">El descifrado se realiza en tu navegador. Los datos no salen de tu equipo.</p>
</div>

<div id="app" class="app hidden">
  <aside class="sidebar">
    <div class="brand">
      <h1 class="logo-tigres">Tigres UANL</h1>
      <div class="powered"><span>Powered by</span> <span class="bm-mini">__LOGO_BM__</span></div>
    </div>
    <nav id="nav">
      <a href="#" data-tab="overview" class="active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
        Resumen
      </a>
      <a href="#" data-tab="listados">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
        Listados
      </a>
      <a href="#" data-tab="vendedores">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        Vendedores
      </a>
      <a href="#" data-tab="compradores">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
        Compradores
      </a>
      <a href="#" data-tab="zonas">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15 8.5 22 9.3 17 14 18.2 21 12 17.8 5.8 21 7 14 2 9.3 9 8.5 12 2"/></svg>
        Zonas
      </a>
      <a href="#" data-tab="bancos">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18"/><path d="M3 10h18"/><path d="M5 6l7-3 7 3"/><path d="M4 10v11"/><path d="M20 10v11"/><path d="M8 14v3"/><path d="M12 14v3"/><path d="M16 14v3"/></svg>
        Bancos
      </a>
    </nav>
    <div class="footer-action">
      <button id="logout">Bloquear sesión</button>
      <div class="session">Reporte generado <span id="genDate"></span></div>
    </div>
  </aside>

  <main>
    <div class="topbar">
      <div>
        <h1 id="tabTitle">Executive Dashboard</h1>
        <div style="font-size:12px;color:var(--muted);margin-top:4px"><span id="metaSummary"></span></div>
      </div>
      <div class="meta">
        <span class="pill" style="color:var(--bm);border-color:rgba(0,232,154,.3)">● AP25 + CL26</span>
        <span class="pill">Confidencial</span>
      </div>
    </div>

    <section class="tab active" id="tab-overview">
      <div class="grid kpi-row" id="kpiGrid"></div>

      <div class="section">
        <h2>Adopción del MS por abonos <span class="badge">Temporada 2025–2026</span></h2>
        <div class="desc">Cuántos abonos (cuentas <code>A22-####</code>) participan en el MS. La unidad de medida es el <b>abono</b>, no el titular: un titular puede tener varios abonos y rentar solo algunos. <b>Pusieron en venta</b> = ofrecieron al menos 1 asiento (vendido o expirado, cruzado por asiento contra el padrón). <b>Vendieron</b> = concretaron al menos 1 venta exitosa (cruzado por código de barras).</div>
        <div class="adopcion-kpis" id="adopKpis"></div>
        <div class="funnel" id="funnel"></div>
      </div>

      <div class="grid cols2">
        <div class="section">
          <h2>Embudo de eficacia <span class="badge">por abono</span></h2>
          <div class="desc">Distribución de los abonos según uso del MS. La eficacia mide a nivel <b>cuenta de abono</b> (basta 1 venta para contar como exitoso) — no es lo mismo que la conversión por boleto que ves en zonas/jornadas.</div>
          <div class="adop-list" id="adopList"></div>
          <div class="efic" style="margin-top:18px" id="eficBox"></div>
        </div>
        <div class="section">
          <h2>Concentración de vendedores</h2>
          <div class="desc">Reparto de los volúmenes entre los vendedores. Concentración alta = pocos vendedores generan la mayoría de las ventas. <b>Solo cuenta boletos vendidos</b> — los listados expirados no se pueden atribuir a un vendedor porque el archivo de Listados no incluye correo.</div>
          <div id="concBox"></div>
        </div>
      </div>

    </section>

    <section class="tab" id="tab-listados">
      <div class="grid kpi-row" id="listKpiGrid"></div>
      <div class="grid cols2">
        <div class="section">
          <h2>Conversión global</h2>
          <div class="desc">De todos los asientos puestos en venta, cuántos se vendieron vs expiraron.</div>
          <div class="chart-wrap"><canvas id="chartListConversion"></canvas></div>
        </div>
        <div class="section">
          <h2>Listados por torneo</h2>
          <div class="desc">Cuántos asientos puestos en venta por torneo y su conversión.</div>
          <div class="chart-wrap"><canvas id="chartListTorneo"></canvas></div>
        </div>
      </div>
      <div class="section">
        <h2>Conversión por jornada <span class="badge">17 jornadas</span></h2>
        <div class="desc">Volumen listado vs vendido por jornada. Una conversión baja señala sobreoferta o expectativa de demanda mal calibrada.</div>
        <div class="chart-wrap tall"><canvas id="chartListEvento"></canvas></div>
        <div style="height:18px"></div>
        <div class="scroll"><table id="tblListEvento"></table></div>
      </div>
      <div class="section">
        <h2>Conversión por zona</h2>
        <div class="desc">Qué zonas se listan más y cuáles convierten mejor. Zonas caras suelen tener menor conversión.</div>
        <div class="chart-wrap tall"><canvas id="chartListZona"></canvas></div>
        <div style="height:18px"></div>
        <div class="scroll"><table id="tblListZona"></table></div>
      </div>
    </section>

    <section class="tab" id="tab-vendedores">
      <div class="section">
        <h2>Top vendedores</h2>
        <div class="desc"><b>Eventos</b> = jornadas distintas en las que el vendedor concretó al menos una venta (de 17 posibles entre AP25 + CL26). Solo se cuentan boletos efectivamente vendidos.</div>
        <div class="scroll"><table id="tblSellers"></table></div>
      </div>
    </section>

    <section class="tab" id="tab-compradores">
      <div class="section">
        <h2>Top compradores</h2>
        <div class="desc"><b>Eventos</b> = jornadas distintas en las que el usuario compró al menos un boleto.</div>
        <div class="scroll"><table id="tblBuyers"></table></div>
      </div>
    </section>

    <section class="tab" id="tab-zonas">
      <div class="section">
        <h2>Desglose por zona <span class="badge">Top 12 por volumen listado</span></h2>
        <div class="desc">Ranking de zonas según volumen de boletos puestos en venta y su tasa de conversión. Las zonas con barra roja tienen volumen alto pero baja conversión — son las críticas para el negocio.</div>
        <div class="zone-legend">
          <span><span class="dot bad"></span>Crítico (&lt; 50% conv.)</span>
          <span><span class="dot warn"></span>Estable (50–80% conv.)</span>
          <span><span class="dot ok"></span>Óptimo (&gt; 80% conv.)</span>
        </div>
        <div class="zone-list" id="zoneList"></div>
      </div>
      <div class="section">
        <h2>Listados por zona</h2>
        <div class="desc">Cuántas veces se puso a la venta un boleto en cada zona del estadio. Volumen total (vendido + expirado).</div>
        <div class="chart-wrap tall"><canvas id="chartZonaListados"></canvas></div>
      </div>
      <div class="section">
        <h2>Detalle por zona</h2>
        <div class="desc">Volumen listado, vendido, expirado, conversión, precio promedio y volumen total vendido por cada zona.</div>
        <div class="scroll"><table id="tblZona"></table></div>
      </div>
    </section>

    <section class="tab" id="tab-bancos">
      <div class="filter-row">
        <label>Buscar banco:</label>
        <input type="text" id="bancoFilter" class="filter-input" placeholder="Escribe el nombre del banco (ej: BBVA, Santander, Banamex…)"/>
      </div>
      <div class="grid cols2">
        <div class="section">
          <h2>Distribución por banco</h2>
          <div class="desc">Proporción de boletos vendidos según el banco receptor del pago al vendedor.</div>
          <div class="chart-wrap tall"><canvas id="chartBancoPie"></canvas></div>
        </div>
        <div class="section">
          <h2>Ingreso por banco</h2>
          <div class="desc">Monto que se transfiere al vendedor a cada banco.</div>
          <div class="chart-wrap tall"><canvas id="chartBancoBar"></canvas></div>
        </div>
      </div>
      <div class="section">
        <h2>Detalle por banco</h2>
        <div class="desc">Boletos transados, vendedores únicos que reciben en ese banco e ingreso neto al vendedor (sin comisión BM).</div>
        <div class="scroll"><table id="tblBanco"></table></div>
      </div>
    </section>

  </main>

  <div id="zoneModal" class="zone-modal" role="dialog">
    <div class="zone-modal-content">
      <button class="zm-close" id="zmClose">×</button>
      <h2 id="zmTitle"></h2>
      <div class="zm-sub" id="zmSub"></div>
      <div class="zm-summary" id="zmSummary"></div>
      <div class="zone-list" id="zmJornadas"></div>
    </div>
  </div>
</div>

<script>
const PAYLOAD = %PAYLOAD_JSON%;
const fmt = new Intl.NumberFormat('es-MX');
const fmtMoney = new Intl.NumberFormat('es-MX',{style:'currency',currency:'MXN',maximumFractionDigits:0});
const fmtPct = (x)=> (x*100).toFixed(1)+'%';
const PALETTE = ['#00E89A','#F3B61C','#4a90e2','#ff7a59','#9b51e0','#ffb84d','#36b37e','#ff6b6b','#5fa3ff','#ff5db1'];
const BM='#00E89A', TIGRES='#F3B61C', RED='#ff6b6b', BLUE='#4a90e2', WARN='#ffb84d';

const TAB_TITLES = {
  overview: 'Executive Dashboard',
  listados: 'Boletos puestos en venta',
  vendedores: 'Top vendedores',
  compradores: 'Top compradores',
  zonas: 'Análisis por zona',
  bancos: 'Bancos receptores',
};

function b64(s){return Uint8Array.from(atob(s),c=>c.charCodeAt(0))}

async function decrypt(password){
  const enc = new TextEncoder();
  const salt = b64(PAYLOAD.salt);
  const iv = b64(PAYLOAD.iv);
  const ct = b64(PAYLOAD.ct);
  const baseKey = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']);
  const key = await crypto.subtle.deriveKey(
    {name:'PBKDF2', salt, iterations: PAYLOAD.iter, hash:'SHA-256'},
    baseKey,
    {name:'AES-GCM', length:256},
    false,
    ['decrypt']
  );
  const plain = await crypto.subtle.decrypt({name:'AES-GCM', iv}, key, ct);
  return JSON.parse(new TextDecoder().decode(plain));
}

document.getElementById('lockForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const pwd = document.getElementById('pwd').value;
  const errEl = document.getElementById('err');
  errEl.textContent = 'Descifrando…';
  try{
    const data = await decrypt(pwd);
    sessionStorage.setItem('tig_p', pwd);
    document.getElementById('lock').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    render(data);
  }catch(err){ errEl.textContent = '✕ Contraseña incorrecta'; }
});
document.getElementById('logout').addEventListener('click', ()=>{ sessionStorage.removeItem('tig_p'); location.reload(); });
window.addEventListener('load', async ()=>{
  const cached = sessionStorage.getItem('tig_p');
  if(cached){ try{
    const data = await decrypt(cached);
    document.getElementById('lock').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    render(data);
  }catch(_){ sessionStorage.removeItem('tig_p'); } }
});

document.querySelectorAll('#nav a').forEach(a=>{
  a.addEventListener('click', (e)=>{
    e.preventDefault();
    document.querySelectorAll('#nav a').forEach(x=>x.classList.remove('active'));
    a.classList.add('active');
    document.querySelectorAll('section.tab').forEach(s=>s.classList.remove('active'));
    document.getElementById('tab-'+a.dataset.tab).classList.add('active');
    document.getElementById('tabTitle').textContent = TAB_TITLES[a.dataset.tab] || 'Dashboard';
    window.scrollTo({top:0,behavior:'smooth'});
  });
});

function tableHTML(headers, rows){
  const ths = headers.map(h=>`<th class="${h.num?'num':''}">${h.label}</th>`).join('');
  const trs = rows.map(r=>{
    return '<tr>'+ headers.map(h=>{
      let v = r[h.key];
      if(h.fmt==='money') v = v ? fmtMoney.format(v) : '—';
      else if(h.fmt==='int') v = (v||v===0) ? fmt.format(v) : '0';
      else if(h.fmt==='pct') v = (v*100).toFixed(1)+'%';
      else if(typeof h.fmt==='function') v = h.fmt(v, r);
      else if(v === '' || v == null) v = '—';
      return `<td class="${h.num?'num':''}">${v}</td>`;
    }).join('') +'</tr>';
  }).join('');
  return `<thead><tr>${ths}</tr></thead><tbody>${trs}</tbody>`;
}

// Tabla con orden clickeable. defaultSort = {key, dir:'asc'|'desc'}
function renderSortableTable(tableId, headers, rows, defaultSort){
  let sortKey = defaultSort?.key || null;
  let sortDir = defaultSort?.dir || 'desc';
  const tbl = document.getElementById(tableId);
  if(!tbl) return;
  const draw = ()=>{
    const arr = [...rows];
    if(sortKey){
      arr.sort((a,b)=>{
        const va = a[sortKey], vb = b[sortKey];
        if(va == null && vb == null) return 0;
        if(va == null) return 1;
        if(vb == null) return -1;
        const cmp = (typeof va === 'number' && typeof vb === 'number') ? va - vb : String(va).localeCompare(String(vb),'es',{numeric:true});
        return sortDir === 'asc' ? cmp : -cmp;
      });
    }
    const ths = headers.map(h=>{
      const sortable = h.sortable !== false;
      const arrow = (sortKey === h.key) ? (sortDir === 'asc' ? ' ▲' : ' ▼') : (sortable ? ' <span style="opacity:.25">⇅</span>' : '');
      const cls = (h.num?'num ':'') + (sortable?'sortable':'');
      const attrs = sortable ? `data-sort="${h.key}" style="cursor:pointer;user-select:none"` : '';
      return `<th class="${cls}" ${attrs}>${h.label}${arrow}</th>`;
    }).join('');
    const trs = arr.map(r=>{
      return '<tr>'+ headers.map(h=>{
        let v = r[h.key];
        if(h.fmt==='money') v = v ? fmtMoney.format(v) : '—';
        else if(h.fmt==='int') v = (v||v===0) ? fmt.format(v) : '0';
        else if(h.fmt==='pct') v = (v*100).toFixed(1)+'%';
        else if(typeof h.fmt==='function') v = h.fmt(v, r);
        else if(v === '' || v == null) v = '—';
        return `<td class="${h.num?'num':''}">${v}</td>`;
      }).join('') +'</tr>';
    }).join('');
    tbl.innerHTML = `<thead><tr>${ths}</tr></thead><tbody>${trs}</tbody>`;
    tbl.querySelectorAll('thead th[data-sort]').forEach(th=>{
      th.addEventListener('click', ()=>{
        const k = th.dataset.sort;
        if(sortKey === k) sortDir = (sortDir === 'asc' ? 'desc' : 'asc');
        else { sortKey = k; sortDir = (headers.find(h=>h.key===k)?.num) ? 'desc' : 'asc'; }
        draw();
      });
    });
  };
  draw();
}

function chart(id, type, labels, datasets, opts={}){
  const el = document.getElementById(id);
  if(!el) return;
  if(el._chart) el._chart.destroy();
  el._chart = new Chart(el, {
    type, data:{labels, datasets},
    options: Object.assign({
      responsive:true,
      maintainAspectRatio:false,
      plugins:{
        legend:{labels:{color:'#f1f3f7',font:{size:11}}},
        tooltip:{callbacks:{
          label: (c)=>{
            const v = c.parsed.y ?? c.parsed;
            return c.dataset.label ? `${c.dataset.label}: ${fmt.format(v)}` : fmt.format(v);
          }
        }}
      },
      scales: type==='bar'||type==='line' ? {
        x:{ticks:{color:'#9aa3b5',font:{size:10}},grid:{color:'#1a1f2a'}},
        y:{ticks:{color:'#9aa3b5',font:{size:10}},grid:{color:'#1a1f2a'},beginAtZero:true}
      } : {}
    }, opts)
  });
}

function convBar(p){
  const lvl = p<0.4?'low':(p<0.6?'mid':'');
  return `<span class="conv-bar ${lvl}"><i style="width:${(p*100).toFixed(1)}%"></i></span>${(p*100).toFixed(1)}%`;
}

function render(d){
  document.getElementById('genDate').textContent = d.meta.generated_at;
  document.getElementById('metaSummary').textContent = `${fmt.format(d.meta.totals_listados)} listados · ${fmt.format(d.meta.totals_ms_orders)} vendidos · ${d.by_evento_detail.length} jornadas · ${fmt.format(d.adopcion_abonados.total_cuentas_abono)} abonos`;

  // ---------- KPI ROW (Resumen) ----------
  const sum = d.ms_detail_summary;
  const list = d.listados_summary;
  const adop = d.adopcion_abonados;
  const conc = d.concentracion_vendedores;

  const kpis = [
    {label:'Asientos puestos en venta', v:fmt.format(list.total), sub:`${d.by_evento_detail.length} jornadas (AP25 + CL26)`, cls:'tigres', icon:'🎟'},
    {label:'Boletos vendidos', v:fmt.format(list.vendidos), sub:`${fmt.format(list.expirados)} expiraron sin venderse`, cls:'ok', icon:'✓'},
    {label:'Conversión por boleto', v:fmtPct(list.conversion), sub:`${fmt.format(list.vendidos)} de ${fmt.format(list.total)} listados se vendieron`, cls:'ok', icon:'📈'},
    {label:'Eficacia por abono', v:fmtPct(adop.eficacia_listaron_a_vendieron), sub:`De los abonos que listaron, % vendió ≥1 boleto`, cls:'tigres', icon:'⭐'},
  ];
  document.getElementById('kpiGrid').innerHTML = kpis.map(k=>`
    <div class="kpi-card ${k.cls||''}">
      <div class="label">${k.label}<span class="icon">${k.icon||''}</span></div>
      <div class="v">${k.v}</div>
      <div class="sub">${k.sub||''}</div>
    </div>`).join('');

  // ---------- ADOPCION KPIs ----------
  const adopKpis = [
    {label:'Total abonos', v:fmt.format(adop.total_cuentas_abono), pct:'100%', cls:'total'},
    {label:'Nunca pusieron en venta', v:fmt.format(adop.cuentas_nunca_usaron_ms), pct:fmtPct(adop.porcentaje_nunca_usaron), cls:'no-uso'},
    {label:'Pusieron pero no vendieron', v:fmt.format(adop.cuentas_listaron_sin_vender), pct:fmtPct(adop.porcentaje_listaron_sin_vender), cls:'listaron'},
    {label:'Vendieron', v:fmt.format(adop.cuentas_vendieron_ms), pct:fmtPct(adop.porcentaje_vendieron), cls:'vendieron'},
  ];
  document.getElementById('adopKpis').innerHTML = adopKpis.map(k=>`
    <div class="adp ${k.cls}">
      <div class="label">${k.label}</div>
      <div class="v">${k.v}<small>${k.pct}</small></div>
    </div>`).join('');

  // ---------- FUNNEL ----------
  const pctList = adop.porcentaje_listaron;
  const pctVend = adop.eficacia_listaron_a_vendieron;
  document.getElementById('funnel').innerHTML = `
    <div class="step s1"><div class="box">100%</div><div class="label">Total abonos</div></div>
    <div class="arrow"><div style="font-size:12px;color:var(--bm);font-weight:700;letter-spacing:.5px;text-transform:none">${fmtPct(pctList)} pusieron en venta</div><div class="line"></div></div>
    <div class="step s2"><div class="box">${(pctList*100).toFixed(0)}%</div><div class="label">Pusieron en venta</div></div>
    <div class="arrow"><div style="font-size:12px;color:var(--bm);font-weight:700;letter-spacing:.5px;text-transform:none">✓ ${fmtPct(pctVend)} vendió ≥ 1 boleto</div><div class="line"></div></div>
    <div class="step s3"><div class="box">${(adop.porcentaje_vendieron*100).toFixed(0)}%</div><div class="label">Vendieron al menos 1</div></div>
  `;

  // ---------- ADOP LIST + EFICACIA ----------
  document.getElementById('adopList').innerHTML = `
    <div class="adop-row ok">
      <div class="icon">✓</div>
      <div class="text"><div class="t">Abonos que vendieron exitosamente</div><div class="pct">${fmtPct(adop.porcentaje_vendieron)} del total</div></div>
      <div class="num">${fmt.format(adop.cuentas_vendieron_ms)}<small>de ${fmt.format(adop.total_cuentas_abono)}</small></div>
    </div>
    <div class="adop-row warn">
      <div class="icon">⏳</div>
      <div class="text"><div class="t">Pusieron en venta pero no concretaron</div><div class="pct">${fmtPct(adop.porcentaje_listaron_sin_vender)} del total</div></div>
      <div class="num">${fmt.format(adop.cuentas_listaron_sin_vender)}<small>expiraron</small></div>
    </div>
    <div class="adop-row bad">
      <div class="icon">∅</div>
      <div class="text"><div class="t">Abonos sin actividad en MS</div><div class="pct">${fmtPct(adop.porcentaje_nunca_usaron)} del total</div></div>
      <div class="num">${fmt.format(adop.cuentas_nunca_usaron_ms)}<small>nunca lo usaron</small></div>
    </div>
  `;
  document.getElementById('eficBox').innerHTML = `
    <div class="v">${fmtPct(adop.eficacia_listaron_a_vendieron)}</div>
    <div class="l">Eficacia · de los abonos que listaron, % vendió ≥ 1 boleto</div>
    <div style="font-size:11px;color:var(--muted);text-align:center;max-width:380px;margin:14px auto 0;line-height:1.5">⚠ Mide cuántos abonos lograron <b>al menos 1 venta</b>. Si un abono lista 17 boletos y solo vende 1, cuenta como ✓. Para % de boletos individuales que se venden, mira la conversión por zona/jornada (60.4% global).</div>
  `;

  // ---------- CONCENTRACIÓN ----------
  document.getElementById('concBox').innerHTML = `
    <div class="grid kpi-row" style="grid-template-columns:repeat(2,1fr);margin:0">
      <div class="adp"><div class="label">Vendedores únicos</div><div class="v">${fmt.format(conc.unique_sellers)}</div></div>
      <div class="adp"><div class="label">Boletos prom. / vendedor</div><div class="v">${conc.avg_boletos_per_seller.toFixed(1)}</div></div>
      <div class="adp vendieron"><div class="label">Máx boletos vendidos por uno</div><div class="v">${fmt.format(conc.max_boletos_single_seller)}</div></div>
      <div class="adp"><div class="label">Top 10% concentra</div><div class="v">${fmtPct(conc.top_10pct_share)}</div></div>
      <div class="adp"><div class="label">Con 5+ boletos</div><div class="v">${fmt.format(conc.sellers_with_5plus)}</div></div>
      <div class="adp"><div class="label">Con 10+ boletos</div><div class="v">${fmt.format(conc.sellers_with_10plus)}</div></div>
      <div class="adp listaron"><div class="label">Con 20+ boletos</div><div class="v">${fmt.format(conc.sellers_with_20plus||0)}</div></div>
      <div class="adp"><div class="label">Con 1 boleto solo</div><div class="v">${fmt.format(conc.sellers_with_1_boleto)}</div></div>
    </div>`;


  // ---------- LISTADOS ----------
  const listKpis = [
    {label:'Total puesto en venta', v:fmt.format(list.total), sub:`${d.by_evento_detail.length} jornadas`, cls:'tigres', icon:'📋'},
    {label:'Vendidos', v:fmt.format(list.vendidos), sub:`<span class="delta">${fmtPct(list.conversion)}</span> conversión global`, cls:'ok', icon:'✓'},
    {label:'Expirados', v:fmt.format(list.expirados), sub:`${fmtPct(list.expirados/list.total)} del total — sin vender`, cls:'bad', icon:'⏳'},
    {label:'Abonos que pusieron en venta', v:fmtPct(adop.porcentaje_listaron), sub:`${fmt.format(adop.cuentas_listaron_ms)} de ${fmt.format(adop.total_cuentas_abono)} abonos`, cls:'tigres', icon:'👤'},
  ];
  document.getElementById('listKpiGrid').innerHTML = listKpis.map(k=>`
    <div class="kpi-card ${k.cls||''}">
      <div class="label">${k.label}<span class="icon">${k.icon||''}</span></div>
      <div class="v">${k.v}</div>
      <div class="sub">${k.sub||''}</div>
    </div>`).join('');

  // Dona "Conversión global" con % en el centro
  const centerTextPlugin = {
    id:'centerText',
    afterDraw(c){
      const ctx = c.ctx;
      const data = c.data.datasets[0].data;
      const total = data.reduce((a,b)=>a+b,0);
      if(!total) return;
      const pct = (data[0]/total*100).toFixed(1)+'%';
      const {chartArea} = c;
      const cx = (chartArea.left + chartArea.right)/2;
      const cy = (chartArea.top + chartArea.bottom)/2;
      ctx.save();
      ctx.font = 'bold 30px -apple-system,BlinkMacSystemFont,sans-serif';
      ctx.fillStyle = '#00E89A';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(pct, cx, cy - 6);
      ctx.font = 'bold 10.5px -apple-system,BlinkMacSystemFont,sans-serif';
      ctx.fillStyle = '#9aa3b5';
      ctx.fillText('VENDIDOS', cx, cy + 18);
      ctx.restore();
    }
  };
  (()=>{
    const el = document.getElementById('chartListConversion');
    if(el._chart) el._chart.destroy();
    el._chart = new Chart(el, {
      type:'doughnut',
      data:{labels:['Vendidos','Expirados'], datasets:[{
        data:[list.vendidos, list.expirados], backgroundColor:[BM, RED], borderColor:'#0d1118', borderWidth:2
      }]},
      options:{responsive:true,maintainAspectRatio:false,cutout:'68%',
        plugins:{legend:{labels:{color:'#f1f3f7',padding:14}},
          tooltip:{callbacks:{label:c=>{
            const tot = c.dataset.data.reduce((a,b)=>a+b,0);
            return `${c.label}: ${fmt.format(c.parsed)} (${(c.parsed/tot*100).toFixed(1)}%)`;
          }}}
        }
      },
      plugins:[centerTextPlugin]
    });
  })();

  // Barras "Listados por torneo" con % en cada segmento
  const stackPctPlugin = {
    id:'stackPct',
    afterDatasetsDraw(c){
      const ctx = c.ctx;
      ctx.save();
      ctx.font = 'bold 12px -apple-system,BlinkMacSystemFont,sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      c.data.datasets.forEach((ds, di)=>{
        const meta = c.getDatasetMeta(di);
        meta.data.forEach((bar, i)=>{
          const total = c.data.datasets.reduce((a,d)=>a+d.data[i],0);
          if(total === 0) return;
          const v = ds.data[i];
          const pct = (v/total*100);
          if(pct < 6) return;
          const yMid = (bar.y + bar.base)/2;
          ctx.fillStyle = '#0a0d12';
          ctx.fillText(pct.toFixed(1)+'%', bar.x, yMid);
        });
      });
      ctx.restore();
    }
  };
  const tornNames = Object.keys(list.by_tournament);
  (()=>{
    const el = document.getElementById('chartListTorneo');
    if(el._chart) el._chart.destroy();
    el._chart = new Chart(el, {
      type:'bar',
      data:{labels:tornNames, datasets:[
        {label:'Vendidos', data:tornNames.map(t=>list.by_tournament[t].VENDIDO||0), backgroundColor:BM, borderRadius:4},
        {label:'Expirados', data:tornNames.map(t=>list.by_tournament[t].EXPIRADO||0), backgroundColor:'#3a4255', borderRadius:4},
      ]},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{color:'#f1f3f7'}},
          tooltip:{callbacks:{label:c=>{
            const tot = c.chart.data.datasets.reduce((a,d)=>a+d.data[c.dataIndex],0);
            return `${c.dataset.label}: ${fmt.format(c.parsed.y)} (${(c.parsed.y/tot*100).toFixed(1)}%)`;
          }}}
        },
        scales:{x:{stacked:true,ticks:{color:'#9aa3b5'},grid:{color:'#1a1f2a'}}, y:{stacked:true,ticks:{color:'#9aa3b5'},grid:{color:'#1a1f2a'},beginAtZero:true}}
      },
      plugins:[stackPctPlugin]
    });
  })();

  const listEv = d.listados_by_evento;
  const evLabels = listEv.map(r=>r.tournament+' · '+r.rival);
  // Plugin custom: dibuja el % de expirados encima de cada barra de expirados
  const expPctPlugin = {
    id:'expPct',
    afterDatasetsDraw(c){
      const ctx = c.ctx;
      const metaExp = c.getDatasetMeta(1);
      ctx.save();
      ctx.font = 'bold 10.5px -apple-system,BlinkMacSystemFont,sans-serif';
      ctx.textAlign = 'center';
      metaExp.data.forEach((bar,i)=>{
        const vend = c.data.datasets[0].data[i];
        const exp = c.data.datasets[1].data[i];
        const total = vend + exp;
        if(total === 0) return;
        const pct = exp/total;
        const txt = (pct*100).toFixed(0)+'% exp.';
        ctx.fillStyle = pct >= 0.5 ? '#ff6b6b' : (pct >= 0.3 ? '#ffb84d' : '#9aa3b5');
        ctx.fillText(txt, bar.x, bar.y - 6);
      });
      ctx.restore();
    }
  };
  // Llamada manual para inyectar plugin específico
  (()=>{
    const el = document.getElementById('chartListEvento');
    if(el._chart) el._chart.destroy();
    el._chart = new Chart(el, {
      type:'bar',
      data:{labels:evLabels, datasets:[
        {label:'Vendidos', data:listEv.map(r=>r.vendido), backgroundColor:BM, borderRadius:3},
        {label:'Expirados', data:listEv.map(r=>r.expirado), backgroundColor:'#3a4255', borderRadius:3},
      ]},
      options:{
        responsive:true, maintainAspectRatio:false,
        layout:{padding:{top:20}},
        plugins:{
          legend:{labels:{color:'#f1f3f7',font:{size:11}}},
          tooltip:{callbacks:{
            label:c=>{
              const v = c.parsed.y;
              const i = c.dataIndex;
              const tot = listEv[i].vendido + listEv[i].expirado;
              const p = ((v/tot)*100).toFixed(1);
              return `${c.dataset.label}: ${fmt.format(v)} (${p}%)`;
            }
          }}
        },
        scales:{
          x:{ticks:{color:'#9aa3b5',autoSkip:false,maxRotation:60,minRotation:45},grid:{display:false}},
          y:{ticks:{color:'#9aa3b5'},grid:{color:'#1a1f2a'},beginAtZero:true}
        }
      },
      plugins:[expPctPlugin]
    });
  })();

  renderSortableTable('tblListEvento', [
    {key:'tournament', label:'Torneo'},
    {key:'rival', label:'Rival'},
    {key:'total', label:'Listados', num:true, fmt:'int'},
    {key:'vendido', label:'Vendidos', num:true, fmt:'int'},
    {key:'expirado', label:'Expirados', num:true, fmt:'int'},
    {key:'conversion', label:'% conversión', num:true, fmt:(v)=>convBar(v||0)},
    {key:'revenue_vendido', label:'Volumen vendido', num:true, fmt:'money'},
  ], listEv, {key:'conversion', dir:'desc'});

  const listZ = d.listados_by_zona;
  const zonasTop = listZ.slice(0,12);
  chart('chartListZona','bar', zonasTop.map(r=>r.zona), [
    {label:'Vendidos', data:zonasTop.map(r=>r.vendido), backgroundColor:BM, borderRadius:3},
    {label:'Expirados', data:zonasTop.map(r=>r.expirado), backgroundColor:'#3a4255', borderRadius:3},
  ],{scales:{x:{stacked:true,ticks:{color:'#9aa3b5'},grid:{display:false}}, y:{stacked:true,ticks:{color:'#9aa3b5'},grid:{color:'#1a1f2a'},beginAtZero:true}}});

  renderSortableTable('tblListZona', [
    {key:'zona', label:'Zona'},
    {key:'total', label:'Listados', num:true, fmt:'int'},
    {key:'vendido', label:'Vendidos', num:true, fmt:'int'},
    {key:'expirado', label:'Expirados', num:true, fmt:'int'},
    {key:'conversion', label:'% conversión', num:true, fmt:(v)=>convBar(v||0)},
    {key:'precio_promedio', label:'Precio prom.', num:true, fmt:'money'},
    {key:'revenue_vendido', label:'Volumen vendido', num:true, fmt:'money'},
  ], listZ, {key:'total', dir:'desc'});

  // ---------- VENDEDORES ----------
  renderSortableTable('tblSellers', [
    {key:'nombre', label:'Vendedor'},
    {key:'correo', label:'Correo'},
    {key:'telefono', label:'Teléfono'},
    {key:'boletos', label:'Boletos', num:true, fmt:'int'},
    {key:'abonos', label:'Abonos', num:true, fmt:'int'},
    {key:'eventos', label:'Eventos', num:true, fmt:'int'},
    {key:'revenue', label:'Recibido', num:true, fmt:'money'},
  ], d.top_sellers, {key:'boletos', dir:'desc'});

  // ---------- COMPRADORES ----------
  renderSortableTable('tblBuyers', [
    {key:'nombre', label:'Comprador'},
    {key:'correo', label:'Correo'},
    {key:'telefono', label:'Teléfono'},
    {key:'boletos', label:'Boletos', num:true, fmt:'int'},
    {key:'ordenes', label:'Órdenes', num:true, fmt:'int'},
    {key:'eventos', label:'Eventos', num:true, fmt:'int'},
    {key:'revenue', label:'Pagado', num:true, fmt:'money'},
  ], d.top_buyers, {key:'boletos', dir:'desc'});

  // ---------- ZONAS ----------
  const zonas = d.listados_by_zona;

  // Desglose por zona (mockup-inspired, top 12 por volumen)
  const zonasOrdenadas = [...zonas].sort((a,b)=>b.total - a.total).slice(0, 12);
  const maxTotal = Math.max(...zonasOrdenadas.map(z=>z.total));
  const zoneRows = zonasOrdenadas.map(z=>{
    const conv = z.conversion;
    const cls = conv < 0.5 ? 'bad' : conv < 0.8 ? 'warn' : 'ok';
    const volTier = z.total / maxTotal;
    const volTag = volTier > 0.66 ? 'Alto Volumen' : volTier > 0.33 ? 'Volumen Medio' : 'Bajo Volumen';
    const volTagCls = volTier > 0.66 ? 'high' : 'mid';
    const alert = (cls==='bad' && volTier > 0.4) ? '<span class="alert">⚠ crítico</span>' : '';
    return `
      <div class="zone-row ${cls}">
        <div class="zname">${z.zona}${alert}</div>
        <div class="bar-wrap">
          <div class="bar-label">
            <span>Conversión: <b>${(conv*100).toFixed(1)}%</b></span>
            <span>${fmt.format(z.vendido)} / ${fmt.format(z.total)} listados</span>
          </div>
          <div class="bar"><i style="width:${(conv*100).toFixed(1)}%"></i></div>
        </div>
        <div class="zmeta">
          <div class="v">${fmtMoney.format(z.revenue_vendido)}</div>
          <div class="l ${volTagCls}">${volTag}</div>
        </div>
      </div>`;
  }).join('');
  document.getElementById('zoneList').innerHTML = zoneRows;

  chart('chartZonaListados','bar', zonas.map(r=>r.zona), [
    {label:'Vendidos', data:zonas.map(r=>r.vendido), backgroundColor:BM, borderRadius:3, stack:'a'},
    {label:'Expirados', data:zonas.map(r=>r.expirado), backgroundColor:'#3a4255', borderRadius:3, stack:'a'},
  ],{scales:{x:{stacked:true,ticks:{color:'#9aa3b5'},grid:{display:false}}, y:{stacked:true,ticks:{color:'#9aa3b5'},grid:{color:'#1a1f2a'},beginAtZero:true}}});

  renderSortableTable('tblZona', [
    {key:'zona', label:'Zona'},
    {key:'total', label:'Listados', num:true, fmt:'int'},
    {key:'vendido', label:'Vendidos', num:true, fmt:'int'},
    {key:'expirado', label:'Expirados', num:true, fmt:'int'},
    {key:'conversion', label:'Tasa de venta', num:true, fmt:(v)=>convBar(v||0)},
    {key:'precio_promedio', label:'Precio prom.', num:true, fmt:'money'},
    {key:'revenue_vendido', label:'Volumen vendido', num:true, fmt:'money'},
  ], zonas, {key:'total', dir:'desc'});

  // ---------- BANCOS (con filtro) ----------
  const renderBancos = (filterText='')=>{
    const f = filterText.trim().toLowerCase();
    const filtered = f ? d.by_banco.filter(b=>b.banco.toLowerCase().includes(f)) : d.by_banco;
    const top = filtered.slice(0,15);

    chart('chartBancoPie','doughnut', top.map(r=>r.banco), [{
      data:top.map(r=>r.orders), backgroundColor:PALETTE, borderColor:'#0d1118', borderWidth:2
    }],{scales:{}, cutout:'58%', plugins:{legend:{position:'right',labels:{color:'#f1f3f7',padding:10,font:{size:11}}},
      tooltip:{callbacks:{label:c=>`${c.label}: ${fmt.format(c.parsed)} boletos`}}}});

    chart('chartBancoBar','bar', top.map(r=>r.banco), [
      {label:'Ingreso (sin comisión)', data:top.map(r=>r.revenue), backgroundColor:TIGRES, borderRadius:3}
    ],{indexAxis:'y',scales:{
      x:{ticks:{color:'#9aa3b5',callback:v=>'$'+(v/1e6).toFixed(1)+'M'},grid:{color:'#1a1f2a'},beginAtZero:true},
      y:{ticks:{color:'#9aa3b5'},grid:{display:false}}
    }, plugins:{legend:{display:false}, tooltip:{callbacks:{label:c=>fmtMoney.format(c.parsed.x)}}}});

    renderSortableTable('tblBanco', [
      {key:'banco', label:'Banco'},
      {key:'orders', label:'Boletos', num:true, fmt:'int'},
      {key:'sellers', label:'Vendedores', num:true, fmt:'int'},
      {key:'revenue', label:'Neto al vendedor', num:true, fmt:'money'},
    ], filtered, {key:'revenue', dir:'desc'});
  };
  renderBancos();
  document.getElementById('bancoFilter').addEventListener('input', e=>renderBancos(e.target.value));

  // ---------- ZONA DRILL-DOWN (modal por jornada) ----------
  const zMap = d.listados_by_zona_jornada || {};
  const showZoneDetail = (zona)=>{
    const partidos = zMap[zona] || [];
    const totalListados = partidos.reduce((a,p)=>a+p.total,0);
    const totalVendidos = partidos.reduce((a,p)=>a+p.vendido,0);
    const totalExpirados = partidos.reduce((a,p)=>a+p.expirado,0);
    const totalRevenue = partidos.reduce((a,p)=>a+p.revenue_vendido,0);
    const conv = totalListados ? totalVendidos/totalListados : 0;

    document.getElementById('zmTitle').textContent = `Zona ${zona}`;
    document.getElementById('zmSub').textContent = `Detalle por jornada · ${partidos.length} partidos · conversión global ${(conv*100).toFixed(1)}%`;

    document.getElementById('zmSummary').innerHTML = `
      <div class="adp"><div class="label">Listados</div><div class="v">${fmt.format(totalListados)}</div></div>
      <div class="adp vendieron"><div class="label">Vendidos</div><div class="v">${fmt.format(totalVendidos)}</div></div>
      <div class="adp no-uso"><div class="label">Expirados</div><div class="v">${fmt.format(totalExpirados)}</div></div>
      <div class="adp listaron"><div class="label">Ingreso</div><div class="v">${fmtMoney.format(totalRevenue)}</div></div>
    `;

    const rows = partidos.map(p=>{
      const c = p.conversion;
      const cls = c < 0.5 ? 'bad' : c < 0.8 ? 'warn' : 'ok';
      return `
        <div class="zone-row ${cls}">
          <div class="zname">${p.tournament} · ${p.rival}</div>
          <div class="bar-wrap">
            <div class="bar-label">
              <span>Conversión: <b>${(c*100).toFixed(1)}%</b></span>
              <span>${fmt.format(p.vendido)} / ${fmt.format(p.total)} listados · ${fmt.format(p.expirado)} expirados</span>
            </div>
            <div class="bar"><i style="width:${(c*100).toFixed(1)}%"></i></div>
          </div>
          <div class="zmeta">
            <div class="v">${fmtMoney.format(p.revenue_vendido)}</div>
            <div class="l">vendido</div>
          </div>
        </div>`;
    }).join('');
    document.getElementById('zmJornadas').innerHTML = rows;
    document.getElementById('zoneModal').classList.add('show');
  };

  // Hacer las filas del desglose y de la tabla de zonas clickeables
  document.querySelectorAll('#zoneList .zone-row').forEach((row, i)=>{
    row.classList.add('clickable');
    row.addEventListener('click', ()=>{
      const zonaName = row.querySelector('.zname').firstChild.textContent.trim();
      showZoneDetail(zonaName);
    });
  });
  document.querySelectorAll('#tblZona tbody tr').forEach(tr=>{
    tr.style.cursor = 'pointer';
    tr.addEventListener('click', ()=>{
      const zona = tr.querySelector('td').textContent.trim();
      showZoneDetail(zona);
    });
  });

  document.getElementById('zmClose').addEventListener('click', ()=>{
    document.getElementById('zoneModal').classList.remove('show');
  });
  document.getElementById('zoneModal').addEventListener('click', (e)=>{
    if(e.target.id === 'zoneModal') document.getElementById('zoneModal').classList.remove('show');
  });
  document.addEventListener('keydown', (e)=>{
    if(e.key === 'Escape') document.getElementById('zoneModal').classList.remove('show');
  });
}
</script>
</body>
</html>
"""

out = HTML.replace('__LOGO_BM__', LOGO_BM).replace('%PAYLOAD_JSON%', json.dumps(blob))

out_path = os.path.join(ROOT, 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(out)
print(f'OK -> {out_path}  ({os.path.getsize(out_path):,} bytes)')
