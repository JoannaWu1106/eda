"""
Joanna Wu
CSE 163 AF
Data visualization for refugee resettlement in Washington State.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_processing import (
    expand_agency_counties,
    count_agencies_by_county,
    merge_all_county_data,
    get_reported_agency_data
)


def load_arrival_data():
    """
    Reads the annual refugee arrival summary.
    """
    arrivals_df = pd.read_csv("washington_refugee_arrivals_summary.csv")
    return arrivals_df


def plot_annual_arrivals(arrivals_df):
    """
    Creates a line chart of annual refugee arrivals.
    FY2025 is excluded because it only contains four months.
    """
    complete_years = arrivals_df[
        arrivals_df["Fiscal_Year"] != "FY2025"
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(
        complete_years["Fiscal_Year"],
        complete_years["Washington_Total"],
        marker="o"
    )

    plt.title("Refugee Arrivals in Washington State (FY2021-FY2024)")
    plt.xlabel("Fiscal Year")
    plt.ylabel("Number of Arrivals")
    plt.grid(True)

    plt.savefig("annual_refugee_arrivals.png")
    plt.show()


def plot_arrival_changes(arrivals_df):
    """
    Creates a bar chart showing annual changes in arrivals.
    """
    arrivals_df["Change_From_Previous_Year"] = (
        arrivals_df["Washington_Total"].diff()
    )

    complete_years = arrivals_df[
        arrivals_df["Fiscal_Year"] != "FY2025"
    ]

    plt.figure(figsize=(9, 5))

    plt.bar(
        complete_years["Fiscal_Year"],
        complete_years["Change_From_Previous_Year"]
    )

    plt.title("Yearly Change in Refugee Arrivals")
    plt.xlabel("Fiscal Year")
    plt.ylabel("Change in Number of Arrivals")
    plt.axhline(y=0)
    plt.grid(axis="y")

    plt.savefig("annual_refugee_arrival_changes.png")
    plt.show()


def load_country_data():
    """
    Reads refugee arrivals by nationality.
    """
    country_df = pd.read_csv(
        "washington_refugee_arrivals_by_country.csv"
    )
    return country_df



def plot_top_countries(country_df):
    """
    Creates a bar chart of the top 10 countries
    of origin across FY2021-FY2024.
    """
    complete_years = country_df[
        country_df["Fiscal_Year"] != "FY2025"
    ]

    country_totals = complete_years.groupby(
        "Nationality"
    )["Grand_Total"].sum()

    country_list = []

    for country in country_totals.index:
        total = country_totals[country]
        country_list.append((country, total))

    top_countries = sorted(
        country_list,
        key=lambda item: item[1],
        reverse=True
    )[:10]

    top_countries.reverse()

    countries = []
    totals = []

    for country, total in top_countries:
        countries.append(country)
        totals.append(total)

    plt.figure(figsize=(14, 7))

    plt.bar(countries, totals)

    plt.title("Top 10 Countries of Origin (FY2021-FY2024)")
    plt.xlabel("Country of Origin")
    plt.ylabel("Total Refugee Arrivals")
    plt.xticks(rotation=45)
    plt.grid(axis="y")

    plt.savefig("top_10_countries.png")
    plt.show()


def plot_top_countries_by_year(country_df):
    """
    Creates a line chart showing annual arrivals
    for the top 5 countries from FY2021 to FY2024.
    """
    complete_years = country_df[
        country_df["Fiscal_Year"] != "FY2025"
    ]

    country_totals = complete_years.groupby(
        "Nationality"
    )["Grand_Total"].sum()

    country_list = []

    for country in country_totals.index:
        total = country_totals[country]
        country_list.append((country, total))

    top_countries = sorted(
        country_list,
        key=lambda item: item[1],
        reverse=True
    )[:5]

    years = ["FY2021", "FY2022", "FY2023", "FY2024"]

    plt.figure(figsize=(10, 6))

    for country, total in top_countries:
        yearly_totals = []

        for year in years:
            country_year = complete_years[
                (complete_years["Nationality"] == country) &
                (complete_years["Fiscal_Year"] == year)
            ]

            yearly_total = country_year["Grand_Total"].sum()
            yearly_totals.append(yearly_total)

        plt.plot(
            years,
            yearly_totals,
            marker="o",
            label=country
        )

    plt.title("Annual Refugee Arrivals from Top 5 Countries")
    plt.xlabel("Fiscal Year")
    plt.ylabel("Number of Refugee Arrivals")
    plt.legend()
    plt.grid(True)

    plt.savefig("top_5_countries_by_year.png")
    plt.show()


def plot_county_applicants(dshs_df):
    """
    Creates a bar chart showing refugee applicants
    in counties with reported counts.
    """
    reported_df = dshs_df[
        dshs_df["Count_Status"] == "Reported"
    ]

    county_list = []

    for index in reported_df.index:
        county = reported_df.loc[index, "County"]
        applicants = reported_df.loc[index, "Applicant_Count"]
        county_list.append((county, applicants))

    county_list = sorted(
        county_list,
        key=lambda item: item[1]
    )

    counties = []
    applicant_counts = []

    for county, applicants in county_list:
        counties.append(county)
        applicant_counts.append(applicants)

    plt.figure(figsize=(12, 7))

    plt.bar(counties, applicant_counts)

    plt.title("Refugee Applicants by County (October 2024-January 2025)")
    plt.xlabel("County")
    plt.ylabel("Number of Refugee Applicants")
    plt.xticks(rotation=45)
    plt.grid(axis="y")

    plt.savefig("refugee_applicants_by_county.png")
    plt.show()


def plot_county_applicant_percentage(dshs_df):
    """
    Creates a bar chart showing the percentage
    of reported refugee applicants in each county.
    """
    reported_df = dshs_df[
        dshs_df["Count_Status"] == "Reported"
    ]

    total_applicants = reported_df["Applicant_Count"].sum()

    counties = []
    percentages = []

    for index in reported_df.index:
        county = reported_df.loc[index, "County"]
        applicants = reported_df.loc[index, "Applicant_Count"]

        percentage = applicants / total_applicants * 100

        counties.append(county)
        percentages.append(percentage)

    plt.figure(figsize=(12, 7))

    plt.bar(counties, percentages)

    plt.title("Percentage of Reported Refugee Applicants by County")
    plt.xlabel("County")
    plt.ylabel("Percentage of Reported Applicants")
    plt.xticks(rotation=45)
    plt.grid(axis="y")

    plt.savefig("county_applicant_percentage.png")
    plt.show()


def load_merged_county_data():
    """
    Reads and merges DSHS applicant data
    and ACS language needs data.
    """
    dshs_df = pd.read_csv(
        "dshs_county_applicants_oct2024_jan2025.csv"
    )

    language_df = pd.read_csv(
        "washington_language_needs_by_county.csv"
    )

    language_df["County"] = language_df["County"].str.replace(
        " County", "", regex=False
    )

    merged_df = pd.merge(
        dshs_df,
        language_df,
        on="County",
        how="left"
    )

    return merged_df


def plot_agencies_by_service_area(agency_df):
    """
    Creates a bar chart showing the number of
    agencies in each service area.
    """
    service_counts = agency_df["Service_Area"].value_counts()

    areas = []
    counts = []

    for area in service_counts.index:
        areas.append(area)
        counts.append(service_counts[area])

    plt.figure(figsize=(10, 6))

    plt.bar(areas, counts)

    plt.title("Number of Agencies by Service Area")
    plt.xlabel("Service Area")
    plt.ylabel("Number of Agencies")
    plt.xticks(rotation=45)
    plt.grid(axis="y")

    plt.savefig("agencies_by_service_area.png")
    plt.show()


def plot_top_language_needs(language_df):
    """
    Creates a bar chart of the top 10 counties
    with the highest language needs.
    """
    county_list = []

    for index in language_df.index:
        county = language_df.loc[index, "County"]
        needs = language_df.loc[index, "Language_Needs"]
        county_list.append((county, needs))

    top_counties = sorted(
        county_list,
        key=lambda item: item[1],
        reverse=True
    )[:10]

    top_counties.reverse()

    counties = []
    needs_counts = []

    for county, needs in top_counties:
        counties.append(county)
        needs_counts.append(needs)

    plt.figure(figsize=(12, 7))

    plt.bar(counties, needs_counts)

    plt.title("Top 10 Washington Counties by Language Needs")
    plt.xlabel("County")
    plt.ylabel("Language Needs")
    plt.xticks(rotation=45)
    plt.grid(axis="y")

    plt.savefig("top_10_language_needs.png")
    plt.show()


def plot_language_needs_by_county(language_df):
    """
    Creates a bar chart showing language needs
    across all Washington counties.
    """
    county_list = []

    for index in language_df.index:
        county = language_df.loc[index, "County"]
        needs = language_df.loc[index, "Language_Needs"]
        county_list.append((county, needs))

    county_list = sorted(
        county_list,
        key=lambda item: item[1]
    )

    counties = []
    needs_counts = []

    for county, needs in county_list:
        counties.append(county)
        needs_counts.append(needs)

    plt.figure(figsize=(16, 8))

    plt.bar(counties, needs_counts)

    plt.title("Language Needs Across Washington Counties")
    plt.xlabel("County")
    plt.ylabel("Language Needs")
    plt.xticks(rotation=90)
    plt.grid(axis="y")

    plt.savefig("language_needs_by_county.png")
    plt.show()


def plot_applicants_vs_language_needs(merged_df):
    """
    Creates a scatter plot comparing refugee applicants
    and language needs across reported counties.
    """
    reported_df = merged_df[
        merged_df["Count_Status"] == "Reported"
    ]

    sns.relplot(
        x="Language_Needs",
        y="Applicant_Count",
        data=reported_df
    )

    plt.title("Refugee Applicants vs. Language Needs by County")
    plt.xlabel("Number of People with Language Needs")
    plt.ylabel("Number of Refugee Applicants")

    plt.savefig("applicants_vs_language_needs.png")
    plt.show()


def plot_applicants_vs_language_needs_without_king(merged_df):
    """
    Creates a scatter plot comparing refugee applicants
    and language needs, excluding King County.
    """
    reported_df = merged_df[
        merged_df["Count_Status"] == "Reported"
    ]

    other_counties = reported_df[
        reported_df["County"] != "King"
    ]

    sns.relplot(
        x="Language_Needs",
        y="Applicant_Count",
        data=other_counties
    )

    plt.title("Refugee Applicants vs. Language Needs (Excluding King)")
    plt.xlabel("Number of People with Language Needs")
    plt.ylabel("Number of Refugee Applicants")

    plt.savefig("applicants_vs_language_needs_without_king.png")
    plt.show()


def plot_counties_by_service_area(agency_county_df):
    """
    Creates a bar chart showing the number of
    counties covered by each service area.
    """
    service_area_counties = {}

    for index in agency_county_df.index:
        service_area = agency_county_df.loc[index, "Service_Area"]
        county = agency_county_df.loc[index, "County"]

        if service_area not in service_area_counties:
            service_area_counties[service_area] = []

        if county not in service_area_counties[service_area]:
            service_area_counties[service_area].append(county)

    service_areas = []
    county_counts = []

    for service_area in service_area_counties:
        service_areas.append(service_area)
        county_counts.append(
            len(service_area_counties[service_area])
        )

    plt.figure(figsize=(10, 6))

    plt.bar(service_areas, county_counts)

    plt.title("Number of Counties Covered by Service Area")
    plt.xlabel("Service Area")
    plt.ylabel("Number of Counties")
    plt.xticks(rotation=45)
    plt.grid(axis="y")

    plt.savefig("counties_by_service_area.png")
    plt.show()


def plot_agency_coverage(reported_agency_df):
    """
    Creates a bar chart showing agency service coverage
    across counties with reported refugee applicants.
    """
    agency_df = reported_agency_df.dropna(
        subset=["Agency_Count"]
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        agency_df["County"],
        agency_df["Agency_Count"]
    )

    plt.title("Resettlement Agency Service Coverage by County")
    plt.xlabel("County")
    plt.ylabel("Number of Agencies Listed for Service Area")
    plt.xticks(rotation=45)
    plt.grid(axis="y")

    plt.savefig("agency_coverage_by_county.png")
    plt.show()


def plot_applicants_vs_agencies(merged_df):
    """
    Creates a scatter plot comparing refugee applicants
    and agency coverage across counties.
    """
    reported_df = merged_df[
        merged_df["Count_Status"] == "Reported"
    ]

    county_list = []

    for index in reported_df.index:
        agency_count = reported_df.loc[index, "Agency_Count"]

        if agency_count == agency_count:
            county_list.append(index)

    agency_df = reported_df.loc[county_list]

    sns.relplot(
        x="Agency_Count",
        y="Applicant_Count",
        data=agency_df
    )

    plt.title("Refugee Applicants vs. Agency Coverage by County")
    plt.xlabel("Number of Resettlement Agencies")
    plt.ylabel("Number of Refugee Applicants")

    plt.savefig("applicants_vs_agencies.png")
    plt.show()


def main():
    # Load datasets
    arrivals_df = load_arrival_data()
    country_df = load_country_data()
    dshs_df = pd.read_csv(
        "dshs_county_applicants_oct2024_jan2025.csv"
    )
    merged_df = load_merged_county_data()
    language_df = pd.read_csv(
    "washington_language_needs_by_county.csv"
)
    agency_df = pd.read_csv(
        "washington_refugee_resettlement_agencies.csv"
    )

    # RQ1
    plot_annual_arrivals(arrivals_df)
    plot_arrival_changes(arrivals_df)
    plot_top_countries(country_df)
    plot_top_countries_by_year(country_df)
    
    # RQ2
    plot_county_applicants(dshs_df)
    plot_county_applicant_percentage(dshs_df)

    # RQ3: Applicants and Language Needs
    plot_applicants_vs_language_needs(merged_df)
    plot_applicants_vs_language_needs_without_king(merged_df)
    plot_top_language_needs(language_df)
    plot_language_needs_by_county(language_df)

    # RQ3: Resettlement Agency Coverage
    plot_agencies_by_service_area(agency_df)
    agency_county_df = expand_agency_counties(agency_df)

    plot_counties_by_service_area(agency_county_df)

    agency_counts_df = count_agencies_by_county(
        agency_county_df
    )

    all_data_df = merge_all_county_data(
        merged_df, agency_counts_df
    )

    reported_agency_df = get_reported_agency_data(
        all_data_df
    )

    plot_agency_coverage(reported_agency_df)
    plot_applicants_vs_agencies(reported_agency_df)


if __name__ == "__main__":
    main()