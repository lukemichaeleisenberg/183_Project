# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = 'CareConnect'
response.subtitle = T('Community-Based Health Providers')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Luke Eisenberg <leisenbe@ucsc.edu>'
response.meta.description = 'A community supported healthcare database.'
response.meta.keywords = 'Santa Cruz, free, healthcare, clinic, clinics, community, supported, health, services, python'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), []),
    (T('For Providers'), False, URL('default','providers'), []),
    (T('Edit Your Clinic'), False, URL('default','edit'), []),
    (T('Administrators'), False, URL('default','manage'), [])
    ]
