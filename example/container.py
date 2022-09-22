import dotenv
from dependency_injector import containers, providers

from example.indicator_services import BancoCentralService, MindicadorService
from example.readjust_calculators import IPCReadjust, UFReadjust

dotenv.load_dotenv()


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=[__package__])

    config = providers.Configuration()

    config.bcentral_user.from_env("BANCO_CENTRAL_USER")
    config.bcentral_pass.from_env("BANCO_CENTRAL_PASS")

    indicator_service = providers.Factory(MindicadorService)

    readjuster_service = providers.Factory(UFReadjust)
