#test
@pytest.mark.parametrize("pollutant_column", ['pm10_concentration', 'pm25_concentration', 'no2_concentration'])
def test_top_10_pollutants(df, pollutant_column):
    """
    Tests that the top 10 cities with the highest pollutant concentration are correctly displayed
    in the sorted DataFrame for a given pollutant.

    Parameters:
    df (DataFrame): The DataFrame containing air quality data.
    pollutant_column (str): The column name representing the pollutant to compare (e.g., 'pm10_concentration', 'pm25_concentration', 'no2_concentration').

    Returns:
    None
    """
    # Check if the necessary column exists
    assert pollutant_column in df.columns, f"Test failed: '{pollutant_column}' column is missing."

    # Drop rows where the pollutant concentration is missing (NaN)
    df_clean = df.dropna(subset=[pollutant_column])

    # If after cleaning, we don't have at least 10 cities, the test is invalid
    assert df_clean.shape[0] >= 10, f"Test failed: Not enough cities with valid {pollutant_column} data."

    # Sort the DataFrame by the pollutant concentration in descending order
    sorted_df = df_clean.sort_values(by=pollutant_column, ascending=False)

    # Select the top 10 cities
    top_10_cities = sorted_df.head(10)

    # Extract the cities from the top 10 (for comparison later)
    top_10_cities_list = top_10_cities["city"].tolist()

    # Check for invalid values (cities with concentration of 0 or negative values)
    invalid_cities = [city for city, value in zip(top_10_cities["city"], top_10_cities[pollutant_column]) if value <= 0]
    
    # Assert that there are no invalid cities
    assert not invalid_cities, f"Test failed: Invalid {pollutant_column} values found in top 10 cities: {invalid_cities}"

    # Print the top 10 cities for verification (optional)
    print(f"Top 10 cities with highest {pollutant_column} concentration: {top_10_cities_list}")

    # If all assertions pass, the test is considered successful
    assert True, f"Test passed: Top 10 cities with highest {pollutant_column} concentration are correct."