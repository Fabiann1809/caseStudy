# Pipeline de CI/CD — Simulador

Simulador de integración y despliegue continuo construido con **Python** y **Streamlit**. Permite gestionar trabajos de compilación, ejecutar un pipeline de 5 etapas, monitorear logs en tiempo real y revertir versiones en producción.

## Cómo ejecutar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Funcionalidades

- **Agentes de Ejecución**: 4 servidores virtuales (Ubuntu, Windows, macOS, Alpine) que procesan trabajos.
- **Cola de Trabajos**: Los trabajos entran en una cola FIFO y se asignan a servidores disponibles.
- **Pipeline**: Ejecuta 5 etapas secuenciales (Checkout → Dependencias → Linter → Tests → Despliegue).
- **Logs en Tiempo Real**: Consola con filtrado por nivel y búsqueda por palabra clave.
- **Rollback**: Cada despliegue se apila; se puede revertir a la versión anterior con un clic.
