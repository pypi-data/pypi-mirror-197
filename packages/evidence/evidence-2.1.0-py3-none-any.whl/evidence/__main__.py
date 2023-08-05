import sys
import argparse

from evidence.Controller import Controller
from evidence.phase.PrepareEvidence import PrepareEvidence
from evidence.phase.MergeEvidence import MergeEvidence
from evidence.phase.CharacterizeEvidence import CharacterizeEvidence

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str, required=True, help="Path to idifference output dir")
    parser.add_argument("--output", "-o", type=str, default="output", help="Path to result dir")
    parser.add_argument("--occurence", "-c", type=int, default=2, help="The number of occurences in *.me to be used in ce processing")
    args = parser.parse_args()

    ctrl = Controller(args.output)
    ctrl.printHeader()
    ctrl.printScaffolding()
    ctrl.scaffold()
    

    ctrl.printPhase("--> Prepare Evidence")
    pe = PrepareEvidence()
    pe.process(args.path, ctrl.pathPE)

    ctrl.printPhase("--> Merge Evidence")
    me = MergeEvidence()
    me.process(ctrl.pathPE, ctrl.pathME)

    ctrl.printPhase("--> Characterize Evidence")
    ce = CharacterizeEvidence(args.occurence)
    ce.process(ctrl.pathME, ctrl.pathCE)

    ctrl.printExecutionTime()


if __name__ == "__main__":
    sys.exit(main())
