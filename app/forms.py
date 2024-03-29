from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators, SelectField, RadioField
from wtforms.fields.html5 import EmailField

from datetime import date, datetime

class loginForm(FlaskForm):
    usuario = StringField('Usuario', 
                [validators.Required(message='El campo usuario es requerido! '), 
                validators.length(min=3, max=25, message='Ingrese un usuario valido')] )
    contraseña = PasswordField('Contraseña',
                    [validators.Required(message='El campo contraseña es requerido')])
    recordar = BooleanField('Recordar Usuario')
    login = SubmitField('Iniciar Sesión')
    
class registerForm(FlaskForm):
    nombre = StringField('',[ validators.Required(message='El campo nombre es requerido! '), 
                            validators.length(min=3, max=25, message='Ingrese un usuario valido')], render_kw={"placeholder": "Nombre"})
    apellido = StringField('',[ validators.Required(message='El campo apellido es requerido! '), 
                            validators.length(min=3, max=25, message='Ingrese un usuario valido')], render_kw={"placeholder": "Apellido"})                            
    usuario = StringField('',[ validators.Required(message='El campo usuario es requerido! '), 
                            validators.length(min=3, max=25, message='Ingrese un usuario valido')], render_kw={"placeholder": "Usuario"})
    email = EmailField('',[ validators.Required( message='El Email es requerido'),
                        validators.Email(message='Ingrese un email valido')], render_kw={"placeholder": "Email"})
    contraseña = PasswordField('',[ validators.Required(message='El campo contraseña es requerido')], render_kw={"placeholder": "Contraseña"})
        
    days   = [(x,x) for x in range(1,32)]
    months = [(x,x) for x in range(1,13)]
    years  = [(x,x) for x in range(date.today().year,date.today().year-100,-1)]
    # fecha =  DateTimeField('')
    dia = SelectField('',choices = days)
    mes = SelectField('',choices = months)
    año = SelectField('',choices = years)

    sexo = RadioField('', choices=[('1','Hombre'),('2','Mujer'),('3','Otro')])
    register = SubmitField('Registrarse')
   

# genero = SelectField('Genero', choices=[(1, 'Acción'), (2, 'Aventuras'), (3, 'Ciencia Ficción'), (4, 'Comedia'), (5, 'Documental'), (6, 'Drama'), (7, 'Fantasía'), (8, 'Musical'), (9, 'Suspenso'), (10, 'Terror')], validators=[
#         DataRequired(message='Campo Requerido')])
# estreno = DateField('Estreno', validators=[
#         DataRequired(message='Campo Requerido')])
# <div class="col-4 form-floating mb-3">
#                         {{ form.genero(class_='form-control',id='floatingSelect',placeholder='#')}}
#                         {{ form.genero.label(for='floatingSelect') }}
#                     </div>
# <div class="col-4 form-floating mb-3">
#                         {{ form.estreno(class_='datepicker
#                         form-control',id='floatingInput',placeholder='#')}}{{form.hidden_tag()}}
#                         {{ form.estreno.label(for='floatingInput') }}
#                     </div>