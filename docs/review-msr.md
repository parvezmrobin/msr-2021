# MSR Reviews

Review | Comment | Possible Remedy
--- | --- | ---
A, C | Two bugs being subsequent doesn't mean they are related. | Either (a) manually investigate all sequences to identify chains that are really related or (b) consider their context (TBD) to find out changes that are correlated.
A | Finding that "Most of the subsequent changes are replacements" is nothing special. It just reflects the distribution of the original dataset | For each bug type `T`, find out the ratio of the total occurrence of `T` vs the occurrence of `T` in subsequent commits.
B | Clearer RQs. Specially the word 'context'. |
B | Clearer evidence to prove that stated bug-types really responsible subsequent commits. |
B | Merge Fig 1 & 2 | N/A
B | Replace KDE with a log-scaled bar-chart. | N/A
