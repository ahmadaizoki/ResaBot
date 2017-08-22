#!/usr/bin/env python
# -*- coding: utf-8 -*-

def photo(room):
    if room=="Standard-Room":
        url="https://mediastore.hotelcontent.net/e87b6078574cc3417cc6f3a76cec4562/2544e5b1e7659a7/f24ae6a615e106bf9b68bc9fc24d36db.jpg"
    elif room=="Camera-Deluxe":
        url="https://mediastore.hotelcontent.net/e87b6078574cc3417cc6f3a76cec4562/2544e5b1e7659a7/9e562e28dd9cca7c701b4c80c308c999.jpg"
    elif room=="Grand-Suite":
        url="https://mediastore.hotelcontent.net/e87b6078574cc3417cc6f3a76cec4562/2544e5b1e7659a7/cf3b8ff8bfd5052b7becefd0ad091028.jpg"
    elif room=="Junior-Suite":
        url="https://mediastore.hotelcontent.net/e87b6078574cc3417cc6f3a76cec4562/2544e5b1e7659a7/733cc1a7f830e50b7114844f911d06ac.jpg"
    elif room=="Suite":
        url="https://mediastore.hotelcontent.net/e87b6078574cc3417cc6f3a76cec4562/2544e5b1e7659a7/a8bc35ef371f4a223896072d5fe6b3ab.jpg"
    elif room=="Suite-Presidenziale":
        url="https://mediastore.hotelcontent.net/e87b6078574cc3417cc6f3a76cec4562/2544e5b1e7659a7/a7011710decdd6632c1fa259051f1cdd.jpg"
    else:
        url=""
    return url
