# Dash Dashboard

Dashboard interactivo construido con Dash y Plotly.

## Características

- ✅ Visualizaciones interactivas con Plotly
- ✅ Callbacks para actualización en tiempo real
- ✅ Integración con FastAPI backend
- ✅ Responsive design

## Estructura

```
app/
├── main.py           # Entry point de la aplicación
├── layouts/          # Layouts de páginas
├── components/       # Componentes reutilizables
└── callbacks/        # Callbacks de interactividad
```

## Desarrollo

```bash
# Levantar servicio en desarrollo
make dev-up

# Ver logs
make dev-logs-dash

# Shell en container
make dev-shell-dash
```

## Próximos pasos

- [ ] Crear `main.py` con Dash app
- [ ] Implementar layout principal
- [ ] Crear gráficos de ejemplo
- [ ] Conectar con API
- [ ] Crear Dockerfile
