from app.businsystem import businsystem
from app import db
from app.businsystem.forms import BusinSysInfoForm
from app.models import TableInfo, BusinSysInfo, InterfaceFile, SystemInfo, HardwareInfo
from flask import render_template, url_for, redirect, flash, session, request, make_response, g
from werkzeug.utils import secure_filename
from functools import wraps