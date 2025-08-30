from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, auth, business

app = FastAPI(
    title="PymeMap API",
    description="Esta es una API de ejemplo con rutas modulares de la aplicacion PymeMap.",
    version="beta",
)

# Configuración de CORS
# En un entorno de producción, deberías restringir los orígenes permitidos.
# origins = ["
#     "http://localhost:3000",
#     "https://tu-dominio-de-frontend.com",
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(business.router, prefix="/business", tags=["Business"])


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}
