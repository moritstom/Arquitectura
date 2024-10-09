# views.py
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import PuntoDeInteres, Evento
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def mapa():
    # Obtener todos los puntos de interés
    puntos = PuntoDeInteres.query.all()
    puntos_geojson = []
    for punto in puntos:
        puntos_geojson.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [punto.longitud,punto.latitud]
            },
            'properties': {
                'nombre': punto.nombre,
                'descripcion': punto.descripcion,
                'tipo': 'punto_de_interes',
                'imagenes': punto.imagenes,
                'apertura': punto.apertura,
                'cierre': punto.cierre,
                'fecha_creacion': punto.fecha_creacion.isoformat()
            }
        })

    # Obtener todos los eventos
    eventos = Evento.query.all()
    eventos_geojson = []
    for evento in eventos:
        eventos_geojson.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [evento.longitud,evento.latitud]
            },
            'properties': {
                'nombre': evento.nombre,
                'descripcion': evento.descripcion,
                'tipo': 'evento',
                'imagenes': evento.imagenes,
                'fecha_inicio': evento.fecha_inicio.isoformat(),
                'duracion': evento.duracion,
                'fecha_creacion': evento.fecha_creacion.isoformat()
            }
        })

    # Crear un FeatureCollection combinando los puntos de interés y los eventos
    mapa_data = {
        'type': 'FeatureCollection',
        'features': puntos_geojson + eventos_geojson
    }

    # Renderizar el template y pasar los datos al frontend
    return render_template("mapa.html", user=current_user, mapa_data=json.dumps(mapa_data))

@views.route('/api/puntos_interes')
def get_puntos_interes():
    puntos = PuntoDeInteres.query.all()
    puntos_geojson = []
    for punto in puntos:
        puntos_geojson.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [punto.longitud,punto.latitud]
            },
            'properties': {
                'nombre': punto.nombre,
                'descripcion': punto.descripcion,
                'tipo': 'punto_de_interes',
                'imagenes': punto.imagenes,
                'apertura': punto.apertura,
                'cierre': punto.cierre,
                'fecha_creacion': punto.fecha_creacion.isoformat()
            }
        })
    return jsonify({
        'type': 'FeatureCollection',
        'features': puntos_geojson
    })

@views.route('/api/eventos')
def get_eventos():
    eventos = Evento.query.all()
    eventos_geojson = []
    for evento in eventos:
        eventos_geojson.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [evento.longitud,evento.latitud]
            },
            'properties': {
                'nombre': evento.nombre,
                'descripcion': evento.descripcion,
                'tipo': evento.tipo,
                'imagenes': evento.imagenes,
                'fecha_inicio': evento.fecha_inicio.isoformat(),
                'hora_incio': evento.hora_inicio.isoformat(),
                'hora_fin': evento.hora_fin.isoformat(),
                'fecha_creacion': evento.fecha_creacion.isoformat()
            }
        })
    return jsonify({
        'type': 'FeatureCollection',
        'features': eventos_geojson
    })
    
@views.route('/nuevo_punto', methods=['GET', 'POST'])
def nuevo_punto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        tipo = request.form['tipo']
        apertura = request.form['apertura']
        cierre = request.form['cierre']
        
        nuevo_punto = PuntoDeInteres(
            nombre=nombre,
            descripcion=descripcion,
            latitud=latitud,
            longitud=longitud,
            tipo=tipo,
            apertura=apertura,
            cierre=cierre,
            user_id=current_user.id
        )
        
        db.session.add(nuevo_punto)
        db.session.commit()
        flash('Punto de Interés creado con éxito.')
        return redirect(url_for('views.nuevo_punto'))

    return render_template('nuevo_punto.html')

@views.route('/nuevo_evento', methods=['GET', 'POST'])
def nuevo_evento():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        tipo = request.form['tipo']
        fecha_inicio = request.form['fecha_inicio']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']
        
        # nuevo_evento dejarselo a un controlador
        #esto de crear evento y subirlo a la BD que lo haga un controlador
        nuevo_evento = Evento(
            nombre=nombre,
            descripcion=descripcion,
            latitud=latitud,
            longitud=longitud,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            user_id=current_user.id
        )
        
        db.session.add(nuevo_evento)
        db.session.commit()
        flash('Evento creado con éxito.')
        return redirect(url_for('views.nuevo_evento'))

    return render_template('nuevo_evento.html')
