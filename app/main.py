from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from pydantic import BaseModel

# URL do banco de dados. O SQLite cria um arquivo local chamado items.db
DATABASE_URL = "sqlite:///./items.db"

# O engine é responsável por conectar o SQLAlchemy ao banco
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necessário para SQLite em aplicações web
)

# Cria uma fábrica de sessões para abrir e fechar conexões com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Modelo da tabela no banco de dados
class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)


# Cria as tabelas quando a aplicação inicia
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD com FastAPI e SQLAlchemy", version="1.0.0")


# Esquema de entrada para criar um item
class ItemCreate(BaseModel):
    title: str
    description: str | None = None


# Esquema de entrada para atualizar um item
class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


# Esquema de saída para mostrar um item
class ItemRead(BaseModel):
    id: int
    title: str
    description: str | None = None

    model_config = {"from_attributes": True}


# Função que devolve uma sessão do banco para cada requisição
# Isso evita vazamento de conexões

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Início"])
def read_root():
    return {"mensagem": "API CRUD funcionando! Acesse /docs para testar."}


@app.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED, tags=["Itens"])
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Cria um objeto do modelo SQLAlchemy com os dados recebidos
    novo_item = Item(title=item.title, description=item.description)

    # Adiciona e salva no banco
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)

    return novo_item


@app.get("/items", response_model=list[ItemRead], tags=["Itens"])
def list_items(db: Session = Depends(get_db)):
    # Busca todos os registros da tabela items
    return db.query(Item).all()


@app.get("/items/{item_id}", response_model=ItemRead, tags=["Itens"])
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return item


@app.put("/items/{item_id}", response_model=ItemRead, tags=["Itens"])
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    # Atualiza apenas os campos que foram enviados
    if item_data.title is not None:
        item.title = item_data.title

    if item_data.description is not None:
        item.description = item_data.description

    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Itens"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    db.delete(item)
    db.commit()

    return None
