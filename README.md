# LegalLens AI

LegalLens AI es una plataforma SaaS diseñada para automatizar la auditoría de contratos legales (Alquiler y NDA) utilizando Inteligencia Artificial. El sistema detecta cláusulas abusivas, resume puntos clave y emite alertas legales de forma automática.

## Guía de Inicio Rápido

Para levantar el proyecto completo en un entorno profesional (Docker), sigue estos pasos:

1. **Construir y levantar los contenedores**:
   ```bash
   docker-compose up -d --build
   ```

2. **Aplicar las migraciones de la base de datos**:
   ```bash
   docker-compose exec app_django python /app/app_django/manage.py migrate
   ```

3. **Crear un superusuario (opcional para el Admin)**:
   ```bash
   docker-compose exec app_django python /app/app_django/manage.py createsuperuser
   ```

4. **Acceso**:
   - Web App: [http://localhost:8000](http://localhost:8000)
   - API Engine (FastAPI): [http://localhost:8002](http://localhost:8002)

---

## Variables de Entorno (.env)

Crea un archivo `.env` en la raíz del proyecto basándote en este formato:

```env
# Google Gemini Config
GOOGLE_API_KEY=tu_clave_aqui

# Django Config (opcional, tiene valores por defecto en settings.py)
POSTGRES_DB=legallens
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## Esquema de Clases: Programación Orientada a Objetos (POO)

Para garantizar la escalabilidad del sistema, hemos implementado una arquitectura basada en dos patrones de diseño principales:

### 1. Patrón Template Method (Método Plantilla)
La clase abstracta `Contrato` define el esqueleto del algoritmo de auditoría en el método `ejecutar_auditoria()`. Las subclases (`ContratoAlquiler` y `ContratoNDA`) heredan de ella e implementan el método `obtener_prompt_especifico()`, permitiendo que cada tipo de contrato tenga sus propias reglas de negocio sin duplicar código.

### 2. Patrón Factory (Fábrica)
La clase `ContratoFactory` centraliza la creación de los objetos. Recibe el tipo de contrato desde la web app y decide instancia la clase adecuada de forma polimórfica, facilitando la adición de nuevos tipos de contratos (ej: Contratos de Trabajo) en el futuro.

---

## Estructura del Proyecto

- `app_django/`: Aplicación principal de gestión, modelos y panel de control.
- `AI/`: Motor de procesamiento de IA con lógica POO y Agente IA.
- `dataset/`: Carpeta con los PDFs de prueba (Correctos y Fraudulentos).
- `nginx/`: Configuración del proxy inverso (en proceso).
- `docker-compose.yml`: Orquestación de microservicios (Django, FastAPI, Postgres, Nginx).