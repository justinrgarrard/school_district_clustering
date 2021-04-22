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

From these, a second set of features was created.

* students_per_school (enrollment / number_of_schools)
* students_per_teacher (enrollment / teachers_total_fte)
* spending_per_student (exp_total / enrollment)
* academic_performance ((read_test_pct_prof_midpt + math_test_pct_prof_midpt) / 2)
* special_ed_students_percent (enrollment / spec_ed_students)



### Exploration 

Targeted dataset in hand, we began exploring our indicators, looking for patterns that would help us in categorizing districts.

One of the earliest findings was the criticality of school district size. Many metrics naturally correlate with the number of schools and students within a district (revenue, expenditure, etc.) It became apparent that any method of categorization was going to have to account for this. Log transformations proved useful for offsetting some of this effect, though there was no discernable relationship between academic performance and the other indicators.

Another finding was the strong relationship between reading and math proficiency at a school (R^2 ~ 0.866 for 2016). We can take this to imply that districts which do well in one subject are likely to do well in the other.



### Modeling

***School District Patterns***

We tried a few different modeling techniques to derive some form of meaningful and easily interpreted categories.

First was **KMeans clustering**, which, even with normalized features, primarily captured size metrics (number of schools and enrollment). Some clusters were significantly larger than others, reflecting the fact that the distribution of schools per district is very uneven (75% 1-5 : 25% 6-1000). One stop-gap measure was to run a second clustering on the largest category. This method showed some promise, but ultimately not enough to warrant pursuing for the final model.

Our second attempt was a **decision tree** based off of test results. The reasoning being that a decision tree would naturally perform splits on the most prominent features in an explainable fashion. As with the clustering, there was a problem of uneven categories. Some leaf nodes consisted of >6,500 records, while others held merely 2.

Next we tried **hierarchical clustering**. The dendrogram visuals produced were particularly interesting. They showed the merging of similar clusters, which could possibly be leveraged to find roughly equivalent cluster sizes. However, the API didn't seem to offer much leeway in traversing the dendrogram, instead only allowing access to the leaf nodes.

Following that, we elected to do a **manual stepwise partitioning** by schools per district followed by a **KMeans Clustering**. Each category would contain a roughly equal number of records, and could then be sub-categorized to emphasize patterns among similar districts.

*Manually Determined Categories*

|                       | Single | Small | Mid   | Large |
| --------------------- | ------ | ----- | ----- | ----- |
| District School Count | 1      | 2-3   | 4-10  | 11+   |
| # of Districts (2016) | ~4000  | ~5000 | ~5000 | ~2000 |


*Sub-Categories for "Single"*

|                       | A         | B       | C         | D       |
| --------------------- | --------- | ------- | --------- | ------- |
| Enrollment 25%-75%    | 1057-1486 | 236-598 | 2437-4018 | 389-761 |
| # of Districts (2016) | ~1300     | ~2094   | ~54       | ~1564   |


There were two major draws for this approach that resulted in it being chosen as the final modeling technique:

1. **[Tuning Sub-Categories]:** The quanitity of sub-categories can be adjusted as needed. For example, we could produce five clusters for "Single School" districts, and two clusters for "Large"  districts. This was a useful tool given our objective of making meaningful and interpretable categories, though it was ultimately not leveraged.

2. **[Applicability to Entire Dataset]:** Clustering isn't much affected by using the entire dataset (2009-2016) as opposed to a single year (2016). This makes it relatively easy to deploy the prototype model into a full-fledged model.


***Relations to Academic Performance***

Given that our original goals included understanding school districts in the context of their academic performance, we spent some time attempting to tease out any latent relationships. 

Regressions were performed at several levels. Firstly, across a single year with the basic features. Second, across each category and sub-category. And third, across the entire labeled dataset. Much to our dismay there were no visible patterns. Even attempting various log transforms had little impact. This suggests that our indicators are not relevant to performance (at the school district level). It does not, however, prove the *absence* of any relationships, only that our analysis was of insufficient detail or scope.

While the regressions did not bear much fruit, the clustering algorithm did pick up on academic performance among similarly sized districts. Each of the four categories had two sub-categories; trending high performance and trending low performance. This was well-demonstrated by a box plot. 

![Visual of Box Plots](academic_performance_boxplot.png)


### Evaluation

The penultimate step in CRISP-DM is to evaluate results. Our outputs were more qualitative than quantitative. As such, the methods of evaluation were likewise qualitative. Surveys were sent out to family and friends of the team with the intent of soliciting feedback on label names and their descriptions. This information would later be incorporated into the interactive choropleth.



### Deployment

The final step for this project is deployment. Intrepreted in this case to be the submission of the project.



### Conclusions

We began with three objectives:

1. Find underlying patterns to categorize school districts by (for example, "Small Rural School District").

2. Determine if those patterns say something about academic performance in these school districts.

3. Visualize these attributes using an interactive choropleth (geographic map graph).


The first was satisfied by the manual partiton / KMeans model. Our major underlying pattern was found to be size (school district enrollment and number of schools). 

The second was found to be negative. While the various categories do exhibit some variation in academic performance, none of the indicators we have chosen appear to explain this behavior.

The third objective was executed using the labeled dataset and D3. 

Overall, we have achieved our objectives, though the results are not as interesting as we had hoped.


***Reflections***

If we were to continue refining this project, I would suggest the following:

* **[Systematic Feature Selection]:** To use a technique such as LASSO or Elastic Net to determine the features used, as opposed to the analysts' intuition.

* **[Alternative Modeling Technique]:** While the manually partitioned KMeans approach did function for our purposes, there are likely others that would've been a better fit.

* **[Extended Literature Review]:** The body of research on education metrics is extensive. Even with the numerous sources perused at the start of the project, we are still under-equipped to produce work that advances the field.