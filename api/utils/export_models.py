import cloudpickle
import os
from lifetimes import BetaGeoFitter, GammaGammaFitter
from dotenv import load_dotenv

load_dotenv()
PROJECT_PATH = os.getenv("PROJECT_PATH")


def export_beta_geo_fitter(bgf: BetaGeoFitter):
    with open(f"{PROJECT_PATH}/models/beta_geo_fitter.pkl", "wb") as file:
        cloudpickle.dump(bgf, file)


def export_gamma_gamma_fitter(ggf: GammaGammaFitter):
    with open(f"{PROJECT_PATH}/models/gamma_gamma_fitter.pkl", "wb") as file:
        cloudpickle.dump(ggf, file)
