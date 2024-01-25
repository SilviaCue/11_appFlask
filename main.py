from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea

app = Flask(__name__) # Objeto para iniciar el servidor de Flask pero solo se arranca con app.run

@app.route("/")
def home():
    todas_las_tareas = db.session.query(Tarea).all()
    #for i in todas_las_tareas:
        #print(i)
    return render_template("index.html", lista_de_tareas = todas_las_tareas)

@app.route("/crear-tarea", methods=["POST"])
def crear():
    tarea = Tarea(contenido=request.form["contenido_tarea"], hecha= False)
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home")) # nos redirecciona a la función home()

@app.route("/eliminar-tarea/<id>")
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id))
    tarea.delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    return redirect(url_for("home"))

##PARA EDITAR

@app.route("/editar-tarea/<id>", methods=["GET", "POST"])
def editar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()

    if request.method == "POST":
        nueva_tarea = request.form["nueva_tarea"]
        tarea.contenido = nueva_tarea
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("editar_tarea.html", tarea=tarea)


   # persona_id = int(input('Id de la persona: '))
    #person = db.session.query(Persona).filter(Persona.id_persona == persona_id).first()

   # if person is None:
       # print('La persona indicada no existe')
    #else:
       # print(person)
       # edad_nueva = int(input('Introduzca la nueva edad: '))
       # person.edad = edad_nueva
      #  db.session.commit()
       # db.session.close()
       # print('Persona actualizada')

##PARA EDITAR


if __name__ =="__main__":

    #db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)  # sirve para hacer pruebas y resetear la db

    # si solo queremos añadir datos cometarla #db.Base.metada.drop_(bind=db.engine, checkfirst=True)

    db.Base.metadata.create_all(db.engine)  # diciendo que cree las tablas de models.py que no existen CREA LA DB!!!!
# si queremos hacer cambios en la estructura de la db y queremos que se reflege ir a carpetas y borrar db o reiniciar

    app.run(debug=True) # SIEMPRE TIENE QUE IR AL FINAL DEL MAIN


