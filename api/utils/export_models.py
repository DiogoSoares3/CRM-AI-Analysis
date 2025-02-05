import cloudpickle
import os
from lifetimes import BetaGeoFitter, GammaGammaFitter
from dotenv import load_dotenv

load_dotenv()
PROJECT_PATH = os.getenv("PROJECT_PATH")


def export_beta_geo_fitter(bgf: BetaGeoFitter) -> None:
    """
    Exports the BetaGeoFitter object to a pickle file.

    Args:
        bgf (BetaGeoFitter): The BetaGeoFitter object to be exported

    Returns:
        None
    """
    with open(f"{PROJECT_PATH}/models/beta_geo_fitter.pkl", "wb") as file:
        cloudpickle.dump(bgf, file)


def export_gamma_gamma_fitter(ggf: GammaGammaFitter) -> None:
    """
    Exports the GammaGammaFitter object to a pickle file.

    Args:
        ggf (GammaGammaFitter): The GammaGammaFitter object to be exported.

    Returns:
        None
    """
    with open(f"{PROJECT_PATH}/models/gamma_gamma_fitter.pkl", "wb") as file:
        cloudpickle.dump(ggf, file)
