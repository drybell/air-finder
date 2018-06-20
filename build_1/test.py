from opensky_api import OpenSkyApi

api = OpenSkyApi()
states = api.get_states(Daedan, HodgeWilson69)
for s in states.states:
    print("(%r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude, s.velocity))