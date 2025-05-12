import numpy as np

from CLI.lib.property.coolprop import get_rho, get_mu


def get_blockmesh_xmin(length, divisions, bias):

    exponent = 1/(divisions-1)
    r = bias**exponent
    start_width = length * ((1-r)/(1-(r**divisions)))
    end_width = start_width * (r**(divisions-1))

    return [start_width, end_width]


def get_yplus(R, Nr, bf, fluid, P0, T0, G):

    # delx from blockmesh_xmin function
    delx = min(get_blockmesh_xmin(R, Nr, bf))
    # print(delx)

    rho = get_rho(fluid, P0, T0)
    mu = get_mu(fluid, P0, T0)
    nu = mu/rho
    U = G/rho

    # Reynolds Number
    Re = (2*U*R)/nu
    # Skin friction coefficient
    cf = (2*np.log10(Re) - 0.65)**(-2.3)
    # Wall shear stress
    tw = cf*0.5*rho*(U**2)
    # u star
    ustar = np.sqrt(tw/rho)
    yplus = (ustar*delx)/nu


    return yplus


def get_2D_mesh_parameters(mesh_info_dict, case_info_dict):

    del_r_min = min(get_blockmesh_xmin(mesh_info_dict['R'], 
                                   mesh_info_dict['Nr'], 
                                   mesh_info_dict['bf']))
    
    del_x_min = 1000/mesh_info_dict['Na']


    if "L0" in mesh_info_dict.keys():
        tot_length = mesh_info_dict['Lh'] + (2*mesh_info_dict['R']*(mesh_info_dict['L0'] + mesh_info_dict['L1']))
    else:
        tot_length = mesh_info_dict['Lh'] + (2*mesh_info_dict['R'] * mesh_info_dict['L1'])

    n_cells: int = (tot_length*1e3 / del_x_min) * mesh_info_dict['Nr']

    yplus_estimated = get_yplus(mesh_info_dict['R'],
                                mesh_info_dict['Nr'],
                                mesh_info_dict['bf'],
                                case_info_dict['fluid'],
                                case_info_dict['p'],
                                case_info_dict['T'],
                                case_info_dict['G'])
    

    return [del_r_min, del_x_min, n_cells, yplus_estimated]



def get_3D_mesh_parameters(mesh_info_dict, case_info_dict):

    # del_r_min = get_blockmesh_xmin(mesh_info_dict['R'], 
    #                                mesh_info_dict['Nr'], 
    #                                mesh_info_dict['bf'])
    
    # del_x_min = 1000/mesh_info_dict['Na']


    # if "L0" in mesh_info_dict.keys():
    #     tot_length = mesh_info_dict['Lh'] + (2*mesh_info_dict['R']*(mesh_info_dict['L0'] + mesh_info_dict['L1']))
    # else:
    #     tot_length = mesh_info_dict['Lh'] + (2*mesh_info_dict['R'] * mesh_info_dict['L1'])

    # n_cells: int = (tot_length*1e3 / del_x_min) * mesh_info_dict['Nr']

    # yplus_estimated = get_yplus(mesh_info_dict['R'],
    #                             mesh_info_dict['Nr'],
    #                             mesh_info_dict['bf'],
    #                             case_info_dict['fluid'],
    #                             case_info_dict['p'],
    #                             case_info_dict['T'],
    #                             case_info_dict['G'])

    return [0, 1, 2, 3, 4]

    # return [del_r_min, del_x_min, del_c_min, n_cells, yplus_estimated]
