from collections import namedtuple
from typing import NamedTuple


# The following does not work, hence why types.NamedTuple was created...
# Employee = namedtuple('Employee', ['name' : str, 'id' : int])

class ReferenceGenome(NamedTuple):
    """ Class representing the sequence of the reference genome. """
    sequence: str
    name: str = None

    def get_sub_sequence(self, start: int, stop: int) -> str:
        if not start >= 0:
            raise ValueError(f"Start ({start}) must be >= 0.")
        if not start <= stop:
            raise ValueError(f"Start ({start}) must be <= stop ({stop}).")
        if not stop <= len(self.sequence):
            raise ValueError(
                f"Stop({stop}) must be <= the length of the reference sequence: "
                f"{len(self.sequence)}."
            )
        return self.sequence[start: stop]


class Allele(NamedTuple):
    """ Class representing an allele.

    Start and stop are 0-indexed stop-exclusive.
    E.g. start=1, stop=2 refers to the base pair(s) at
         the second position of the genome.

    Attributes:
        start: Integer - start position of this allele, with respect to the reference genome.
        stop: Integer - stop position of this allele, with respect to the reference genome.
        sequence: String - genomic sequence of this allele
    """
    start: int
    stop: int
    sequence: str
    reference_genome: ReferenceGenome

    '''
    Alleles must have non-zero length. Specifically:
    * len(sequence) >= 1
    * stop > start

    Note that the coordinates of `Allele.start` and `Allele.stop` are indexes within a `ReferenceGenome`. 
    For insertions and deletions, this means that the length of  `Allele.sequence` is not necessarily
    equal to `Allele.stop - Allele.start`.

    Examples:
        reference sequence: 012  34
                            ACT  CG
        Mutate 1st T -> A:  --A  --  Allele(2, 3, "A")
        Delete 1st T:       -Cx  --  Allele(1, 3, "C")
        Insert after 1st T: --TAG--  Allele(2, 3, "TAG")
    '''
    def in_reference(self) -> bool:
        ref_sub_sequence = self.reference_genome.get_sub_sequence(self.start, self.stop)
        return self.sequence == ref_sub_sequence


rg = ReferenceGenome("CAATCG", 'wild fuzzy amoeba')
example_allele = Allele(2, 5, "ATC", rg)

result = ' ' if example_allele.in_reference() else ' NOT '

print(f"\nAllele {example_allele.sequence} is{result}consistent with reference genome for '{rg.name}'")
