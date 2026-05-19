## What is Power BI Copilot?

![Power BI Copilot](https://media.datacamp.com/legacy/v1716458921/image_63fe60892c.jpg)Power BI Copilot. Source: [2WTECH](https://2wtech.com/benefits-of-using-copilot-in-power-bi/)  
  

For those unfamiliar with Power BI, it is a popular business analytics service from Microsoft. Power BI extracts and transforms data and provides beautiful visualizations to aid organizations in making better business decisions. DataCamp offers many courses for beginners who want to learn, such as [Introduction to Power BI](https://www.datacamp.com/courses/introduction-to-power-bi).

The newest addition, Power BI Copilot, enhances the functionality of Power BI using generative AI. Data professionals can now uncover, extract, and analyze data faster by simply asking questions or making requests in plain language.

In other words, with Power BI Copilot, Power BI users have a generative AI coding assistant that is present with their data, understands their business context, and provides support in these areas:

- **Generating Reports:** Power BI Copilot receives input using natural language in order to generate insightful reports. 
- **Suggesting Metrics and Visuals:** Power BI Copilot suggests which data visualization might be most appropriate given the data's features and business context. 
- **Producing Narratives:** Power BI Copilot will craft a story to explain the data and the reasoning behind the numbers.

Simply put, while other coding assistants only help with code generation, Power BI Copilot transforms your data into a compelling data narrative so your organization can make better data-driven business decisions. 

## How Power BI Copilot Works

Let’s explore how Power BI Copilot works in terms of architecture and user experience. Understanding how Power BI Copilot works will help us phrase our prompts for the most accurate and effective insights. 

### Power BI Copilot’s architecture

![How Microsoft Copilot accesses data from various sources.](https://media.datacamp.com/legacy/v1716458921/image_c07c6f4193.png)How Power BI Copilot accesses data from various sources. Source: [Microsoft](https://imaginet.com/2023/microsoft-365-copilot-for-power-bi/)  
  

Like other language models, Power BI Copilot uses natural language processing (NLP) techniques to understand the context and meaning behind text data. 

More specifically, Power BI Copilot works because it has been trained on large datasets, and when faced with new data, it converts words to numbers where it can then analyze sequences and relationships. Specifically, it uses the following machine learning techniques.

- **Recurrent Neural Networks:** [RNNs](https://app.datacamp.com/learn/tutorials/tutorial-for-recurrent-neural-network) use sequential data to solve language-related problems like speech recognition or translation.
- **Transformers:** [Transformers](https://app.datacamp.com/learn/tutorials/how-transformers-work) understand and generate human-like text by analyzing patterns in large amounts of text data.

After understanding the data context, Power BI Copilot uses its semantic and data modeling capabilities to find relationships and patterns in your data. It then provides targeted recommendations and suggestions based on natural language prompts from the user. 

### Power BI Copilot’s user experience

The machine learning behind Power BI is pretty amazing stuff. Let's now take a look at the result of these algorithms in the user experience.

Power BI Copilot suggestions appear in clear visuals so you can understand data more easily. You can refine these suggestions within the Power BI Desktop interface and provide feedback, which then helps improve Copilot over time.

Let’s illustrate with an example: One could ask Power BI Copilot: "C_reate a page to analyze the sales amount, revenue, and profit margin of different products, categories, and subcategories over time and across regions."_ As a result of this prompt, it can give a full product analysis, including the sales performance of different products, and provide this information in a custom-built dashboard. Take a look:   
  

![Power BI Copilot’s dashboard](https://media.datacamp.com/legacy/v1716458922/image_2ecacad136.png)Power BI Copilot’s dashboard after a user-generated prompt. Source: [Microsoft](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prompts-report-pages)  
  

You can see how Power BI Copliot’s easy-to-use interface makes it seamless to interact with it using natural language. You can ask questions about the data and receive insightful feedback. 

Overall, it’s a quicker, more natural, and interactive way of exploring and analyzing data accurately and effectively. And it’s handy for data analysts and business intelligence professionals who are tight on deadlines and might be overloaded with work. 

## Exploring Power BI Copilot Features and Use Cases

Let’s now examine Power BI’s most desirable features and use cases. Common use cases include semantic modeling, report creation, narrative generation, and more. As you will see, Power BI Copilot can be leveraged during all parts of the data analysis lifecycle. 

### Semantic modeling

[Semantic modeling](https://www.datacamp.com/blog/what-are-power-bi-semantic-models) refers to structuring data in a way that becomes meaningful and easily understandable. This involves defining clear relationships between different data elements, organizing data hierarchies, and creating measures and calculated columns that express business logic. For example, in order to see how customers might place orders for different products, we have to have keys to join those relationships. 

### DAX formula suggestions

DAX, which stands for [Data Analysis Expressions](https://www.datacamp.com/courses/dax-functions-in-power-bi), creates custom calculations on the data stored in a data model. It's similar to Excel formulas but has been enhanced to work with relational data and perform dynamic aggregation. Amazingly, Power BI Copilot can write these DAX queries for you, including highly customized calculations for report pages.

### Report creation

One of the most striking features of Power BI Copilot is its ability to create report pages that include nice-looking charts and graphs. Power BI Copilot leverages generative AI to identify key trends, relationships, and patterns in creating reports. By automating report creation, analysts save a huge amount of time compared to manually building reports through the user interface.   
  

![A report page in Power BI Copilot](https://media.datacamp.com/legacy/v1716458921/image_0b27d5c683.png)A report page in Power BI Copilot. Source: [Microsoft](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-create-desktop-report)

### Narrative generation

An equally compelling but lesser-known use case of Power BI Copilot is its narrative generation. Not only can analysts use Power BI Copilot to automate report creation, Power BI Copilot can also generate a narrative summarizing the data insights. Power BI Copilot presents the insights in a natural language format, making your reports easier to understand for even non-technical audiences.

### Report summarization in the copilot pane

You can easily create a summary of any report page in the Copilot pane. This will help you quickly understand your reports. Even if you don’t have permission to edit your organization’s reports, you can still understand the report without editing or changing the original Power BI report.   
  

![Report Summarization in Power BI Copilot Pane](https://media.datacamp.com/legacy/v1716458922/image_81aba5ebd0.png)Report Summarization in Power BI Copilot Pane. Source: [Microsoft](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-pane-summarize-content)

### Visual summarization in the copilot pane

The Copilot also allows you to automatically generate a written summary or narrative about the data visualizations and insights in your Power BI report. This summary is displayed as a visual element right within the report itself.

Instead of manually writing an explanation for each chart, graph, or table in your report, the Copilot can analyze the data and create a plain-language narrative that summarizes and explains the key takeaways.

### Synonyms to enhance Q&A

When working with Power BI reports, you can ask natural language questions about the data, and it will understand the intent behind the question to provide relevant insights. However, how you phrase your questions may sometimes not match the terminology used in the data model itself.

So, by providing synonyms, the Copilot can understand a wider range of user questions. 

![Setting up the Q&A visual in Power BI](https://media.datacamp.com/legacy/v1716458921/image_07fa99f0f0.png)Setting up the Q&A visual in Power BI. Source: [Microsoft](https://learn.microsoft.com/en-us/power-bi/natural-language/q-and-a-copilot-enhancements)  
  

### Content suggestions for a report

Power BI Copilot leverages the power of AI to analyze your data and give you different content recommendations. These content recommendations can include: 

- **Suggesting Reports:** Power BI Copilot can suggest different report pages for you based on the unique features of your data and business context.
- **Creating Visuals:** Power BI Copilot can create all kinds of visualizations, everything from histograms to heat maps. 
- **Optimizing Tables:** These are the tables that store your data and are joined together for report creation. 

Power BI Copilot can surprise by making suggestions for improvement - things the user never even thought to ask about. 

## How to Enable Power BI Copilot with Microsoft Fabric

Your organization can only begin using Copilot in Power BI if you enable Copilot in Microsoft Fabric. Microsoft Fabric is a software-as-a-service platform (SaaS) that combines components of Power BI and other Microsoft services in a unified environment. Fabric is accessed by purchasing a Microsoft Azure subscription. 

Here is a step-by-step guide on how to enable Power BI Copilot with Microsoft Fabric. The instructions are a bit different depending on whether or not Azure is available in your region. 

### Enabling Power BI Copilot If Azure is available in your region

Here are the steps if Azure is available:

- **Step 1:** Go to [Microsoft Fabric’s website](https://www.microsoft.com/en-us/microsoft-fabric) and log in with your admin account credentials.
- **Step 2:** Go to **Fabric Settings** and select **Admin Portal** from the menu options.
- **Step 3:** Open the **Fabric Admin Portal** and go to **Tenant settings**. Here, you can search for the **Copilot Settings** for your organization.
- **Step 4:** Turn the switch on to enable Copilot in Fabric. 

![Enabling Power BI Copilot with Microsoft Fabric](https://media.datacamp.com/legacy/v1716458922/image_6ac42dd3e9.png)Enabling Power BI Copilot with Microsoft Fabric. Source: [Microsoft](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-enable-power-bi)

  
Switching on the button enables Copilot for all applications and services it can integrate with, not just Power BI. The final four steps inside the **Admin Portal** are quick. 

- **Step 5:** First, search for **Copilot in Azure OpenAI Service (preview)** settings.
- **Step 6:** Turn the switch so it says **Enabled**.
- **Step 7:** Next, define who can access Copilot in Fabric. 
- **Step 8:** Click the **Apply** button to save all the changes. 

### Enabling Power BI Copilot If Azure isn’t available in your region

In addition to the above-mentioned steps, you have to perform two extra steps to enable Power BI Copilot with MS Fabric if Azure isn’t available in your region: 

- **Step 9:** Switch on the setting that says **Data sent to Azure OpenAI can be processed outside your capacity’s geographic region**.
- **Step 10:** Select **Apply** to save this change. 

![Enabling Power BI Copilot with Microsoft Fabric when Azure isn’t available in your region](https://media.datacamp.com/legacy/v1716458922/image_71405eb166.png)Enabling Power BI Copilot with Microsoft Fabric when Azure isn’t available in your region. Source: [Microsoft](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-enable-power-bi)  
  

## Exploring Power BI Copilot Plans and Pricing

The cost of using Fabric Copilot in Power BI depends on the number of prompts you send and the responses you receive. These interactions are measured using tokens, which can be words, spaces, or punctuation marks. Input tokens include the text you type into the Copilot chat and metadata from your tables. Output tokens cover code, Power BI reports, and text responses generated by Copilot.

Luckily, Power BI will cache the input tokens for 2 days. When you re-run the same prompt on the same data, you get a faster response and aren’t even charged.  
  

![Calculating capacity consumption cost (CU seconds) of Power BI Copilot interactions](https://media.datacamp.com/legacy/v1716458922/image_967bfe8721.jpg)Calculating capacity consumption cost (CU seconds) of Power BI Copilot interactions. Source: [Microsoft](https://blog.fabric.microsoft.com/en-us/blog/fabric-copilot-pricing-an-end-to-end-example-2/)  
  

## Advanced Tricks and Best Practices

Here we will review a few best practices and helpful keyboard shortcuts to get the most out of Power BI Copilot’s features and functionality.

### Best practices

Here are a few heuristics: 

1. **Prepare Data in Advance:** Data cleaning requires standardizing naming conventions, removing duplicates, and ensuring the data type is correct. So prepare your data in advance instead of solely relying on Power BI Copilot to clean and organize data for you.
2. **Calculate Complex Metrics:** Reduce the burden on Copilot by working through complex calculations in Power BI Desktop before using Copilot. This will streamline the report generation process when complex calculations are involved.
3. **Experiment with Prompts:** Explore the potential of Power BI Copilot by using natural language to ask questions, then drill down further with follow-up questions.
4. **Refine Copilot’s Output:** Use Copilot’s formatting options to enhance generated reports' visual appeal and readability. For example, if you don’t like a chart type, you can ask Power BI Copilot to change the chart to a bar chart or a line graph. 
5. **Document your Prompts:** Save the prompts you use to generate reports. You can refer to them later, saving time.
6. **Combine Your Manual Edits with Copilot’s Output:** Combine your charts and data points with Copilot-generated visuals for a more customized report. 

### Some helpful keyboard shortcuts

And here are some general keyboard shortcuts for Power BI that can streamline your workflow.    
  

|Technique|Description|
|---|---|
|Resize a visual|Use arrow keys|
|Group visuals|Select visuals + Ctrl + G|
|Show or hide tooltip|Ctrl + H|
|Selecting or unselecting a data point|Enter or spacebar|
|Move a visual on the canvas|Use arrow keys (up, down, right, left)|
|Canvas zoom-in|Ctrl + Plus|
|Canvas zoom-out|Ctrl + Minus|
|Move around the canvas|Use arrow keys (up, down, right, left)|
|Interact with a slicer|Use the up arrow key and down arrow key to move focus between menu items|
|Select multiple contiguous items from the slicers|Shift + Up arrow key/Down arrow key, then Shift + F10 to open the context menu|

## Final Thoughts on Leveraging Power BI Copilot for Quick Data Analysis 

Power BI Copilot is a revolutionary tool in the realm of business intelligence, seamlessly integrating AI to enhance data analysis. For those aiming to elevate their skills, it's crucial to [Learn Power BI](https://www.datacamp.com/learn/power-bi). Additionally, [Understanding Large Language Models for Business](https://campus.datacamp.com/courses/large-language-models-for-business/the-rise-of-llms-in-the-business-realm?ex=5) and enrolling in a [Large Language Models Concepts Course](https://www.datacamp.com/courses/large-language-models-llms-concepts) will deepen your knowledge of the advanced capabilities offered by Power BI Copilot.

[Implementing AI Solutions in Business](https://campus.datacamp.com/courses/implementing-ai-solutions-in-business/benefits-limitations-and-use-cases-of-ai?ex=1) has become more straightforward with the introduction of Power BI Copilot. This tool aids in generating reports, suggesting metrics, and crafting narratives, making it an invaluable resource for data analysts and business intelligence professionals. By mastering Power BI Copilot, users can significantly boost their productivity and derive more insightful, data-driven decisions.
up:: [[Power BI MOC]]
