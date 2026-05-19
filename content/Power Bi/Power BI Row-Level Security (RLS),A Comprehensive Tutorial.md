## What is Row-Level Security?

Row-Level Security (RLS) is a security feature in Power BI that restricts access to rows in a table based on the identity of the user viewing the report. Rather than duplicating reports for different user groups, RLS allows you to apply filters at the data level so that each user sees only the data they are permitted to view.

This is crucial for preserving data confidentiality and integrity, especially in scenarios involving sensitive or proprietary information. RLS operates within the [Power BI data model](https://app.datacamp.com/learn/tutorials/data-modeling-in-power-bi-tutorial) and ensures that unauthorized users cannot access restricted data, even through indirect methods such as slicers or drill-downs.

### Roles and filters

RLS implementation is based on three core elements:

- Roles: Logical groupings with defined access rules.
- [DAX](https://app.datacamp.com/learn/tutorials/power-bi-dax-tutorial-for-beginners) filters: Expressions that determine what data each role can access.
- User assignments: Configuration of which users or groups belong to which roles.

These elements work in tandem to evaluate each query against the access conditions before returning results.

### Use cases

RLS is highly applicable across many industries and scenarios, including:

- Sales territories: Sales managers see only their region’s performance data.
- Healthcare: Doctors access records of their assigned patients only.
- Multi-tenant SaaS: Clients see only their own organization’s data in shared dashboards.

This security model enables shared datasets to remain secure while minimizing duplication and administrative overhead.

## Static vs Dynamic RLS Architectures

Row-level security can be split into two types: static and dynamic.

I’ve summarized their differences in the table below:

|   |   |   |
|---|---|---|
|**Criteria**|**Static RLS**|**Dynamic RLS**|
|Setup Time|Quick|Moderate|
|Maintenance|Manual|Table-driven|
|Scalability|Limited|High|
|Complexity|Low|Moderate to High|

Tip: Use static RLS for small, fixed user groups. Use dynamic RLS for growing or large-scale environments.

I’ll go through some implementations of both static and dynamic examples below.

### Static RLS implementation

Static RLS involves creating roles with hardcoded DAX filters. Each role corresponds to a specific group or segment, such as a geographic region or department.

Here are the general steps to implement a static RLS:

1. Create a role named, e.g., "Region_East."
2. Apply a filter such as `[Region] = "East"` to that role.
3. Assign specific users to the role in Power BI Service.

### Dynamic RLS implementation

Dynamic RLS uses functions like `USERNAME()` or `USERPRINCIPALNAME()` combined with mapping tables to dynamically filter data based on user identity.

Here are the general steps to implement a dynamic RLS:

1. Create a mapping table linking users to access levels. This will be your security table. This table should include columns like user emails, their access regions, and their names.
2. Write a DAX filter like: `[Region] = RELATED(UserRegion[Region])`
3. Filter that table with: `UserRegion[Email] = USERPRINCIPALNAME()`

## Setting Up Row-Level Security in Power BI Desktop

We’ll now look at a quick guide on how to set up static row-level security using a simple sales dataset.

### 1. Creating a sample dataset using Python

To test RLS, create a sample dataset using Python:

`import pandas as pd  data = {     'Salesperson': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie'],     'Region': ['East', 'West', 'South', 'East', 'West', 'South'],     'SalesAmount': [15000, 20000, 18000, 17000, 21000, 16000],     'Email': ['alice@company.com', 'bob@company.com', 'charlie@company.com'] * 2,     'Date': pd.date_range(start='2025-01-01', periods=6, freq='M') }  sales_df = pd.DataFrame(data) sales_df.to_csv('sample_sales_data.csv', index=False)`

[](https://app.datacamp.com/workspace)

### 2. Importing into Power BI and Creating a Reference Visualization

1. Open Power BI Desktop.
2. Go to Home > Get Data > Text/CSV.
3. Select the `sample_sales_data.csv` file.

![loading csv dataset](https://media.datacamp.com/cms/ad_4nxfe_vbpssizmozzw4tadbncyjtby6jcet0qajwu3_rwnmijqf65mk2ugso9bjddv4o_ekbfw1ugg6oxgqaz7xf4z1435stpfmcaai5pwrj3cukkshyoihsgexqrbesonzdwswuyxq.png)

4. Load the data into the model.

Ensure proper data types and confirm that the `Email` column matches login identity formats (usually email).

5. Create a basic Stacked Column Chart in Power BI. Drag the Date field to the X-axis and the SalesAmount to the Y-axis.

Here’s what your chart should look like:

![sample visualization](https://media.datacamp.com/cms/ad_4nxfxawsc9mqrrlq2we2umunybgtx11mnudigvw0zr1hlhjcxpposl9j5jaxe2vj7plx1cby0vsl9mfvp3gvznhaq6y7xxxodxey_8y6z5xjnzqfkim8ceonvbq9r_wvj_so7zk7zqa.png)

More on using Power BI can be found in our [cheat sheet](https://www.datacamp.com/cheat-sheet/power-bi-cheat-sheet), as shown below.

[![power BI cheat sheet](https://media.datacamp.com/cms/ad_4nxd_pq5_xkqwnjwm1xvjx-bgyi5f_xf3fd5svdbdnjwy0r4xkzt3zl0rr4npe8vsxdl0axgj_4faqw9x588l0meqnimsldukb9putez1n6nqmbydrcwrupdoxgqmomjlm0bnn1et.png)](https://www.datacamp.com/cheat-sheet/power-bi-cheat-sheet)

### 3. Creating roles

Next, let’s create some roles to define which roles can have what permissions.

1. Go to Modeling > Manage Roles.![manage roles](https://media.datacamp.com/cms/ad_4nxfxmhzqccrx9nsiwlbxz0t5tfnrpjhhjdhiw2tguzwqfck3zk-hnsvx-n8dsqpxvkjvhqhqmvggp2rirc_y57dd1sta5jer7mdjzaikpctnaz38d3jy9fyeawfesguebkvzkhk1wg.png)

2. Click Create and name your role, e.g., `SalesRegionStatic`.
3. Select the relevant table.
4. Enter a filter DAX expression:

```dax
[Email] = “charlie@company.com”
```

This is what your interface should look like:

![creating roles in DAX](https://media.datacamp.com/cms/ad_4nxdwrddoc7rhdbyjp51-tupxpgc4ytw2xijbyfz9j2rqtosytke0wkjlubups8bfe9gkt0hjgrtsv_po1qlxjc1nqsi_sb_1gy0f1fb8uy0b93pfocejrekjqqasl2x8pknproma.png)

5. Save and close the dialog.

If the changes are saved successfully, a green bar notification will appear as shown below.

![security roles created](https://media.datacamp.com/cms/ad_4nxecdgnw_pguznvagtxb2b850nbv3tmkeh2fmmvtiloymirukfsw9oa3aw2mtqkzkjh-59c_zin7xbfziaxtrb1valr6xk0286-7aagpegms2jdb1zhtvaujnpkueg9_smfjplpg7a.png)

### 4. Testing roles

1. Go to Modeling > View as Roles.

![View as button](https://media.datacamp.com/cms/ad_4nxcj_goz2vm2hzeuinecfh4_py-d6v5n5grkzdym4nqyjh6xuvldu-fhfsfhgv8-nkhevkmyhug1jr6xcyqnry9uqxrljgh21xh2ohwib6lmjzroskowx-bb9mollkj0uvio4vz9dq.png)

2. Choose the `SalesRegionStatic` role we created earlier.

![select security roles](https://media.datacamp.com/cms/ad_4nxfe7zisv7degvnscxvmvc4x4ax1rnip0_p-w2gu61u8_ai7pydi2c9qa0dl-i-rsuxhiduhg8jlz_rvafmrszssab3nqkzyzc4wbo3-gpitm_ww7l8fz6w7gf1vqi1uj8zjocxrwa.png)

3. View report visuals filtered by that identity.

As you can see from the image below, the chart has been filtered to show only data where the email is “charlie@company.com”.

![end result data visualization](https://media.datacamp.com/cms/ad_4nxdyhbus0z-y8cst4myfegukv15nti4vik8y4i8jo6iy01vjyjct65nd1e9it8u3cq1xbfuuerqrzrhvu-c30j4sg8ptaaovv0avulksfcif0n8-w21adwcvghiwq4gaz0hwliot5g.png)

This allows local validation before deployment.

## Assigning Users and Managing Roles in Power BI Service

Once your RLS roles are set up and tested in Power BI Desktop, the next step is to publish the report to the Power BI Service. This allows you to assign specific users or security groups to each role, ensuring that access control is enforced when the report is shared.

### 1. Publishing the report to Power BI Service

1. In Power BI Desktop, click on Home > Publish > To Power BI.
2. Choose the target workspace in your Power BI Service.

![publishing to Power BI workspace](https://media.datacamp.com/cms/ad_4nxett9kijcm-g0ujxlhhxsowkashnz-84ficz5ledm2sa2y-uvkj77mxfkxu63hagrbdd2flp6mvrhmfsa6dx7tcetx9gprq8alkkhk7n0jwiuakzehaznxtmynive6vptezd4w_.png)

3. After publishing, log in to Power BI Service at [](https://app.powerbi.com/)[https://app.powerbi.com](https://app.powerbi.com/).

Here’s what mine looks like on the Power BI service on the web.

![Power BI service](https://media.datacamp.com/cms/ad_4nxfdmiiygln50gbuuylawb9_t8jfsy6kwj5x3ylpqjrpnurz-s1gxuit7cgllpzczbzz4yvybmy767jkfgqtc85490dehcyojx_ay7ospea1jafyqtjhd2nv39dmz-ijsikroqoeya.png)

Publishing is a prerequisite for configuring RLS role assignments, as the roles defined in Power BI Desktop are transferred along with the dataset.

### 2. Accessing security settings

1. Select the More options menu for your relevant semantic model.Click the ellipsis (...) next to the dataset and select Security.
2. You’ll see a list of roles defined in Power BI Desktop.

This is where you assign users or Azure Active Directory (AAD) groups to each role.

### 3. Assigning individual users and security groups

To assign users, enter their full email addresses in the text box under the desired role, press Enter, and click Add.

![assigning users on PBI service](https://media.datacamp.com/cms/ad_4nxdrv6qf6kquemgie2ig_acxzvgvgy2kyj-1g8oigjstlmna31f8wbxsjolbt19jtr5ukn0fh70qdu_2lqdvogyf6rkha2cmtzze69cpnistfvambfhcsrvc3rhqrlv22wyyt66lza.png)

To assign AAD groups, use the name of the group (e.g., `Sales_Region_East` or `Finance_Team`). Do ensure that the group is already defined and maintained in Azure Active Directory.

### 4. Verifying assigned access

After assigning users or groups, take some time to verify that the correct data is presented to the right group.

Each person will only see the data filtered by the DAX expression linked to their role. They will not be notified of role assignment directly, so you may want to communicate any access instructions after you’ve done the verification.

### 5. Testing role assignments in Power BI Service

1. On the same page, click on your RLS name you defined earlier and click on the ellipsis (...), and then Test as role.

![testing as user roles on PBI service](https://media.datacamp.com/cms/ad_4nxd9ea9nxlrikcayvuf3gq7zsob9hydkqaq9n-3m7jdur0uo9yvit1iv2l5qppfpg3-x7crikdbr7ki-4ibbn0w2q1f2m0cp9xzhwzd875aeszpr7c9uuksywxku5w4ekrdeqpcbua.png)

2. Power BI will open a read-only version of the report showing only the data permitted by the selected role.

For dynamic RLS, you can also simulate what a specific user will see:

- Click Test as role.
- Enter the email of a user to simulate their experience.

This is useful for ensuring your dynamic filters (e.g., based on `USERPRINCIPALNAME()`) are functioning correctly.

## Advanced Implementation Techniques

RLS can be further integrated into your Power BI workflow through some advanced techniques. Here are some that you should take note of:

### 1. Security group integration

Using Azure Active Directory (AAD) security groups allows you to assign access permissions to entire groups rather than individual users. 

This practice is especially useful in enterprises where employees frequently join or leave teams, as it eliminates the need to manually update access permissions in Power BI.

### 2. Complex data model considerations

When building large-scale data models, ensure that RLS does not interfere with relationships and filter propagation. 

Here are some tips:

- Use a star schema design to avoid complex joins.
- Limit the use of bi-directional relationships unless necessary.
- Avoid ambiguous relationships that could result in incorrect filtering.
- Optimize performance by minimizing calculated columns in heavily filtered tables.

### 3. Hybrid approaches

A hybrid approach to RLS is the combination of static and dynamic techniques. 

For example, you might define a static role to grant access to a specific business unit and apply dynamic filtering within that role based on individual email addresses or usernames. This method enables layered and flexible security logic.

### 4. Object-level security (OLS)

Object-Level Security allows you to hide entire tables or columns from certain roles. It complements RLS by adding another layer of data protection. OLS can be used for sensitive fields like salary or medical information.

## Testing and Validation Strategies

### 1. Desktop testing

Power BI Desktop provides a helpful way to simulate different user views through the “View as” role feature. This feature helps report developers validate that the Row-Level Security logic is working correctly before publishing the report.

How to test RLS in Power BI Desktop:

1. Click on the Modeling tab.
2. Select View as from the ribbon.
3. Choose the roles you've configured (e.g., SalesRegionStatic).
4. Optionally enter a test username/email if you're using dynamic RLS.
5. Click OK and examine how visuals are filtered.

This simulates the report as if a user assigned to that role is viewing it. It's especially helpful when testing dynamic RLS filters that depend on DAX functions like `USERPRINCIPALNAME()`.

### 2. Service testing

Once published to Power BI Service, RLS should be tested again in the cloud environment to ensure accuracy.

How to test RLS in Power BI Service:

1. Navigate to the dataset in your workspace.
2. Click the ... next to the dataset > Security.
3. Select a role > click Test as role.
4. Use the “Test as specific user” option to simulate dynamic RLS filters.

This ensures the filters behave as expected for actual users.

### 3. Key validation tips

For validation, you can consider using test accounts or service identities to mimic real usage. All filters on key visuals, like tables and charts, should also be reviewed periodically.

You should also check through slicers, drillthrough, and bookmarks thoroughly to ensure that they’re not leaking unauthorized data.

## Common Pitfalls and Solutions

Implementing RLS may come with some issues, so here are some common ones and how to fix them.

### 1. Post-publishing issues

After publishing to Power BI Service, some users find that RLS does not behave as expected, even though it worked in Power BI Desktop.

Solutions:

- Ensure the report is re-published after making role or filter changes.
- Confirm that the email used in USERPRINCIPALNAME() matches the login domain format in the dataset.

### 2. Workspace role conflicts

Users with certain workspace roles (Admin, Member) may inadvertently bypass RLS.

Solutions:

- Assign users as Viewers in the workspace to enforce RLS rules.
- Avoid giving Contributor/Admin rights unless necessary for content development.

### 3. DAX function limitations

Common pitfalls arise from the misuse of DAX functions like `USERNAME()` and `USERPRINCIPALNAME()`:

- `USERNAME()` may return a local account name instead of an email when tested in Desktop.
- Use `USERPRINCIPALNAME()` for consistency with cloud identity behavior.

Tips:

- Add a reference table with sample emails to facilitate local testing.
- Use conditional logic or default values in DAX to prevent filter failures.

### 4. DirectQuery and SSO challenges

Dynamic RLS with DirectQuery sources requires extra attention, especially when used with Single Sign-On (SSO).

Common issues:

- Incorrect gateway configuration can block user impersonation.
- SSO setup with Kerberos may fail if SPNs are misconfigured.

Solutions:

- Consult Microsoft documentation on SSO with Power BI gateways.
- Work closely with IT and infrastructure teams to enable Kerberos delegation.

## Removing or Disabling RLS for Public Access

There may be scenarios where RLS needs to be removed temporarily (e.g., for demos or open dashboards) or permanently (e.g., when sharing data with external stakeholders). In such cases, you’ll have to be careful with visibility settings to prevent unexpected leakages.

### Disabling RLS in Power BI Desktop

To disable RLS:

1. Open your report in Power BI Desktop.
2. Navigate to Modeling > Manage Roles.
3. Select and delete all roles or disable their filters.
4. Save and re-publish the dataset to Power BI Service.

Once removed, all users will be able to access the full dataset unless other security measures are in place.

### Secure sharing without RLS

If RLS is not feasible or necessary, consider the following practices to maintain data security:

- Use dataset-level permissions: Share the dataset or report only with trusted users and use workspace permissions (Viewer, Contributor) appropriately.
- Avoid publishing to web: “Publish to Web” removes all security controls. Instead, use “Embed for organization” or Power BI Embedded for secure public-style sharing.

Removing RLS doesn’t mean removing all security. Use other layers of access control and sharing features in Power BI Service to ensure responsible data dissemination.

## Best Practices for Enterprise Deployment

Successful enterprise-wide deployment of Row-Level Security requires thoughtful planning, scalable architecture, and proper governance. This section outlines proven best practices across different dimensions of RLS implementation.

### 1. Data modeling

A well-designed data model supports efficient and maintainable RLS configurations.

Recommendations:

- Follow a star schema with clear relationships between fact and dimension tables.
- Avoid unnecessary bidirectional relationships that could introduce ambiguity in filtering.

### 2. Role management

Managing RLS roles centrally and consistently helps reduce errors and improve collaboration.

Recommendations:

- Maintain a role definition document to track RLS logic and DAX expressions.
- Use descriptive role names (e.g., “Region_East_Sales”) to avoid confusion.

### 3. Performance optimization

RLS can impact report performance, especially when complex filters or large datasets are involved.

Recommendations:

- Pre-aggregate data, where possible, using summary tables.
- Minimize the use of calculated columns in RLS logic.
- Use indexing and optimized queries in source systems to support DirectQuery scenarios.

## RLS vs Alternative Security Models

Let’s now compare the differences between Row-Level Security (RLS) and other security features, particularly Object-Level Security (OLS).

### 1. Granularity and use case

RLS allows access control to individual rows of data, which is ideal for filtering data by user identity, geography, department, or business unit. OLS, on the other hand, controls access to entire tables or columns, which is useful for hiding sensitive financial or HR information (e.g., salary column). 

### 2. Implementation and dynamic adaptation

RLS can be easily implemented within Power BI Desktop via DAX filters on roles. These rules can be either static (hard-coded filters) or dynamic (user-driven logic). OLS is configured via the Tabular Editor or XMLA endpoint. It also requires a premium workspace or Power BI dataset hosted in Analysis Services.

I’ve put together a comparison summary in the table below:

|   |   |   |
|---|---|---|
|**Feature**|**RLS**|**OLS**|
|Level of Control|Row-level|Table/Column-level|
|User-Specific Views|Yes|No|
|GUI Configuration|Supported in Power BI Desktop|Requires external tools|
|Use Cases|Sales region access, employee-specific|Hide salary, sensitive columns|
|Scalability|Moderate to High (with dynamic setup)|High (if integrated with governance tools)|

## Conclusion

Wrapping up, row-level security (RLS) in Power BI is a key method for ensuring data governance within the platform. It allows organizations to deliver personalized, secure analytics experiences within a single report or dashboard, without compromising the confidentiality or integrity of underlying data.
up:: [[Power BI MOC]]
