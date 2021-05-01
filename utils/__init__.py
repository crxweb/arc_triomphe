"""
module gérant les fonctionnalités courantes
"""

from .utils_date import (
    next_weekday,
    arctriomphe_date,
)

from .utils_scraping import (
    generate_url_targets,
)

from .utils_dataFrame import (
    setTempSecondePalmares,
    getChevauxDepart,
)

from .utils_francegalop import (
    getHeader,
    searchChevalByName,
    getChevalPerformance,
    getChevalCarriere,
    getChevalEngagement,
    getArcTriompheHistorique,
    getChevalDetail,
)
