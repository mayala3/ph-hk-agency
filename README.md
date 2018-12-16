## Mapping the HK-PH Domestic Worker Industry
Stanford CS 224W
Miguel Ayala

### This Project
Foreign Domestic Workers make up 5% of Hong Kong's population. Unfortunately, many of these workers are subject to terrible working conditions, emotional or physical abuse and civil disenfranchisement. The third is particularly alarming because the employment agencies that source and place these women are often the cause. 

This study explores the interconnected web of Hong Kong (HK) and Philippine (PH) employment agencies that are responsible for bringing Filipinos to work as domestic workers in HK. The study looks at how central certain agencies are and how closely interlinked the entire industry is.

### This Repo
This repo contains the bulk of the pre-processing and processing for the project. The code uses python graph analysis libraries (snap and networkx) to encode and then explore the intricacies of the PH, HK and combined domestic worker
networks. The data used was pulled from an mongo database consisting of data scraped from the PH and HK employment portals.

In the repo are the various intermediary files used to perform created in the process. Also contained here are 
some of the final images of these networks produced by visualization techniques.

The project was developed modularly so that the scraping code and visualization code are contained in
separate repositories. Scraping was done with BS4 and Selenium. Visualization was done with react-graph-viz.js.

### Project Report
The full project report is available [here](http://web.stanford.edu/class/cs224w/reports/CS224W-2018-6.pdf)

