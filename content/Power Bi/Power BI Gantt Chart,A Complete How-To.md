## What is a Gantt Chart in Power BI?

A Gantt chart is a bar chart where each project task is represented by a horizontal bar. The start and end of this bar represent the task timeline. It also shows the relationship between bars and prerequisites before starting a particular task. A Gantt chart is made up of the following components:

- Tasks: These are activities regarding a project that team members are expected to complete within a specific timeline.
- Timelines: This is the timeframe assigned to a particular task and can also define the **overall** project timeline. 
- Dependencies: These are the prerequisite tasks to be completed before starting a new one.
- Progress: This is a measure of the time spent on a task.

Now, let’s go into how to create your own Power BI Gantt chart, which should make all these concepts clear. 

## How to Create a Gantt Chart in Power BI

The first step is to make sure you have [installed Power BI Desktop](https://app.datacamp.com/learn/tutorials/tutorial-power-bi-installation). Also, download the [project data](https://github.com/adejumoridwan/datasets/blob/main/project.csv) we will use in this article.

### Importing the Gantt chart custom visual

A Gantt chart is not among Power BI built-in visuals, which means it’s a custom visual that you need to download. You do this by going to the Visualizations pane, on the ellipsis(...), and clicking on Get more visuals.

**Note**: to download custom visuals, you need a Power BI license. If you don’t have one, open a [Microsoft Fabric account](https://learn.microsoft.com/en-us/fabric/get-started/fabric-trial) for a free Power BI license. We also have a blog post, [What is Microsoft Fabric?](https://www.datacamp.com/blog/what-is-microsoft-fabric) If you want to do some research first. 

![Download a Power BI Gantt chart](https://media.datacamp.com/cms/google/ad_4nxflwyhnito3u3euu6ioqh8j_z0ktaerzpz7e_xbvjrwngi5rxjc229qd6spje4bt09mw5fgslwdxqcvjzasiyszpghims0h3oksuvt4p-j13ko11pmab_y39c68d27zts9dweuxefsxnjnv-3kqm9vzd9o.png)

Downloading a Power BI Gantt chart. Image by Author  
  

After the window opens, go to the search bar and type “Gantt” to get a list of various Gantt chart visuals, and select the one by Microsoft Corporation, then click the Add button.

![The Power BI Gantt chart window](https://media.datacamp.com/cms/google/ad_4nxcq4bpbzbdwa-drccrok8wyc5acz7mrzmjoaxbtgwkpxm01wthmiu32xc_4agxinkblq_ubwqfnrfkeixptqc3uxkbzf-pncsdfi0u9bpjiqdyxhc0qacokcgxaasztafdesrkdlkzsxvtd4xu7qcvc58c.png)

_Adding the Gantt chart to Power BI. Image by Author._

###   
  
Setting up your data for a Gantt chart

The next important step to creating the Gantt chart visual is to structure your dataset based on the Gantt chart components discussed earlier. You need to ensure that your dataset has the necessary columns, such as:

- Task name
- Start date
- Duration
- Dependencies

Go to the Get Data icon under the Home tab on Power BI Desktop and click Text/CSV to import the project data. 

![Power BI Gantt chart project dataset overview](https://media.datacamp.com/cms/google/ad_4nxcvgdrjnw2oqymkjwkaotnieultzfyw9n76nk8samgj7cdlped9zsmjx0qjwgyrgbpd_kqnigxdcnfe_7fwitgnzm6wddy6-sfjxijzmarxqg3t3by-scaqyujohic0e6n995cus79uayql_y1xqmib8t2d.png)

Seeing the project dataset preview. Image by Author.

  
If your dataset does not have the necessary chart columns, you can click the Transform Data button to apply the necessary transformations. On the preview window, click Load to load the data into Power BI.

### Creating the Gantt chart

Click on the Gantt chart icon on the Visualizations pane to apply an empty visual to the Power BI canvas. Select the empty visual and drag each field of your dataset to its respective Gantt chart field.

Note that you have to move the Dependencies field to the Power BI Gantt chart visual Resource field. Also, you can’t add Duration and End Date to a Gantt chart visual simultaneously. Instead, you choose **Start** **Date** with either **Duration** or **End** **Date**.

![Power BI Gantt chart visual fields](https://media.datacamp.com/cms/google/ad_4nxci3x8wy5qod4malq6tuonqojd97rthz3beldamsfar7yk6supkksfswkd9hsrpn3xa12o1hlprw_voeqal-xda3yvvfzhwj1qdcvurp7yuhmu71rxblhybljkdxnfnw8yey_r8f3amv0no7w2y0lkfiii.png)

_Power BI Gantt chart visual fields. Image by Author._

## Customizing a Gantt Chart in Power BI

Power BI gives you options to customize your Gantt chart visual, from changing the colors to axis labels and adding milestones to the Gantt chart visual. 

### Changing colors and labels

You can change the colors of the bars to any color of your choice. To do that, select the Power BI Gantt chart visual on the canvas and go to the Format visual tab on the Visualizations pane. Then, select your preferred color under the Task Settings dropdown.

![Changing the task column color in our Power BI Gantt chart](https://media.datacamp.com/cms/1c1fe8533ff1216f420097ea8012ceb9.png)

Changing the task column color in our Power BI Gantt chart. Image by Author.  
  

Below the Task Settings dropdown is the Data Labels dropdown, where you can format the labels of the Gantt chat visual.

![Format the data labels in our Power BI Gantt chart](https://media.datacamp.com/cms/google/ad_4nxfmifaoxhbus3w2n7nxnpn6dm7wahg_fspsatgcu1bmcjpz82pqloh1imprv_qj521h8qjhfyih2lqy-jr7vnywx_uis2k9dozc5_xdq3k64mybxny5bpspb4zxbv9t-beunohvzv_-5jlqasg9vjlzvobq.png)

Formatting the Power BI Gantt chart data labels. Image by Author.  
  

### Adding milestones

Milestones are used to mark significant events during a project lifecycle. You can add milestones in a Power BI Gantt chart visual by dragging any dataset field representing project milestones into the Gantt chart visual.

![Power BI Gantt chart with milestones](https://media.datacamp.com/cms/google/ad_4nxf9ds6muda8ns3zzpnvruo5fow23be9of0rnyyjcncod8au6lcm05a3afxewduoyqcq_rawbggdokthl46in543igymlcgpaawtzzh1jqjzd-kgpktn-vj9cslul5q0oxdeq3oaigbp1jj03mufl9y8zar9.png)Adding milestones to the Power BI Gantt chart. Image by Author.  
  

## Interpreting Gantt Charts in Power BI

Let's now move on to how to interpret a Gantt chart visual so you can make the most out of it in your work.

### Visualizing task progress

A taskbar represents each project task timeline, and a dark color on a taskbar measures a task completion rate. Tasks already completed will have completely dark colors, while those still in progress will have shades of dark and light. 

The x-axis represents the project tasks, while the y-axis is the project timeline. The Power BI tooltip lets you get detailed information about a task by hovering over the taskbar. This provides detailed information about a project task, such as the task name, start date, end date, progress, and the resources needed.

![Power BI Gantt chart and tooltip task progress](https://media.datacamp.com/cms/google/ad_4nxd8woqrkqki9xt-vvuk-esnfvedycy-4aum8hluogjykg5yyevuzzhk9asaeb-bhgrze76caxxebbyivmfk25jrdrtmt8_puz8oxnupgz7wjzprn_orlgrwjqobgx1ww0-jqk8hvukrbdiq5rrv2krbtq0.png)

Use the tooltip to visualize task progress. Image by Author.  
  

### Identifying critical paths and dependencies

**If you have added dependencies to your Gantt chart visual in Power BI, you should see the dependency next to each taskbar. The dependency is what you need to finish before moving on to the next task.**

![Power BI Gantt chart with dependencies included](https://media.datacamp.com/cms/google/ad_4nxews8_hraq3ijqfh4cxn1gturllmzeofhhcaojfnrhqwfoira3karh1v0abiqafdb1mjz4chcxrjj8jebdb-eokg-zwywsdvpb4n3bf344ljfzbeintmbsc-ygxfqfklhb0vbog8pucwuk_r6fp1bqfvf1m.png)

Seeing dependencies on our Power BI Gantt chart. Image by Author.  
  

## Power BI Gantt Chart Troubleshooting

While trying to create a Gantt chart in Power BI, you may face some challenges due to not having the necessary Gantt chart columns or missing values in your dataset, or the Power BI Gantt visual not displaying correctly. 

### Missing data fields

Before importing a dataset into Power BI, you can see a preview and see if the columns in the dataset are the necessary Gantt chart columns. You can click on the Transform button of the Power Query to open the datasets and see if there are any missing values or errors in the column formatting. These issues, if they exist, you can fix directly in the Power Query editor.

### Visual not displaying properly

If you have created a Power BI Gantt Chart visual and you notice that after filling in all the fields, the visual is not displaying, the first thing you need to do is check if you have selected the proper fields from the dataset columns into the Gantt chart visual fields. 

If you notice no problem with the fields, check your date columns and ensure they are in the proper format. Also, check the columns containing numeric values and ensure they are formatted as numbers, not strings. If you are using a dataset from a database, ensure your data model is specified correctly so that it can render. A final action is to reset and rebuild the visual. Starting afresh can help you identify where the problem is.

## Conclusion

In this article, you have learned how to create and customize a Gantt Chart in Power BI and the steps to take when having issues creating one. The **Format** **visual** tab under the visualization pane offers many more customization options, which you can explore to make sure you have a beautiful Gantt chart that effectively explains and tracks your entire project, whatever it is.