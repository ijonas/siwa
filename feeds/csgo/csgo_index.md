# CS:GO Index Construction

### tl;dr
1. Restrict data to items that have many listings and are frequently traded
2. Determine the value of each item
3. Sum the value of all items to obtain the index value
4. Adjust the value of items such that each item's percentage share in the index is within its upper and lower bounds
5. Once all the values are within their bounds, sum the values to obtain the final index value

## Detailed Methodology

### Data Source:
The source of data is the API provided by [csgoskins.gg](https://csgoskins.gg/). This platform aggregates data from various CS:GO items exchanges, providing a comprehensive overview of the market.

### Picking the right items for the index

In order to be robust, yet representative, the methodology relies on a set of criteria to select the items that will be included in the index. The criteria are as follows:

1. **Highly Traded**: The items in the index should be of interest to the market. Therefore, firstly, the index is limited to the top 5000 most traded items. The most traded item is the one that has the most number of unique minimum listing prices in the analysis period. By the same logic, the least traded items are those that have had the same minimum listing price throughout the year.
2. **Minimum Number of Listings**: For the robustness of the index, it is also desirable that the the selected items have a minimum number of listings. The current version of the index is restricted to items with at least 100 listings on all days of the analysis period. This ensures that the items are not too concentrated in the hands of a few traders.

### Determining the Value of Each Item

The value calculation follows a straightforward approach to capture the dollar amount of value represented by each item on the market.

#### Value Calculation:
The value for each item is derived using two key metrics from the API:

1. **Number of Listings**: This represents the total number listings across all exchanges tracked by csgoskins.gg. It essentially captures the supply of that item in the market.
2. **Minimum Price**: Among all the listings for an item, this is the lowest price at which the item is being offered. It reflects the most competitive price point for that item in the market.

The "value" for each item is then calculated as:
Value = Number of Listings * Minimum Price

The sum of all these "values" at a point in time, could be the index value for that point in time. However, to restrict manipulability and ensure robustness of the index over time, it is necessary to impose some constraints on the value of each item. This is explained in the next section.


### Capping item values between upper and lower bounds

For a clear understanding of this methodology, let's walk through an example using a simple index of 5 CS:GO items. The below tables show how the `value` of each item is changed so that its share in the total index falls within the pre-defined lower cap and upper cap percentage share.

The "Deviation From Cap" column shows each item's percentage contribution from its closest cap (either lower or upper). The goal of this methodology is to minimize this deviation for every item. Each iteration reduces the deviation, aligning the items' contributions more closely with their designated range.

**Initial State**:

| Value  | Percentage Contribution | Deviation From Cap | Lower Cap Percentage | Upper Cap Percentage |
|--------|-------------------------|--------------------|----------------------|----------------------|
| 1000   | 91.74%                  | 76.74%             | 10%                  | 15%                  |
| 20     | 1.83%                   | -13.17%            | 15%                  | 25%                  |
| 20     | 1.83%                   | -15.17%            | 17%                  | 23%                  |
| 20     | 1.83%                   | -17.17%            | 19%                  | 25%                  |
| 30     | 2.75%                   | -22.25%            | 25%                  | 35%                  |


**Index Value**: 1090

**First Iteration**:

| Value      | Percentage Contribution | Deviation From Cap | Lower Cap Percentage | Upper Cap Percentage |
|------------|-------------------------|--------------------|----------------------|----------------------|
| 15.882     | 15.00%                  | 0.00%              | 10%                  | 15%                  |
| 20         | 18.89%                  | 0.00%              | 15%                  | 25%                  |
| 20         | 18.89%                  | 0.00%              | 17%                  | 23%                  |
| 20         | 18.89%                  | -0.11%             | 19%                  | 25%                  |
| 30         | 28.33%                  | 0.00%              | 25%                  | 35%                  |

**Index Value**: 105.882

**Final Iteration**:

| Value      | Percentage Contribution | Deviation From Cap | Lower Cap Percentage | Upper Cap Percentage |
|------------|-------------------------|--------------------|----------------------|----------------------|
| 15.882     | 14.98%                  | 0.00%              | 10%                  | 15%                  |
| 20         | 18.86%                  | 0.00%              | 15%                  | 25%                  |
| 20         | 18.86%                  | 0.00%              | 17%                  | 23%                  |
| 20.145     | 19.00%                  | 0.00%              | 19%                  | 25%                  |
| 30         | 28.29%                  | 0.00%              | 25%                  | 35%                  |

**Index Value**: 106.027

The final index value is the sum of the values of all the items in the index. In this case, it is 106.027.