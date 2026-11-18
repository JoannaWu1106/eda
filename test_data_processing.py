"""
Joanna Wu
CSE 163 AF
Tests for data processing functions.
"""

import pandas as pd

from data_processing import (
    expand_agency_counties,
    count_agencies_by_county,
    merge_all_county_data,
    get_reported_agency_data
)


def test_expand_agency_counties():
    """Test splitting service areas into individual counties."""
    agency_df = pd.DataFrame({
        "Service_Area": ["Puget Sound", "Spokane"],
        "Counties": ["King; Pierce", "Spokane"],
        "Agency": ["Agency A", "Agency B"]
    })

    result = expand_agency_counties(agency_df)

    assert len(result) == 3
    assert "King" in result["County"].values
    assert "Pierce" in result["County"].values
    assert "Spokane" in result["County"].values


def test_count_agencies_by_county():
    """Test counting unique agencies in each county."""
    agency_county_df = pd.DataFrame({
        "County": ["King", "King", "King", "Spokane"],
        "Service_Area": [
            "Puget Sound", "Puget Sound",
            "Puget Sound", "Spokane"
        ],
        "Agency": ["Agency A", "Agency B", "Agency A", "Agency C"]
    })

    result = count_agencies_by_county(agency_county_df)

    king_rows = result[result["County"] == "King"]
    spokane_rows = result[result["County"] == "Spokane"]

    assert king_rows["Agency_Count"].values[0] == 2
    assert spokane_rows["Agency_Count"].values[0] == 1


def test_merge_all_county_data():
    """Test merging agency counts with county data."""
    merged_df = pd.DataFrame({
        "County": ["King", "Pierce", "Spokane"],
        "Applicant_Count": [100, 50, 30],
        "Count_Status": ["Reported", "Reported", "Reported"],
        "Language_Needs": [1000, 500, 300]
    })

    agency_counts_df = pd.DataFrame({
        "County": ["King", "Spokane"],
        "Agency_Count": [5, 2]
    })

    result = merge_all_county_data(
        merged_df, agency_counts_df
    )

    assert len(result) == 3

    king_rows = result[result["County"] == "King"]
    pierce_rows = result[result["County"] == "Pierce"]

    assert king_rows["Agency_Count"].values[0] == 5
    assert pd.isnull(pierce_rows["Agency_Count"].values[0])


def test_get_reported_agency_data():
    """Test selecting counties with reported applicant counts."""
    all_data_df = pd.DataFrame({
        "County": ["King", "Pierce", "Spokane"],
        "Count_Status": [
            "Reported", "Suppressed (<10)", "No applicants"
        ],
        "Applicant_Count": [100, None, 0],
        "Agency_Count": [5, 5, 2]
    })

    result = get_reported_agency_data(all_data_df)

    assert len(result) == 1
    assert result["County"].values[0] == "King"


def main():
    """Run all tests."""
    test_expand_agency_counties()
    test_count_agencies_by_county()
    test_merge_all_county_data()
    test_get_reported_agency_data()

    print("All tests passed!")


if __name__ == "__main__":
    main()