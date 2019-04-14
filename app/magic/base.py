#!/usr/bin/env python
# -*- coding: utf8 -*-

from app.magic import smssend

def send_sms(phone):
    return smssend.send(phone)
