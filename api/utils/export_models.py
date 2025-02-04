import cloudpickle
import os
from lifetimes import BetaGeoFitter, GammaGammaFitter
from dotenv import load_dotenv

load_dotenv()
PROJECT_PATH = os.getenv("PROJECT_PATH")


def export_beta_geo_fitter(bgf: BetaGeoFitter) -> None:
    """
    Exporta o objeto BetaGeoFitter para um arquivo pickle.

    Parameters
    ----------
    bgf : BetaGeoFitter
        O objeto BetaGeoFitter a ser exportado.

    Returns
    -------
    None
    """
    with open(f"{PROJECT_PATH}/models/beta_geo_fitter.pkl", "wb") as file:
        cloudpickle.dump(bgf, file)


def export_gamma_gamma_fitter(ggf: GammaGammaFitter) -> None:
    """
    Exporta o objeto GammaGammaFitter para um arquivo pickle.

    Parameters
    ----------
    ggf : GammaGammaFitter
        O objeto GammaGammaFitter a ser exportado.

    Returns
    -------
    None
    """
    with open(f"{PROJECT_PATH}/models/gamma_gamma_fitter.pkl", "wb") as file:
        cloudpickle.dump(ggf, file)
