def get_class(id):
    if id == '1':
        from sources.exxon import Exxon
        return Exxon()
    elif id == '2':
        from sources.cvs import Cvs
        return Cvs()
    elif id == '3':
        from sources.mckesson import Mckesson
        return Mckesson()
    elif id == '4':
        from sources.jpm import Jpm
        return Jpm()
    elif id == '5':
        from sources.kroger import Kroger
        return Kroger()
    elif id == '6':
        from sources.archer import Archer
        return Archer()
    elif id == '7':
        from sources.metlife import Metlife
        return Metlife()
    elif id == '8':
        from sources.homedepot import Homedepot
        return Homedepot()
    elif id == '9':
        from sources.pepsico import Pepsico
        return Pepsico()
    elif id == '10':
        from sources.state import State
        return State()
    elif id == '11':
        from sources.wellpoint import Wellpoint
        return Wellpoint()
    elif id == '12':
        from sources.fannie import Fannie
        return Fannie()
    elif id == '13':
        from sources.boeing import Boeing
        return Boeing()
    elif id == '14':
        from sources.comcast import Comcast
        return Comcast()
    elif id == '15':
        from sources.merck import Merck
        return Merck()
    elif id == '16':
        from sources.lockheed import Lockheed
        return Lockheed()
    elif id == '17':
        from sources.sunoco import Sunoco
        return Sunoco()
    elif id == '18':
        from sources.safeway import Safeway
        return Safeway()
    elif id == '19':
        from sources.johnson import Johnson
        return Johnson()
    elif id == '20':
        from sources.fedex import Fedex
        return Fedex()
    elif id == '21':
        from sources.abbott import Abbott
        return Abbott()
    elif id == '22':
        from sources.unitedcont import Unitedcont
        return Unitedcont()
    elif id == '23':
        from sources.liberty import Liberty
        return Liberty()
    elif id == '24':
        from sources.delta import Delta
        return Delta()
    elif id == '25':
        from sources.nylife import Nylife
        return Nylife()
    elif id == '26':
        from sources.aetna import Aetna
        return Aetna()
    elif id == '27':
        from sources.sprint import Sprint
        return Sprint()
    elif id == '28':
        from sources.allstate import Allstate
        return Allstate()
    elif id == '29':
        from sources.amex import Amex 
        return Amex()
    elif id == '30':
        from sources.deere import Deere
        return Deere()
    elif id == '31':
        from sources.amazon import Amazon
        return Amazon()
    elif id == '32':
        from sources.apple import Apple
        return Apple()
    elif id == '33':
        from sources.boa import Boa
        return Boa()
    elif id == '34':
        from sources.citi import Citi
        return Citi()
    elif id == '35':
        from sources.ford import Ford
        return Ford()
    elif id == '36':
        from sources.ibm import Ibm
        return Ibm()
    elif id == '37':
        from sources.microsoft import Microsoft
        return Microsoft()
    elif id == '38':
        from sources.morgan import Morgan
        return Morgan()
    elif id == '39':
        from sources.target import Target
        return Target()
    elif id == '40':
        from sources.wf import Wf
        return Wf()
    else:
        raise Exception("class not found for id: " + id)
