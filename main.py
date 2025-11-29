import os
from typing import Optional, List
from uuid import UUID
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
import httpx

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
TABLE = os.getenv("TABLE_LIVROS", "livros")
POSTGREST_URL = f"{SUPABASE_URL}/rest/v1"
AUTH_URL = f"{SUPABASE_URL}/auth/v1"

if not SUPABASE_URL or not ANON_KEY:
    raise RuntimeError("Configure SUPABASE_URL e SUPABASE_ANON_KEY no .env")

app = FastAPI(title="API de Livros")


class Usuario(BaseModel):
    email: str
    password: str

class LivroCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=255)
    autor: str = Field(min_length=1, max_length=255)

class LivroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=255)
    autor: Optional[str] = Field(None, min_length=1, max_length=255)

class LivroOut(BaseModel):
    id: int
    titulo: str
    autor: str
    user_id: UUID
    created_at: str
    updated_at: str


def postgrest_headers(auth: str) -> dict:
    return {
        "apikey": ANON_KEY,
        "Authorization": auth,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Prefer": "return=representation"
    }

def auth_headers() -> dict:
    return {"apikey": ANON_KEY, "Content-Type": "application/json"}

async def request_supabase(method: str, url: str, **kwargs):
    """Função centralizada para requisições HTTP + validação de erro."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.request(method, url, **kwargs)

    if r.status_code >= 400:
        try:
            msg = r.json().get("msg", r.text)
        except:
            msg = r.text
        raise HTTPException(r.status_code, msg)

    return r.json() if r.text else None


async def get_user_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Token não fornecido ou inválido")
    return authorization

async def get_user_id(auth=Depends(get_user_token)):
    token = auth.replace("Bearer ", "")
    data = await request_supabase(
        "GET",
        f"{AUTH_URL}/user",
        headers={"Authorization": f"Bearer {token}", "apikey": ANON_KEY},
    )
    return data["id"]


@app.post("/auth/registrar", status_code=201)
async def registrar(usuario: Usuario):
    return await request_supabase(
        "POST",
        f"{AUTH_URL}/signup",
        headers=auth_headers(),
        json={"email": usuario.email, "password": usuario.password},
    )

@app.post("/auth/login")
async def login(usuario: Usuario):
    return await request_supabase(
        "POST",
        f"{AUTH_URL}/token?grant_type=password",
        headers=auth_headers(),
        json={"email": usuario.email, "password": usuario.password},
    )

@app.post("/auth/logout")
async def logout(auth=Depends(get_user_token)):
    await request_supabase(
        "POST",
        f"{AUTH_URL}/logout",
        headers=postgrest_headers(auth),
    )
    return {"mensagem": "Logout realizado com sucesso"}


@app.get("/livros", response_model=List[LivroOut])
async def listar_livros(
    auth=Depends(get_user_token), 
    limit: int = 50, 
    offset: int = 0,
    search: Optional[str] = None
):
    params = {
        "select": "*",
        "limit": min(limit, 100),
        "offset": max(offset, 0),
        "order": "created_at.desc"
    }

    if search:
        params["titulo"] = f"ilike.*{search}*"

    return await request_supabase(
        "GET",
        f"{POSTGREST_URL}/{TABLE}",
        headers=postgrest_headers(auth),
        params=params,
    )

@app.get("/livros/{livro_id}", response_model=List[LivroOut])
async def listar_livro_by_id(livro_id: int, auth=Depends(get_user_token)):
    return await request_supabase(
        "GET",
        f"{POSTGREST_URL}/{TABLE}",
        headers=postgrest_headers(auth),
        params={"select": "*", "id": f"eq.{livro_id}"},
    )

@app.post("/livros", response_model=List[LivroOut], status_code=201)
async def criar_livro(payload: LivroCreate, auth=Depends(get_user_token), user_id=Depends(get_user_id)):
    data = payload.model_dump()
    data["user_id"] = user_id

    return await request_supabase(
        "POST",
        f"{POSTGREST_URL}/{TABLE}",
        headers=postgrest_headers(auth),
        json=data,
    )

@app.put("/livros/{livro_id}", response_model=List[LivroOut])
async def editar_livro_by_id(livro_id: int, payload: LivroUpdate, auth=Depends(get_user_token)):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}

    if not data:
        raise HTTPException(400, "Nenhum campo para atualizar")

    return await request_supabase(
        "PATCH",
        f"{POSTGREST_URL}/{TABLE}",
        headers=postgrest_headers(auth),
        params={"id": f"eq.{livro_id}"},
        json=data,
    )

@app.delete("/livros/{livro_id}", status_code=204)
async def excluir_livro_by_id(livro_id: int, auth=Depends(get_user_token)):
    await request_supabase(
        "DELETE",
        f"{POSTGREST_URL}/{TABLE}",
        headers=postgrest_headers(auth),
        params={"id": f"eq.{livro_id}"},
    )
    return None
