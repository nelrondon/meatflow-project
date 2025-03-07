# Sistema de Gestión Financiera para Carnicerías "MeatFlow"

## Descripción

Proyecto universitario para resolver problemas financieros y de gestión en carnicerías pequeñas-medianas mediante un sistema orientado a objetos en Python. Optimiza inventario, ventas, compras y análisis de datos.

## Problema a Resolver

- **Desperdicio de materia prima** por mal manejo de inventario.
- **Margen de ganancia reducido** por despieces ineficientes y compras mal planificadas.
- **Falta de visibilidad** sobre productos rentables y preferencias de clientes.

## Solución Propuesta

Un sistema modular en Python que:

- Automatiza control de inventario y alertas.
- Analiza ventas históricas para recomendaciones estratégicas.
- Optimiza despieces y relación con clientes.

---

## Estructura del Sistema

### Módulos y Funcionalidades

#### Módulo 1: Gestión de Inventario

- **Clases**: `Producto`, `Inventario`, `Procesamiento`
- **Funcionalidades**:
  - Alertas de stock mínimo y caducidad.
  - Cálculo de desperdicio en despieces (% aprovechamiento).
  - Sugerencias para reducir stock según rotación.

#### Módulo 2: Ventas y Clientes

- **Clases**: `Venta`, `Cliente`
- **Funcionalidades**:
  - Registro de ventas con puntuación de atención.
  - Análisis de clientes recurrentes.
  - Tickets personalizados con promociones.

#### Módulo 3: Proveedores y Compras

- **Clases**: `Proveedor`, `Compra`
- **Funcionalidades**:
  - Evaluación de proveedores (calidad, tiempo de entrega).
  - Detección de "malas compras" (costo vs. calidad).

#### Módulo 4: Análisis y Reportes

- **Clases**: `Reporte`
- **Funcionalidades**:
  - Gráficos de participación en ventas (ej: 40% cortes delanteros).
  - Recomendaciones para subproductos (hamburguesas, huesos).
  - Predicción de demanda usando tendencias históricas.

---

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/nelrondon/meatflow-project.git
   ```

2. Instala las dependencias:

   ```bash
   pip install requirements.txt
   ```

3. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
