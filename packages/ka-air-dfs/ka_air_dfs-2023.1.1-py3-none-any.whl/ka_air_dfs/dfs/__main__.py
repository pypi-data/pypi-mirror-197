import sys
import warnings

from ka_air_dfs.dfs.parms import Parms
from ka_air_dfs.dfs.do import Do

warnings.filterwarnings("ignore")


def main(*args, **kwargs):
    """
    Load portable Variable into airflow database
    """
    Do.do(sys.argv, sh_parms=Parms.sh)


if __name__ == "__main__":
    main()
