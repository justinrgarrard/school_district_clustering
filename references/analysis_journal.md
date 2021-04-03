# Analysis Journal



### Purpose 

We began with a large dataset containing school district metrics. Our goal was three-part:

1. Find underlying patterns to categorize school districts by (for example, "Small Rural School District").

2. Determine if those patterns say something about academic performance in these school districts.

3. Visualize these attributes using an interactive choropleth (geographic map graph).

We decided to use the CRISP-DM framework to structure our inquiry.



### Dataset Processing 

The full magnitude of available data was far too great to do meaningful work with. Our first task was to reduce it to a managable set of indicators.

The Cookie Cutter Data Science Template offered a handy structure for building out a pipeline. Raw data pulled from an API was aggregated, then filtered. The resulting product was still excessively big:

* ~585,000 Records w/ 51 Indicators

* A Range of Years from 1986 to 2018

We moved to perform a second filtering, this time with the intent to find indicators that were sufficiently present and representative of some interesting quality. Twelve indicators met these requirements:

* leaid (District ID)
* year (Year of Survey)
* lea_name (District Name)
* fips (District U.S. State Code)
* number_of_schools (Number of Schools in District)
* total_teachers_fte (Total Teachers Full-Time-Employed)
* spec_ed_students (Number of Special Education Students in District)
* enrollment (Number of Students in District)
* read_test_pct_prof_midpt (Percent of Reading Tests at the Midpoint)
* math_test_pct_prof_midpt (Percent of Math Tests at the Midpoint)
* rev_total (Revenue Total)
* exp_total (Expenditure Total)



### Exploration 

Targeted dataset in hand, we began exploring our indicators, looking for patterns that would help us in categorizing districts.

One of the earliest findings was the criticality of school district size. Many metrics naturally correlate with the number of schools and students within a district (revenue, expenditure, etc.) It became apparent that any method of categorization was going to have to account for this. Log transformations proved useful for offsetting some of this effect, though "number_of_schools" did not benefit as much from the change.

Another interesting pattern was the strong relationship between reading and math proficiency at a school (R^2 ~ 0.866). We can take this to imply that districts which do well in one subject are likely to do well in the other.



### Modeling

***School District Patterns***

We tried a few different modeling techniques to derive some form of meaningful and easily interpreted categories.

First was **KMeans clustering**, which, even with normalized features, primarily captured size metrics (number of schools and enrollment). Some clusters were significantly larger than others, reflecting the fact that the distribution of schools per district is very uneven (75% 1-5 : 25% 6-1000). One stop-gap measure was to run a second clustering on the largest category. This method showed some promise, but ultimately not enough to warrant pursuing for the final model.

Our second attempt was a **decision tree** based off of test results. The reasoning being that a decision tree would naturally perform splits on the most prominent features in an explainable fashion. As with the clustering, there was a problem of uneven categories. Some leaf nodes consisted of >6,500 records, while others held merely 2.

Next we tried **hierarchical clustering**. The dendrogram visuals produced were particularly interesting. They showed the merging of similar clusters, which could possibly be leveraged to find roughly equivalent cluster sizes. However, the API didn't seem to have much leeway in traversing the dendrogram, instead only allowing access to the leaf nodes.

Finally, we elected to do a **manual stepwise partitioning** by schools per district followed by a **KMeans Clustering**. Each category would contain a roughly equal number of records, and could then be sub-categorized to emphasize patterns among similar districts.

*Manually Decided Categories*

|                       | Single | Small | Mid   | Large |
| --------------------- | ------ | ----- | ----- | ----- |
| District School Count | 1      | 2-3   | 4-10  | 11+   |
| # of Districts (2016) | ~4000  | ~5000 | ~5000 | ~2000 |


*Sub-Categories for "Single"*

|                       | A         | B       | C         | D       |
| --------------------- | --------- | ------- | --------- | ------- |
| Enrollment 25%-75%    | 1057-1486 | 236-598 | 2437-4018 | 389-761 |
| # of Districts (2016) | ~1300     | ~2094   | ~54       | ~1564   |

