"""
This script calculate mass_fraction of species from a Phi
"""

__all__ = ["yk_from_phi", "phi_from_far"]


def phi_from_far(far:float, c_x:float, h_y:float)-> float:
    """
    *Return phi coefficient with the fuel air ratio coeff + fuel composition*

    :param far: the air-fuel ratio
    :type far: float
    :param c_x: stoechio coeff of Carbone
    :type c_x: float
    :param h_y: stoechio coeff of hydrogene
    :type h_y: float

    :returns:
        - **phi** - Equivalence ratio
    """
    mass_molar = {"C": 0.0120107, "H": 0.00100797, "O2": 0.0319988, "N2": 0.0280134}
    mass_mol_fuel = c_x * mass_molar["C"] + h_y * mass_molar["H"]
    coeff_o2 = c_x + (h_y / 4)
    y_o2_fuel_sto = (coeff_o2 * mass_molar["O2"]) / mass_mol_fuel
    phi = far / y_o2_fuel_sto

    return phi


# use "fuel" here as default. Beware it important for pyavbp.
def yk_from_phi(phi:float, c_x:float, h_y:float, fuel_name:str="fuel")-> float:
    """
    *Return the species mass fractions in a fresh fuel-air mixture*

    :param phi: equivalence ratio
    :type phi: float
    :param c_x: stoechio coeff of Carbone
    :type c_x: float
    :param h_y: stoechio coeff of hydrogene
    :type h_y: float
    :param fuel_name: Name of the fuel
    :type fuel_name: str

    :returns:
        - **y_k** - A dict of mass fractions

    """
    y_k = dict()
    mass_molar = {"C": 0.0120107, "H": 0.00100797, "O2": 0.0319988, "N2": 0.0280134}

    mass_mol_fuel = c_x * mass_molar["C"] + h_y * mass_molar["H"]
    coeff_o2 = c_x + (h_y / 4)
    y_o2_fuel_sto = (coeff_o2 * mass_molar["O2"]) / mass_mol_fuel

    if phi == 0.0:
        y_k[fuel_name] = 0.0
    else:
        y_k[fuel_name] = 1.0 / (
            1.0
            + (1.0 + 3.76 * (mass_molar["N2"] / mass_molar["O2"]))
            * (y_o2_fuel_sto / phi)
        )
    y_air = 1 - y_k[fuel_name]
    y_k["N2"] = y_air / 1.303794
    y_k["O2"] = 0.303794 * y_k["N2"]

    return y_k
