#Archivo firma.py
from flask import Flask, request,  redirect, url_for, render_template, jsonify

import json

from config import _credential
from functions import blockchain, credential
from cadena import Cadena
import test
def firma_():
    if not blockchain():
        return redirect(url_for('scb'))
    if not credential():
        return redirect(url_for('newnodo'))
    cpu_before, mem_before = test.measure_resources_before()
    lat_get = test.start_timer()
    blockchain_ = Cadena()
    signlist=blockchain_.bd_listfirma()
    #return jsonify(signlist[::-1])
    test.measure_resources_after("INTERFAZ FIRMA" ,cpu_before, mem_before,lat_get )
    test.salt()
    return render_template('listafirma.html', datablockf=signlist[::-1])