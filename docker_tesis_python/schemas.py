from pydantic import BaseModel

class UsuarioBase(BaseModel):
    usuario: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioUpdate(BaseModel):
    contraseña: str

class UsuarioOut(UsuarioBase):
    contraseña: str

    class Config:
        orm_mode = True
