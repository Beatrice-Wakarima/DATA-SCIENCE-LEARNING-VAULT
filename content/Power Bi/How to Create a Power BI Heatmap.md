### What are Data Visualization Heatmaps?

Heatmaps were originally introduced by [Cormac Kinney](https://en.wikipedia.org/wiki/Cormac_Kinney) to graphically represent real-time financial information. They are used in data visualization to measure the intensity of given business values, encoded using different colors. 

The following image is an example of the heatmap, shared by NASA on July 13th, 2022. It shows the surface air temperatures for many countries in the world. The hottest the area is, the darkest the color. Investly, the coldest, the color is more driven towards blue. Such information can be easily understood at a glance.

![NASA heatmap](https://images.datacamp.com/image/upload/v1660727926/NASA_heatmap_79abbd8972.jpg)

Source: [NASA heatwave map](https://uttarakhandnewsnetwork.com/2022/07/nasa-heatwave-map-reveals-alarming-rise-in-temperatures-globally) reveals an alarming rise in temperatures globally

Data Scientists can use them to turn companies' information into easy-to-understand visualizations to help them make actionable smart decisions.

### Why are Heatmaps Useful?

Using heatmaps can provide a significant intuitive level of visual representation of information at different levels. It is one of the most powerful approaches to business intelligence. Also, many businesses are using it for the following reasons:

- #### Have a global overview of customers' behavior
    

When designing a tool, like a website, we have an expectation of the end use. However, the end-users might not have the right understanding of the design concept, which can lead them to have a different interaction with the tool. In such a situation, a heatmap visualization can be used to have a better understanding of the users' behavior by tracking the main pages getting more interest, and the areas (clickable and non-clickable) that are being clicked the most. 

- #### Improve business performance
    

After having a better understanding of the users’ behavior, businesses can design and set up their tools in a way that people can find the right information at the right location. Doing so can lead to generating more traffic and consequently create more business values.

- #### A good alternative for visual analytics
    

Heatmap visualizations can provide an in-depth visual understanding of how users interact with your business website, and can be a good alternative to tools like google analytics which are not always intuitive and might be even sometimes overwhelming. 

- #### A good way for Data Scientists to visualize features' relationship
    

Heatmaps are my go-to approach when performing correlation analysis. Instead of dealing with numerical values in the correlation matrix, heatmaps can be used to get a quick visual representation of the relationship between multiple variables for training your Machine Learning models. 

### Heatmap Examples

Heatmaps provide a wide range of possibilities in different domains because of their ability to generate a simple visual representation of the data. Below are five different types and their applications.

- #### Web heatmaps
    

These types of heatmaps are used by organizations whose activity is internet-driven, such as media services, SaaS companies, eCommerce companies, etc. They use heatmap visualizations to monitor and understand users’ behavior on their platforms, to discover insights for better decision making. Some of the web heatmaps are: 

- **clickmap** showing which parts of a web application have had the most click. 
- **scrollmap** highlights how far users scroll down the web page before further navigation. 
- **eye tracking** is not always obvious due to some level of complexity. The overall goal is to capture where the users pay most attention to. 
- **mouse** tracking is indicated by some research as a substitute for eye tracking.

- #### Geographical heatmaps
    

Mainly used by earth scientists, a geographical heatmap displays data on a real map and assigns high and low density to some geographical areas. An illustration of this case is the NASA example shown previously.

- #### AI-Generated heatmaps
    

These heatmap visualizations have been successful with the rise of Artificial Intelligence. They can be used for instance in modern vehicles to monitor the visual actions of drivers in order to increase road safety by trying to minimize their cognitive distractions. 

- #### Heatmaps in Finance
    

Heatmaps can be used by financial market specialists to quickly assess the performance of companies and the continuous fluctuation of the market values of assets, products, etc.

- #### Heatmaps in sports
    

Many sports coaches and managers use heatmaps nowadays not only to monitor their players' performance but also to study the rival team players to create winning strategies.

### A step-by-step guide on creating a heatmap on Power BI

Now that you have a general understanding of what heatmaps are and some examples of visualizations, this section will provide you with the skills to create your own table heatmap of the sales of video games. The table will show for each platform, its global sales per year, from 2006 to 2020. 

The data being used is available at [Datacamp workspace](https://www.datacamp.com/workspace/datasets/dataset-r-video-games-sales), a collaborative cloud-based environment with built-in datasets. If you’re intrigued to learn more about Power BI, check out our [Power BI fundamentals track](https://www.datacamp.com/tracks/power-bi-fundamentals). 

- #### Upload  the data into Power BI
    

From the left column panel, select the workspaces tab to upload your data. Create one if you do not have one yet. 

![Data in powerbi](https://images.datacamp.com/image/upload/v1660727929/Data_in_powerbi_1_858ac72499.gif)

- #### Create a matrix from your columns of interest
    

Before building the heatmap table visualization, we need to create a two-by-two matrix from our data. This can be done as follows from the plus sign on the left column.

Choose your data and your matrix template 

This corresponds to choosing the data you want to build the heatmap table from.

- +> Add data to get started > Pick a published data set > Select a dataset to create a report. From here you can select your data and select the Create button. Then, select the matrix template as follows from the **Visualizations** tab on the top right. 

**![Viz tab 2](https://images.datacamp.com/image/upload/v1660727929/Viz_tab_2_89a4af1e2b.gif)**

**Create matrix from data**: we need to select the row, column, and values we want to display. In our case: 

- the rows will correspond to the different platforms. 
- the columns represent the years. 
- the values are the global sales made by each platform in a specific year. 

click your matrix > expand data on the right > this will show all the columns in your data. 

- drag, drop Platform in the Rows field. 
- drag, drop Year in the Columns field. 
- drag, drop Global_Sales in the Values field. 

![global sales](https://images.datacamp.com/image/upload/v1660727929/global_sales_3_1adde6a426.gif)

Let’s remove the Total row and column because keeping them can be too much information. from the **Visualizations** tab: 

- Format your visual (paintbrush)> Turn off Row and Column subtotals

![Format viz](https://images.datacamp.com/image/upload/v1660727928/Format_viz_4_966c7416ac.gif)

- #### Build your heatmap 
    

Building the heatmap table visualization consists of two main steps: (1) encoding the background of each sales value with colors using a color range, and (2) **using the same color range** for the values font. 

(1) Global_Sales from Values > Conditional Formatting > Background color

The color is whiter when we have lower values of global sales. On the other hand, it is redder for higher values.

![adding colour](https://images.datacamp.com/image/upload/v1660727930/adding_colour_5_f1227b574f.gif)

(2) Global_Sales from Values > Conditional Formatting > Font color

![heat map 6](https://images.datacamp.com/image/upload/v1660727930/heat_map_6_cb38bb031f.gif)

Congratulations! you have created your heatmap table visualization using PowerBI.

### Things to Remember When Using Power BI Heatmaps

It is important to keep in mind the following key points when building heatmaps using Power BI:  

- Heatmaps are density and intensity driven. So it is important to choose colors that accurately represent that information. 
- If you are not using numerical data in the Values section, you won’t get the Conditional Formatting option. 
- Some cells might not have any value after transforming your data into a matrix. In this case, PowerBI gives you the option to set those values to zero, which can be helpful. 
- You can customize your Power BI heatmap by either using predefined colors or customizing your own colors.
- Power BI heatmaps are only available from the Power BI Marketplace. 

### Conclusion 

This conceptual blog has provided a complete overview of what heatmaps are, and their benefits to businesses in different domains. Also, you have learned how to create your own heatmap visualization using Power BI. 

If you are interested in getting more Data Science skills, the following courses might be a great next move. 

- [Data modeling in Power BI](https://www.datacamp.com/courses/data-modeling-in-power-bi), from this course, you will be able to understand the foundations of data modeling by going into star and snowflake schemas.
- [Data Analyst in Power BI](https://www.datacamp.com/tracks/data-analyst-in-power-bi), through hands-on exercises, you will learn data analysts’ best practices and discover advanced Power BI features, including DAX, Power Query, etc.