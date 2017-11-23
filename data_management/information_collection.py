import threading
from data_management.information_management import information_receive_send


class Information_Collection_Thread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, socket, info, local_models, t):
        threading.Thread.__init__(self)
        self.socket = socket
        self.info = info
        self.local_models = local_models
        self.t = t

    def run(self):
        self.local_models = information_collection_updating(self.socket, self.info, self.local_models, self.t)


def information_collection_updating(*args):
    socket = args[0]
    info = args[1]
    models = args[2]
    T = args[3]

    info = information_receive_send.information_receive(socket, info, 2)
    # Update profiles
    ug_info = info.dg[0]
    dg_info = info.dg[1]
    ess_info = info.ess[0]
    pv_info = info.pv[0]
    wp_info = info.wp[0]
    load_ac_info = info.load_ac[0]
    load_uac_info = info.load_ac[1]
    load_dc_info = info.load_dc[0]
    load_udc_info = info.load_dc[1]
    bic_info = info.bic[0]
    ### Update the availability information

    models["DG"]["GEN_STATUS"] = [0]*T
    models["UG"]["GEN_STATUS"] = [0]*T  # The microgrid is isolated.

    models["Load_ac"]["PD"] = [0]*T
    models["Load_dc"]["PD"] = [0]*T
    models["Load_uac"]["PD"] = [0]*T
    models["Load_udc"]["PD"] = [0]*T

    models["PV"]["PG"] = [0]*T
    models["WP"]["PG"] = [0]*T

    for i in range(T):
        models["DG"]["GEN_STATUS"][i] = dg_info.GEN_STATUS._values[i]
        models["UG"]["GEN_STATUS"][i] = ug_info.GEN_STATUS._values[i]  # The microgrid is isolated.

        models["Load_ac"]["PD"][i] = load_ac_info.PD._values[i]
        models["Load_dc"]["PD"][i] = load_dc_info.PD._values[i]
        models["Load_uac"]["PD"][i] = load_uac_info.PD._values[i]
        models["Load_udc"]["PD"][i] = load_udc_info.PD._values[i]

        models["PV"]["PG"][i] = pv_info.PG._values[i]
        models["WP"]["PG"][i] = wp_info.PG._values[i]

    models["ESS"]["SOC"] = float(ess_info.SOC._values[0])  # The initial energy state in the storage systems.


    return models
