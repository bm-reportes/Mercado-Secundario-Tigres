# Mercado Secundario · Tigres UANL

Reporte ejecutivo del mercado secundario (MS) de boletos de Tigres UANL para los torneos **Apertura 2025** y **Clausura 2026**, generado a partir de los archivos de Boletomóvil.

El reporte se entrega como un HTML standalone con datos cifrados client-side (AES-GCM 256 + PBKDF2-SHA256, 250,000 iteraciones). Para abrirlo solo se necesita un navegador moderno y la contraseña.

## Contenido del reporte

- **Resumen** — KPIs globales, adopción del MS por abonos, embudo de eficacia y concentración de vendedores.
- **Listados** — conversión global, por torneo, por jornada (con % de expirados sobre cada barra) y por zona.
- **Vendedores** — top 100 con boletos vendidos, órdenes únicas, abonos detrás, eventos cubiertos, total recibido y banco principal.
- **Compradores** — top 100 con boletos, órdenes y total pagado.
- **Zonas** — desglose con tasa de conversión, drill-down clickeable a detalle por jornada para cada zona.
- **Bancos** — distribución del ingreso (sin comisión BM) por banco receptor, con filtro de búsqueda.

## Estructura esperada de archivos (no se incluye en el repo)

```
Tigres/
├── MS/
│   ├── AP25/J# Rival.xlsx       # MS detallado 31 cols por jornada
│   └── CL26/J# Rival.xlsx
├── Listados/
│   └── J# Rival.xlsx            # listados con status (vendido/expirado/disponible)
├── TR/
│   ├── Abonos AP26CL26.xlsx     # padrón de abonos
│   └── <Rival>.xlsx             # mercado primario individual
├── build_data.py
├── build_html.py
└── reporte_tigres_ms.html       # output cifrado
```

## Cómo regenerar el reporte

```bash
# 1. Procesa todos los Excel y genera analytics.json
python3 build_data.py

# 2. Cifra y embebe en HTML standalone (pide la contraseña)
TIGRES_PASS='tu_contraseña' python3 build_html.py
```

### Modo anonimización (para compartir públicamente)

Si vas a publicar el reporte en un repositorio público, exporta `ANONYMIZE=1` para que los nombres, correos y teléfonos de vendedores y compradores se enmascaren con asteriscos antes de cifrarse:

```bash
ANONYMIZE=1 python3 build_data.py
TIGRES_PASS='tu_contraseña' python3 build_html.py
```

El `reporte_tigres_ms.html` incluido en este repo está generado con `ANONYMIZE=1`.

## Dependencias

```bash
pip install openpyxl cryptography
```

## Seguridad y privacidad

- Los Excel originales contienen datos personales (correos, teléfonos, CLABEs, nombres) y **no se incluyen en este repositorio**. Quedan locales en la máquina que ejecuta los scripts.
- El HTML resultante encripta todos los datos con AES-GCM 256. Sin la contraseña no se puede leer el contenido.
- El descifrado ocurre 100% en el navegador del lector — los datos no salen del equipo.

## Métricas clave (snapshot mayo 2026)

- 90,775 boletos puestos en venta · 54,846 vendidos (60.4% conversión global)
- $42.9M MXN pagados a vendedores (sin comisión)
- 17,258 abonos analizados · 7,693 (44.6%) pusieron al menos uno en venta · 6,628 (38.4%) concretaron al menos una venta
- 5,523 vendedores únicos · top 10% concentra el 36% del volumen
