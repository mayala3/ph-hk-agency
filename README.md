Mapping the HK-PH Domestic Worker Industry
Stanford CS 224W
Miguel Ayala

This repo contains the bulk of the pre-processing and processing for the project. The code uses python graph analysis libraries (snap and networkx) to encode and then explore the intricacies of the PH, HK and combined domestic worker
networks. The data used was pulled from an mongo database consisting of data scraped from the PH and HK employment portals.

In the repo are the various intermediary files used to perform created in the process. Also contained here are 
some of the final images of these networks produced by visualization techniques.

The project was developed modularly so that the scraping code and visualization code are contained in
separate repositories. Scraping was done with BS4 and Selenium. Visualization was done with react-graph-viz.js.

