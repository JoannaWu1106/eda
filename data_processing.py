"""
Joanna Wu
CSE 163 AF
Data processing for refugee resettlement in Washington State.
"""

import pandas as pd


def load_data():
    """
    Read the three project datasets.
    """
    arrivals_df = pd.read_csv(
        "washington_refugee_arrivals_summary.csv"
    )

    dshs_df = pd.read_csv(
        "dshs_county_applicants_oct2024_jan2025.csv"
    )

    language_df = pd.read_csv(
        "washington_language_needs_by_county.csv"
    )

    return arrivals_df, dshs_df, language_df


def clean_language_data(language_df):
    """
    Remove ' County' from county names so they match DSHS.
    """
    language_df["County"] = language_df["County"].str.replace(
        " County", ""
    )

    return language_df


def merge_county_data(dshs_df, language_df):
    """
    Merge DSHS applicant data with ACS language data
    using county names.
    """
    language_df = clean_language_data(language_df)

    merged_df = pd.merge(
        dshs_df,
        language_df,
        on="County",
        how="left"
    )

    return merged_df


def get_reported_counties(merged_df):
    """
    Return counties with reported applicant counts.
    """
    reported_df = merged_df[
        merged_df["Count_Status"] == "Reported"
    ]

    return reported_df


def get_counties_without_king(merged_df):
    """
    Return reported counties except King County.
    """
    reported_df = get_reported_counties(merged_df)

    other_counties = reported_df[
        reported_df["County"] != "King"
    ]

    return other_counties


def calculate_arrival_changes(arrivals_df):
    """
    Calculate the change in refugee arrivals between years.
    """
    arrivals_df["Change_From_Previous_Year"] = (
        arrivals_df["Washington_Total"].diff()
    )

    return arrivals_df


def calculate_county_percentages(reported_df):
    """
    Calculate each reported county's percentage
    of the total reported applicants.
    """
    total_applicants = reported_df["Applicant_Count"].sum()

    reported_df["Applicant_Percentage"] = (
        reported_df["Applicant_Count"] / total_applicants * 100
    )

    return reported_df


def load_agency_data():
    """
    Reads refugee resettlement agency data.
    """
    agency_df = pd.read_csv(
        "washington_refugee_resettlement_agencies.csv"
    )
    return agency_df


def expand_agency_counties(agency_df):
    """
    Creates one row for each agency and county
    in its listed service area.
    """
    agency_county_list = []

    for index in agency_df.index:
        service_area = agency_df.loc[index, "Service_Area"]
        counties = agency_df.loc[index, "Counties"].split(";")
        agency = agency_df.loc[index, "Agency"]

        for county in counties:
            agency_county_list.append(
                (county.strip(), service_area, agency)
            )

    agency_county_df = pd.DataFrame(
        agency_county_list,
        columns=["County", "Service_Area", "Agency"]
    )

    return agency_county_df


def count_agencies_by_county(agency_county_df):
    """
    Counts the number of agencies listed for each county.
    """
    county_agency_counts = {}

    for index in agency_county_df.index:
        county = agency_county_df.loc[index, "County"]
        agency = agency_county_df.loc[index, "Agency"]

        if county not in county_agency_counts:
            county_agency_counts[county] = []

        if agency not in county_agency_counts[county]:
            county_agency_counts[county].append(agency)

    county_list = []

    for county in county_agency_counts:
        agency_count = len(county_agency_counts[county])
        county_list.append((county, agency_count))

    agency_counts_df = pd.DataFrame(
        county_list,
        columns=["County", "Agency_Count"]
    )

    return agency_counts_df


def merge_all_county_data(merged_df, agency_counts_df):
    """
    Combines refugee applicants, language needs,
    and agency service coverage by county.
    """
    all_data_df = pd.merge(
        merged_df,
        agency_counts_df,
        on="County",
        how="left"
    )

    return all_data_df


def get_reported_agency_data(all_data_df):
    """
    Selects counties with reported refugee applicant counts.
    """
    reported_df = all_data_df[
        all_data_df["Count_Status"] == "Reported"
    ]

    return reported_df


def main():
    """
    Load, clean, and combine project datasets.
    """
    arrivals_df, dshs_df, language_df = load_data()

    merged_df = merge_county_data(dshs_df, language_df)

    reported_df = get_reported_counties(merged_df)

    other_counties = get_counties_without_king(merged_df)

    arrivals_df = calculate_arrival_changes(arrivals_df)

    reported_df = calculate_county_percentages(reported_df)

    agency_df = load_agency_data()

    agency_county_df = expand_agency_counties(agency_df)

    agency_counts_df = count_agencies_by_county(
        agency_county_df
    )

    all_data_df = merge_all_county_data(
        merged_df,
        agency_counts_df
    )

    reported_agency_df = get_reported_agency_data(
        all_data_df
    )

    print("Annual Refugee Arrivals:")
    print(arrivals_df)

    print("Merged County Data:")
    print(merged_df)

    print("Reported Counties:")
    print(reported_df)

    print("Reported Counties without King:")
    print(other_counties)

    print("Agency Data by County:")
    print(agency_county_df)

    print("Agency Counts by County:")
    print(agency_counts_df)

    print("All County Data:")
    print(all_data_df)

    print("Reported Counties with Agency Coverage:")
    print(
        reported_agency_df[
            ["County", "Applicant_Count",
             "Language_Needs", "Agency_Count"]
        ]
    )


if __name__ == "__main__":
    main()