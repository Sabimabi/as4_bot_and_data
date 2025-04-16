# 🐄 Livestock Data Analysis – Kazakhstan 2024

This repository contains a collection of Jupyter Notebooks for cleaning, processing, and visualizing livestock development data in the Republic of Kazakhstan for the year 2024. The analysis includes production volumes, livestock population, milk and egg output, and slaughter statistics.

This repository contains a collection of Jupyter Notebooks for cleaning, processing, and visualizing livestock development data in the Republic of Kazakhstan for the year 2024. The analysis includes production volumes, livestock population, milk and egg output, and slaughter statistics.

## 🧠 How I Started My Code

*-Data selection:* I chose 2024 because it is the most up-to-date of all the data that was on the site.

*-Choosing subgroups for analysis:* I decided to choose these five subgroups, because they can show the changes better than the others and help to see the overall picture of the analysis, besides making the task in parts much more convenient.

Next, I just cleaned each subgroup separately and made a graph visualization for each one.


## 📁 Notebooks Overview

| File | Description |
|------|-------------|
| `1_Производство_cleaned_viz.ipynb` | Cleans and visualizes general livestock product output by category for 2023–2024 |
| `2_Численность_cleaning.ipynb` | Cleans data on livestock and poultry population by species and year |
| `3_Молоко_cleaning_viz.ipynb` | Cleans and visualizes milk production by animal type across 2023–2024 |
| `4_Производство_яиц_cleaning.ipynb` | Cleans and visualizes egg production data, grouped by farm type or region |
| `5_Убой_скота_cleaning.ipynb` | Cleans data on slaughter volumes of livestock and poultry (live weight) |
| `livestock_cleaning.ipynb` | General-purpose cleaner for merging and inspecting all raw Excel tables |
| `split_livestock_tables.ipynb` | Splits one large Excel file into five smaller files by major livestock categories |

## 📊 Topics Covered

- Handling missing and irrelevant rows  
- Sheet-wise merging and filtering  
- Grouped bar charts for yearly comparisons  
- Horizontal bar charts for sorted volume metrics  
- Removing technical rows (e.g., headings, summaries)  
- Saving clean `.xlsx` files for each analysis

## 🧰 Technologies Used

- **Python 3.13**  
- **pandas** for data manipulation  
- **matplotlib** for visualization  
- **openpyxl** and **xlrd** for Excel processing  
- Jupyter Notebooks (.ipynb) for iterative analysis

## 📦 Folder Structure (Suggested) 

```
📁 data/
├── 2024.xlsx
├── 1_Производство_cleaned.xlsx
├── 2_Численность_cleaned.xlsx
├── 3_Молоко_cleaned.xlsx
├── 4_Производство_яиц_cleaned.xlsx
├── 5_Убой_скота_cleaned.xlsx


✅ Final Summary
This project demonstrates a full pipeline of working with real-life agricultural statistics — from raw Excel spreadsheets to clean, structured data and visual insights. Through cleaning, filtering, and visualization of five selected livestock indicators for 2024, the project provides a practical and accessible way to analyze Kazakhstan's livestock development. By breaking the task into subgroups and focusing on clarity, each stage of the workflow contributes to building a reliable analytical foundation for further research or reporting.



```
## ✨ Made by: Kozhakhmet Aruzhan and Rakhat Sabina 
```
 



