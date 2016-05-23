# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django import forms
from validate.models import User
from django.db import IntegrityError
import json

# Create your views here.

@csrf_exempt
def index(request):
    jsonRequest= json.loads(request.body)
    email=jsonRequest['email']
    password=jsonRequest['password']
    try:
        validate_email(email)
    except forms.ValidationError:
        return JsonResponse({"status":"ERROR", "message": "The mail address " + email + " is not valid"})
    else:
        if not any(p.isupper() for p in password):
            return JsonResponse({"status":"ERROR", "message": "The password should contain at least one uppercase letter"})
        if not any(p.isdigit() for p in password):
            return JsonResponse({"status":"ERROR", "message": "The password should contain at least one number"})
        if len(password)<=5:
            return JsonResponse({"status":"ERROR", "message": "The password length should be greater than 5"})
        try:
            user= User(email= email, name = jsonRequest['name'], password = password)
            user.save()
        except IntegrityError:
            return JsonResponse({"status":"ERROR", "message": "The mail address " + email + " is already in use"})
        else:
            return JsonResponse({"status":"OK","id":user.id})
