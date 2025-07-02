from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.ciclo_service import (
    crear_ciclo,
    obtener_ciclos,
    obtener_ciclo_por_id,
    actualizar_ciclo,
    eliminar_ciclo
)