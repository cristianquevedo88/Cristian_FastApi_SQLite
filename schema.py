from pydantic import BaseModel


class AprendizCrear(BaseModel):
    nombre: str
    documento: str
    programa: str

class AprendizRespuesta(AprendizCrear):
    id: int

    class Config:
        from_atributes = True