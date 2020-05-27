# CRO55: COVID-19 prompt test

Contains:

- An investigation into the audiences that could get different prompt treatments.
- A script to run the alpha-spending function approach for test monitoring for t-tests.
- Two different MDE approaches for t-tests (ttest_MDE based on iterating the mean, ttest_MDE_model based on iterating on the gift distribution)

N.B. the previous approach of getting transaction IDs from GA led to too much sampling, and so a workaround has been set up with a daily Google Sheets run. The information quotients are different between the z- and t- scores, as they are therefore drawing from differently-sampled data.

### How to check test progress

1. Get the LBL data from the web reporting database
2. _lbl_munge.py_: change path for the new LBL CSV if needed, run
3. Add new dates into [the less-sampled transaction ID sheet](https://docs.google.com/spreadsheets/d/10M-glXPJoNxjO2fNPybhvqE3AR0FUWh7u2Zsdp-hCtM/edit#gid=395427764)
4. _FetchData.py__: run, with GA access token
5. _lbl_ga_join.py_: change end date, run
6. _DoSeqAnalysis.py_ for the conversion % check
7. _seq_analysis_ttest.py_ for the average gift check

### t-test alpha spending function

One approach is to calculate a z-score directly from the data (cf. [1]).

However, it felt more robust to use the better-documented approach ([2], [3]) of transforming z-statistics to p-values to t-statistics, and use the same boundaries as with the agreed z-statistic approach:

> The methodology underlying all boundary calculations is based on Z-boundary calculations. Following the recommendation of Jennison and Turnbull (2000), p. 80, Z-scale boundaries are first produced, using the common methods. The corresponding p-value boundaries are computed from the Z-value boundaries. These p-value boundaries are then converted to t-value boundaries, using the appropriate degrees of freedom. As discussed in Jennison and Turnbull (2000), these t-value boundaries have been found to be ‘remarkably accurate.’
[2]

The t-statistic formula is on p9 of [2]. The classic df calculation is used, rather than the Welch–Satterthwaite equation, for simplicity (given how insensitive the boundary is to higher numbers).

![t_k = \frac{\bar{x}_{1k}-\bar{x}_{2k}}{\sqrt{\frac{s^2_{1k}}{n_{1k}}+\frac{s^2_{2k}}{n_{2k}}}}](https://render.githubusercontent.com/render/math?math=t_k%20%3D%20%5Cfrac%7B%5Cbar%7Bx%7D_%7B1k%7D-%5Cbar%7Bx%7D_%7B2k%7D%7D%7B%5Csqrt%7B%5Cfrac%7Bs%5E2_%7B1k%7D%7D%7Bn_%7B1k%7D%7D%2B%5Cfrac%7Bs%5E2_%7B2k%7D%7D%7Bn_%7B2k%7D%7D%7D%7D)

Rather than using the group sequential design information quotient from [2],  an alpha-spending approach is taken [to allow unknown checks](https://online.stat.psu.edu/stat509/node/81/) and [avoid needless complexity](https://www.jstor.org/stable/2673566?seq=1#metadata_info_tab_contents) cf. [4]:

![I_k = n_k/n_K](https://render.githubusercontent.com/render/math?math=I_k%20%3D%20n_k%2Fn_K)

### References

1. [Defazio, 2016](https://www.aarondefazio.com/adefazio-seqtesting.pdf)
2. [NCSS Statistical Software manual, Group-Sequential T-Tests for Two Means](https://ncss-wpengine.netdna-ssl.com/wp-content/themes/ncss/pdf/Procedures/NCSS/Group-Sequential_T-Tests_for_Two_Means.pdf)
3. [Koopmeiners, Sequential Analysis](http://www.biostat.umn.edu/~josephk/courses/pubh8482_fall2012/lecture_notes/pubh8482_week6.pdf)
4. Wassmer, G. (2014). Group Sequential Designs. In Wiley StatsRef: Statistics Reference Online (eds N. Balakrishnan, T. Colton, B. Everitt, W. Piegorsch, F. Ruggeri and J.L. Teugels). doi:10.1002/9781118445112.stat06804

Inline LaTeX made using [this tool](https://alexanderrodin.com/github-latex-markdown/)
