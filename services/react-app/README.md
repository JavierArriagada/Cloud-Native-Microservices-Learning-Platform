# React Frontend

Single Page Application construida con React, TypeScript y Vite.

## Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool (ultra rápido)
- **TanStack Query** - Server state management
- **React Router** - Routing
- **Tailwind CSS** - Styling

## Estructura

```
src/
├── main.tsx          # Entry point
├── App.tsx           # App principal
├── components/       # Componentes reutilizables
├── pages/            # Páginas/vistas
├── hooks/            # Custom React hooks
├── services/         # API calls
└── types/            # TypeScript types
```

## Desarrollo

```bash
# Levantar servicio en desarrollo
make dev-up

# Ver logs
make dev-logs-react

# Ejecutar tests
make test-react

# Lint
make lint-react
```

## Características

- ✅ TypeScript strict mode
- ✅ Hot Module Replacement (HMR)
- ✅ Code splitting
- ✅ Lazy loading
- ✅ ESLint + Prettier

## Próximos pasos

- [ ] Inicializar proyecto con Vite
- [ ] Configurar TypeScript
- [ ] Configurar Tailwind CSS
- [ ] Configurar TanStack Query
- [ ] Crear componentes base
- [ ] Crear Dockerfile
