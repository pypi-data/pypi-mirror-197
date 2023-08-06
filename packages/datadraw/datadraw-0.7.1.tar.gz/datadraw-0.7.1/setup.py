
from distutils.core import setup

setup( 
    name = 'datadraw',
    version = '0.7.1',
    author = 'Stephen Grubb',
    author_email = 'stevegrubb@gmail.com',
    packages = ['datadraw'],
    url = 'http://datadraw.org/',
    license = 'MIT License',
    description = 'Library to produce many kinds of automated, presentable, data-driven 2-D plots, charts, graphs in SVG',

    keywords = [ 'plot', 'plotting', 'chart', 'charing', 'graph', 'graphing', 'dynamic', 'web', '2-D', 'SVG', 
                 'axis', 'legend', 'python', 'flask', 'django', 
                 'categorical', 'dates', 'times', 'datetime', 'log', 'log10', 'automatic ranging',
                 'automatic axis', 'tooltip', 'image annotation', 'vector graphics', 
                 'bar graph', 'scatterplot', 'boxplot', 'beeswarm plot', 'violin plot', 'pie chart', 
                 'Tukey box whisker plot', 'percentiles', 'outlier', 'line plot', 'heatmap', 'tooltip', 
                 'distribution', 'histogram', 'Kaplan-Meier', 'survival plot', 
                 'chromosomes', 'business day', 'trading day', 'secchi', 'windbarb', 'crispr',
                 'bioinformatics', 'biostatistics', 'biometrics'  ],

    long_description = """ DataDraw is a python function library class to produce many kinds of automated, 
presentable, data-driven 2-D plots / charts / graphics / image annotations in SVG.
It's an all-python server-side solution, producing SVG results that can be
embedded directly into html web pages or saved as .svg image files.  
No javascript, css, or svg knowledge is required.

Axis and legend rendering, tooltips, linkouts, automatic ranging, basic statistics, 
draw primitives.  Handles numeric, log, categorical, and datetime data types.
Leverages SVG's fonts, colors, transparency, image handling, and other aspects.
Works well within frameworks such as Flask or Django.  
Limited interactivity / reactivity use-cases.

Tested on linux python 3.6 and 3.9 using recent browser versions; believed to be thread-safe.

 """,

    long_description_content_type = 'text/plain',

    classifiers = [ 'Development Status :: 4 - Beta', 
'Environment :: Web Environment', 
'Intended Audience :: Developers', 
'Intended Audience :: Education',
'Intended Audience :: Financial and Insurance Industry',
'Intended Audience :: Healthcare Industry',
'Intended Audience :: Information Technology',
'Intended Audience :: Manufacturing',
'Intended Audience :: Other Audience',
'Intended Audience :: Science/Research',
'Intended Audience :: System Administrators',
'Intended Audience :: Telecommunications Industry',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3.6',
'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
'Topic :: Multimedia :: Graphics',
'Topic :: Multimedia :: Graphics :: Presentation',
'Topic :: Scientific/Engineering :: Visualization',
'Topic :: Scientific/Engineering :: Information Analysis',
'Topic :: Scientific/Engineering :: Medical Science Apps.',
'Topic :: Software Development :: Libraries :: Python Modules',
'Topic :: Utilities' ],

  )


