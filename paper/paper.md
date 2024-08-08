---
title: 'AstroGlue: An exploratory clustering analysis tool for astrophyiscal data sets'

tags:
  - Python
  - AstroLink
  - Glueviz
  - Astrophysics
  - Clustering
  - Data Visualization

authors:
  - name: Kamalesh Sampath
    orcid: 0009-0009-0055-3215
    affiliation: "1"
  - name: William H. Oliver
    orcid: 0009-0008-1180-537X
    affiliation: "2, 3"
  - name: Tobias Buck
    orcid: 0000-0003-2027-399X
    affiliation: "2, 3"

affiliations:
 - name: National Institute of Technology, Department of Instrumentation and Control Engineering, Tiruchirappalli - 620015, Tamil Nadu, India
   index: 1
 - name: Universit&auml;t Heidelberg, Interdisziplin&auml;res Zentrum f&uuml;r Wissenschaftliches Rechnen, Im Neuenheimer Feld 205, D-69120 Heidelberg, Germany
   index: 2
 - name: Universit&auml;t Heidelberg, Zentrum f&uuml;r Astronomie, Institut f&uuml;r Theoretische Astrophysik, Albert-&Uuml;berle-Stra&szlig;e 2, D-69120 Heidelberg, Germany
   index: 3
date: 01 August 2024
bibliography: paper.bib
---

# Summary
`AstroGlue` serves as a bridge between the `AstroLink` [@Oliver2024] clustering algorithm and the `Glue` [@robitaille_2019_3385920] visualization tool. `AstroLink` is a versatile clustering algorithm designed to extract meaningful hierarchical structures from astrophysical datasets. The clustering structure found by the `AstroLink` can be visualized via the 2-dimensional ordered-density plot that it produces. `Glue` can be used to explore relationships within and among related datasets. Its features include - linked statistical graphics, flexible linking across data and full scripting capability with Python. `AstroGlue` combines these functionalities giving the user the ability to interactively explore the astrophysical clustering structure of the input data. AstroGlue also provides a GUI frontend that allows the user to import a dataset, choose the plots to be displayed and optionally run the `AstroLink` clustering algorithm on any subset of the feature space as the user wishes to. Following the AstroGlue GUI window, a `Glue` session will be automatically launched with all chosen plots in addition to the ordered-density plots produced by instances of the `AstroLink` clustering algorithm, allowing interactive visualization and analysis of the clusters.

# Statement of need
Astronomers tend to identify structures in observational data sets using one of two methods - a standard clustering algorithm [@ElAziz2016;@Malhan2018b;@Malhan2018c;@Hasselquist2019;@CastroGinard2019;@PriceJones2019;@Kounkel2019;@Hunt2021;@Ibata2021;@Malhan2022;@Pearson2022;@Swiggum2024] or visual inspection [@Arifyanto2006;@Duffau2006;@Williams2011;@Helmi2017;@Helmi2018;@Belokurov2018]. However, standard clustering algorithms often lack astrophysical robustness, while structures detected via visual inspection require verification using additional techniques. `AstroGlue` addresses the limitations associated with both of the aforementioned methods by combining the statistically and astrophysically robust clustering algorithm, `AstroLink` with the multi-dimensional linked-data exploration tool, `Glue`.

The interactive and easy-to-use GUI of `AstroGlue` eliminates the need for any additional coding, thereby making the process of identifying and visualizing clusters much more efficient and accurate than existing methods. Users have the option to either work with the GUI provided or programmatically with the `AstroGlue` class methods. `AstroGlue` facilitates the easy import of astrophysical data sets and provides various customization options, enabling users to streamline their analysis. At the time of writing, the authors are not aware of any existing implementations that offer these interactive capabilities and usability options. 

![`AstroGlue` GUI with a data set imported, columns labelled, plots chosen, and `AstroLink` feature space set.](AstroGlue_example/1.png) 

![`Glue` session launched with all chosen plots (including the `AstroLink` ordered-density plot) and a few highlighted user-chosen clusters. The lower panel shows the process a user takes to highlight a cluster found by AstroLink."](AstroGlue_example/2.png)

![`Glue` session with all highlighted clusters (following the action shown in Figure 2) and overlayed arrows to mark their correspondance to the ordered-density plot."](AstroGlue_example/3.png)


# Acknowledgements
KS acknowledges financial support from the Working Internships in Science and Engineering (WISE) scholarship provided by the Deutscher Akademischer Austauschdienst (DAAD). WHO and TB acknowledge financial support from the Carl-Zeiss-Stiftung. The authors would also like to thank the Scientific Software Center at the Interdisciplinary Center for Scientific Computing of Heidelberg University for its support and guidance during the development of this package.

# References
