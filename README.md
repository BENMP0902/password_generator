# Generador de contraseñas — Ejercicio de CI/CD con GitHub Actions

Proyecto didáctico del curso **Herramientas para DevOps** (Hybridge). El objetivo del repositorio **no** es entregar un generador de contraseñas de producción, sino **practicar la construcción de un pipeline de CI/CD con GitHub Actions**: ejecución automática de linting (`flake8`), pruebas (`pytest`) y build/push de una imagen Docker a GitHub Container Registry (GHCR) en cada cambio.

> **Purpose / Propósito:** aprender GitHub Actions (workflows, jobs, steps, secrets, GHCR), no generar secretos seguros. El código se conserva **fiel al material del curso** de forma intencional.

---

## ⚠️ Nota de seguridad (leer antes de usar)

**Este proyecto genera contraseñas con el módulo `random` de Python, lo cual NO es una práctica recomendable para seguridad.** Se usa aquí **únicamente como ejercicio** para trabajar con GitHub Actions.

`random` implementa el algoritmo *Mersenne Twister*, un **PRNG (Pseudo-Random Number Generator) no criptográfico y determinista**: observando suficientes salidas, su estado interno es reconstruible y las contraseñas se vuelven predecibles. La [documentación oficial de Python](https://docs.python.org/3/library/random.html) advierte explícitamente que este módulo **no debe usarse con fines de seguridad**.

- **Referencia:** [CWE-338 — Use of Cryptographically Weak PRNG](https://cwe.mitre.org/data/definitions/338.html), [CWE-330 — Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html).
- **En producción se usaría** el módulo [`secrets`](https://docs.python.org/3/library/secrets.html) (PEP 506, Python 3.6+), diseñado para generar tokens y contraseñas con un CSPRNG (Cryptographically Secure PRNG).

> **No uses las contraseñas generadas por este repositorio para nada real.** Su valor es demostrar un flujo de CI/CD, no proteger cuentas.

### Otras limitaciones conocidas (no corregidas en este ejercicio)

Se documentan por transparencia. El alcance de esta práctica es el pipeline, no el *hardening*:

| # | Limitación | Estándar / concepto |
|---|------------|---------------------|
| 1 | `random` en generación de secretos | CWE-338 / CWE-330 |
| 2 | Permiso `packages: write` a nivel de workflow completo (el job de test no lo necesita) | Least privilege |
| 3 | Push de imagen en cada evento (no solo en merge a `main`) | Superficie de ataque de CI/CD |
| 4 | Tag `:latest` mutable (sin trazabilidad commit → imagen) | Inmutabilidad / auditoría |
| 5 | Dependencias de dev sin versión fija | Reproducibilidad / supply chain |

---

## Estructura del proyecto

```
password_generator/
├── generator/
│   ├── __init__.py
│   └── password_generator.py     # lógica del generador (usa random — ver nota de seguridad)
├── tests/
│   └── test_generator.py         # pruebas con pytest
├── .github/
│   └── workflows/                # ← plural: requisito de GitHub Actions
│       └── ci.yml                # definición del pipeline
├── main.py                       # entrypoint por CLI
├── requirements-dev.txt          # pytest, flake8
├── .flake8                       # config de linting
├── .gitignore
├── README.md
└── LICENSE
```

> **Nota:** GitHub Actions **solo** descubre workflows en `.github/workflows/` (plural). Cualquier variante (`workflow/` singular) hace que el pipeline nunca se ejecute, sin emitir error.

---

## Uso local

Requisitos: Python 3.13.

```bash
# 1. Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# 2. Linting (estilo y malas prácticas)
flake8 .

# 3. Pruebas
pytest

# 4. Generar una contraseña de longitud N (mínimo 4)
python main.py 12
```

---

## CI/CD con GitHub Actions

El archivo `.github/workflows/ci.yml` define el pipeline. En cada `push` / `pull_request` ejecuta, en orden:

1. **Checkout** del código en el runner.
2. **Setup de Python**.
3. **Instalación** de dependencias de desarrollo.
4. **Linting** con `flake8` (si falla, el workflow falla).
5. **Pruebas** con `pytest` (si fallan, el workflow falla).
6. **Login** a GHCR con el `GITHUB_TOKEN` provisto por GitHub.
7. **Build & push** de la imagen Docker.

> **Autenticación:** el pipeline usa `${{ secrets.GITHUB_TOKEN }}`, un token efímero que GitHub inyecta automáticamente en cada ejecución. No se almacenan credenciales en el repositorio.

El estado (éxito/fallo) aparece en la pestaña **Actions** del repositorio y como *check* en cada pull request.

---

## Glosario (bilingüe)

| Español | Inglés / técnico |
|---------|------------------|
| Integración/entrega continua | Continuous Integration / Delivery (CI/CD) |
| Flujo de trabajo | Workflow |
| Corredor | Runner |
| Registro de contenedores | Container registry (GHCR) |
| Generador pseudoaleatorio no criptográfico | Non-cryptographic PRNG |
| Generador pseudoaleatorio criptográficamente seguro | CSPRNG |

---

## Licencia

Ver `LICENSE`.

---

_Repositorio con fines educativos. El código se mantiene fiel al material del curso; las decisiones de seguridad están divulgadas en la sección correspondiente._