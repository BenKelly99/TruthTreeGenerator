#TruthTreeGenerator
## What is TruthTreeGenerator
TruthTreeGenerator is a python program that given a set of options returns a TruthTree problem that can be opened in willow.
## How to use:
TruthTreeGenerator is easy to use it takes at most 3 easy steps:
- **Step 1:** run `python options_generator.py <file_name.json>` to create a blank options file (optional)
- **Step 2:** fill your options file with the specifications you would like out of the premises (see Options File Info for more details)
- **Step 3:** run `python generator.py <file_name.json> <file_name.willow>` to create the random premises based off your options file
From there you can open the created file in [Willow](https://willow.bramhub.com/).
## Options File Info
The options file has 13 different fields:
```
{
    "atomics": "",                // Number of literals
    "consistent": "",             // Boolean of whether it should be consistent  
    "num_premises": "",           // Number of premises at the end including conclusion
    "max_decomps_in_premise": "", // Max decomposition of a single premise
    "min_logic_depth": "",        // Minimum number of branches
    "min_and_decomps": "",        // Minimum and decompositions
    "min_or_decomps": "",         // Minimum or decompositions
    "min_cond_decomps": "",       // Minimum conditional decompositions
    "min_bicond_decomps": "",     // Minimum biconditional decompositions
    "min_neg_and_decomps": "",    // Minimum negated and decompositions
    "min_neg_or_decomps": "",     // Minimum negated or decompositions
    "min_neg_cond_decomps": "",   // Minimum negated conditional decompositions
    "min_neg_bicond_decomps": ""  // Minimum negated biconditional decompositions
}
```
## Possible future additions
- adding a GUI
## Authors
Ben Kelly
Jenay Barela
## License
[MIT](https://choosealicense.com/licenses/mit/)
