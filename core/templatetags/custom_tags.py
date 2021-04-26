from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    splt_arg, index_split = arg.split(' ')
    return value.split(splt_arg)[int(index_split)]

@register.simple_tag
def direktur_auth(rumahsakits, rumahsakits_confirmed):
    try: rumahsakit_id = [rumahsakit.id for rumahsakit in rumahsakits]
    except: rumahsakit_id = [rumahsakit['id'] for rumahsakit in rumahsakits]
    rumahsakit_id_confirmed = [rumahsakit['rumahsakit'] for rumahsakit in rumahsakits_confirmed]
    print(rumahsakit_id, rumahsakit_id_confirmed)
    return any(item in rumahsakit_id_confirmed for item in rumahsakit_id)

@register.simple_tag
def reg_humas_lists(reg_rs_id, regis_humas_lists):
    for reg_humas in regis_humas_lists:
        if reg_humas['register_rumahsakit'] == reg_rs_id: return reg_humas
        else: continue