from fastapi import FastAPI,Request,Depends,Form
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from database.database import engine, SessionLocal
from model import basemodel
from fastapi.templating import Jinja2Templates
app = FastAPI()
basemodel.Base.metadata.create_all(bind=engine)
# templates = Jinja2Templates(directory="templates")
tmp = Jinja2Templates(directory = "template")
tb=basemodel.Contact.__tablename__
app.mount("/assets",StaticFiles(directory="static/assets/"),name="assets")
@app.get("/")
async def view_index(request:Request):
    return tmp.TemplateResponse(request=request,name="index.html")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/index")
async def view_home(request: Request, db: Session = Depends(get_db)):
    contacts = db.query(basemodel.Contact).all()

    return tmp.TemplateResponse(
        "index.html",
        {
            "request": request,
            "total_contacts": len(contacts),
            "new_contacts": 0,
            "deleted_contacts": 0
        }
    )

@app.get("/sign-in")
async def sign_in(request:Request):
    return tmp.TemplateResponse(request=request,name="auth-signin.html")

@app.get("/edit")
async def edit(request:Request):
    return tmp.TemplateResponse(request=request,name="edit.html")


@app.get("/add")
async def add(request:Request):
    return tmp.TemplateResponse(request=request,name="add.html")

@app.get("/about")
async def about(request:Request):
    return tmp.TemplateResponse(request=request,name="about.html")

@app.get("/contact")
async def view_contact(request: Request,db:Session = Depends(get_db)):
    contact = db.query(basemodel.Contact).all()
    db.commit()
    return tmp.TemplateResponse(request=request,name="contacts.html",context={"contact":contact})

@app.post("/contact")
async def view_contact_get(request: Request,db:Session = Depends(get_db)):
    contact = db.query(basemodel.Contact).all()
    db.commit()
    return tmp.TemplateResponse(request=request,name="contacts.html",context={"contact":contact})



@app.post("/add_data")
def add_data(request:Request,name:Annotated[str,Form()],lastname:Annotated[str,Form()],mobile_number:Annotated[int,Form()],db:Session=Depends(get_db)):
    db.add(basemodel.Contact(name=name,lastname=lastname,mobile_number=mobile_number))
    db.commit()
    return RedirectResponse(url="/contact", status_code=303)


@app.get("/update/{u_id}")
async def del_contact(u_id:int,request:Request,db:Session = Depends(get_db)):
    contact=db.query(basemodel.Contact).filter(basemodel.Contact.id==u_id)
    db.commit()
    return tmp.TemplateResponse(request=request,name="edit.html",context={"contact":contact})

@app.post("/update_data/{u_id}")
async def update_data(u_id:int,request:Request,name:Annotated[str,Form()],lastname:Annotated[str,Form()],mobile_number:Annotated[int,Form()],db:Session=Depends(get_db)):
    contact_item = db.query(basemodel.Contact).filter(basemodel.Contact.id==u_id).first()
    contact_item.name = name
    contact_item.lastname = lastname
    contact_item.mobile_number = mobile_number
    db.commit()
    return RedirectResponse(url="/contact", status_code=303)
@app.get("/delete/{d_id}")
async def del_contact(request:Request,d_id:int,db:Session = Depends(get_db)):
    query=db.query(basemodel.Contact).filter(basemodel.Contact.id == d_id).first()
    db.delete(query)
    db.commit()
    return RedirectResponse(url="/contact", status_code=303)