# 📁 ESTRUCTURA DE ESTILOS - CLIENTE

## Ubicación
```
Cliente/
├── static/
│   └── Cliente/
│       └── css/
│           ├── base.css          # Estilos globales y variables
│           ├── login.css         # Estilos específicos de login
│           └── dashboard.css     # Estilos específicos de dashboard
└── templates/
    └── Cliente/
        ├── login.html           # Usa: base.css + login.css
        └── dashboard.html       # Usa: base.css + dashboard.css
```

---

## 📄 DESCRIPCIÓN DE ARCHIVOS

### `base.css`
- **Variables CSS:** Colores, tipografía, gradientes (reutilizable)
- **Estilos globales:** Reset, body, formularios, botones, mensajes
- **Responsive:** Media queries para todos los dispositivos

**Variables principales:**
```css
--primary: #1877f2
--primary-dark: #0056b3
--secondary: #2e7d32
--error-color: #dc3545
--bg-gradient: linear-gradient(135deg, #f0f2f5 0%, #c3cfe2 100%)
--card-bg: rgba(255, 255, 255, 0.98)
```

### `login.css`
- **Estilos específicos** para la página de login
- **Componentes:** login-container, logo-circle, form-group
- **Responsive:** Adaptado para móvil, tablet, desktop

### `dashboard.css`
- **Estilos específicos** para el dashboard
- **Componentes:** container, botones (btn-primary, btn-secondary)
- **Animaciones:** slideUp, hover effects
- **Responsive:** Diseño adaptable

---

## 🎨 CÓMO USAR

### En un Template:
```html
{% load static %}
<link rel="stylesheet" href="{% static 'Cliente/css/base.css' %}">
<link rel="stylesheet" href="{% static 'Cliente/css/login.css' %}">
```

### Agregar una clase personalizada:
```html
<div class="login-container">
    <!-- contenido -->
</div>
```

---

## 📝 PALETA DE COLORES

| Variable | Valor | Uso |
|----------|-------|-----|
| `--primary` | #1877f2 | Botones principales, links |
| `--primary-dark` | #0056b3 | Hover de botones principales |
| `--secondary` | #2e7d32 | Botones secundarios |
| `--error-color` | #dc3545 | Errores y alertas |
| `--text-main` | #1c1e21 | Texto principal |
| `--text-muted` | #65676b | Texto secundario, descripciones |
| `--border-color` | #e5e5e5 | Bordes |
| `--card-bg` | rgba(255,255,255,0.98) | Fondo de cards |

---

## 📱 BREAKPOINTS RESPONSIVE

```css
Desktop:    > 768px
Tablet:     768px
Mobile:     480px
```

---

## ✨ CARACTERÍSTICAS

✅ Variables CSS reutilizables
✅ Estilos modulares (base + específicos)
✅ Completamente responsive
✅ Transiciones y animaciones suaves
✅ Accesibilidad (focus states)
✅ Sin librerías externas (CSS puro)
✅ Fácil de mantener y escalar

---

## 🔧 PARA AGREGAR NUEVAS PÁGINAS

1. Crea un nuevo archivo `nueva_pagina.css` en `Cliente/static/Cliente/css/`
2. Define los estilos específicos para esa página
3. En el template, agrega:
   ```html
   {% load static %}
   <link rel="stylesheet" href="{% static 'Cliente/css/base.css' %}">
   <link rel="stylesheet" href="{% static 'Cliente/css/nueva_pagina.css' %}">
   ```
4. Usa las variables CSS del `base.css` para mantener consistencia

---

## 🎯 BUENAS PRÁCTICAS

- ✅ Siempre importa `base.css` primero
- ✅ Usa variables CSS en lugar de valores hardcodeados
- ✅ Mantén los breakpoints responsive
- ✅ Agrupa estilos por componente
- ✅ Comenta secciones principales
