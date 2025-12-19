# Documentación del Proyecto

Esta carpeta `docs/` contiene la documentación técnica y operativa del proyecto.

Propósito
- Centralizar conceptos, guías y tutoriales relacionados con el desarrollo, pruebas, despliegue y operación de la plataforma.
- Mantener instrucciones prácticas para entornos local y cloud, incluyendo Docker Compose, Kubernetes y pipelines de CI/CD.
- Documentar decisiones arquitectónicas, convenciones de código, formatos de configuración y procedimientos de recuperación.

Contenido esperado
- Conceptos y arquitectura: diagramas, contexto, componentes y flujos de datos.
- Guías de desarrollo: cómo ejecutar servicios localmente, ejecutar tests y flujos comunes de desarrollo.
- Guías de despliegue: CI/CD, despliegue a staging/producción, configuración de infraestructura.
- Operación y mantenimiento: monitoreo, logging, backups, escalado y troubleshooting.
- Portabilidad: cómo adaptar la plataforma a otros proveedores cloud o entornos on-premise.
- Plantillas y ejemplos: snippets de `docker-compose`, manifests de Kubernetes, snippets de GitHub Actions, y archivos `.env` de ejemplo.

Cómo contribuir
- Añade archivos nuevos bajo `docs/` siguiendo la convención `docs/<tema>/README.md` o `docs/<tema>.md`.
- Mantén un índice actualizado en `docs/README.md` si agregas secciones nuevas.
- Los cambios en la documentación deben incluirse en PRs con una breve descripción del objetivo y, si aplica, comandos para reproducir los ejemplos.

Contacto
- Para dudas sobre la documentación abre un issue en el repositorio o contacta al equipo responsable del proyecto.

## Índice de la documentación (actual)

- [MICROSERVICES_MASTER_PLAN.md](MICROSERVICES_MASTER_PLAN.md) — Documento maestro de planificación y arquitectura (arquitectura, stack, guías, diagramas).
- [README.md](/README.md) — Presentación del repo y resumen del proyecto.

> Nota: este índice debe actualizarse cada vez que se añada un nuevo documento en `docs/`.

## Formato y convenciones

- Formato: todos los documentos deben estar en Markdown (`.md`).
- Diagramas: use Mermaid dentro de bloques triple-backtick con la etiqueta `mermaid` (por ejemplo, ```mermaid). Evite sintaxis Mermaid no soportada por GitHub (use flowcharts, sequence, and standard diagrams); los bloques C4 especiales pueden fallar en el renderizador de GitHub.
- Nombres: prefiera `docs/<tema>/README.md` para secciones completas, o `docs/<tema>.md` para documentos sueltos.
- Enlaces: cuando agregue un documento, añádalo a la sección "Índice de la documentación (actual)" aquí.

## Cómo agregar nueva documentación

1. Crear el archivo Markdown en `docs/` o en un subdirectorio (p. ej. `docs/deployment/README.md`).
2. Incluir un breve resumen al inicio y una sección de contenidos si el documento es largo.
3. Añadir diagramas Mermaid usando bloques etiquetados `mermaid`.
4. Actualizar este `docs/README.md` para añadir el nuevo documento al índice.
5. Abrir un PR con la descripción del cambio de documentación y, si procede, capturas o ejemplos para visualización.

Si quieres, puedo actualizar automáticamente el índice cuando agregues nuevos archivos en `docs/`.
