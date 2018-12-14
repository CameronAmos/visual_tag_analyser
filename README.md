# visual_tag_analyser

This is a GUI that can be used to analyze the data inside of specially formated .txt files that contain tag information
about vaious alleles that can be found within a (in this instance, wheat) genome. These tags are snippets of nucleotide sequences
that have the potential to become diagnostic tags if they are found to be within a coding region of a gene which is known to make up
a certain allele. These diagnostic sequences can be used to determine if the allele for the gene that a specific wheat variety has
is a good allele (one that increases the strength or bread quality of the wheat) or a poor allele (one that does the opposite).
Tags from up to two genomes can be compared side-by-side in order to get a grip on how the alleles that are found within these two
genomes are similar or different, which is incredibly useful from a plant breeding perspective.

This text is available in the 'Help' section of the GUI:
It is possible to compare two different tags sets from two different genomes at the same time.
First, Load in a tag file (.txt) using the File -> Import Genome Tags.
Now it is possible to select that genome from the Genome combo boxes.
You may query increased specificity on which tags you would like to show up on the screen by choosing what chromosome, base pair range,
and specific sequence the tags must have.
You may also highlight tags that are similar by sequence between the two genomes by checking the 'Compare Similar Seqs' box.
