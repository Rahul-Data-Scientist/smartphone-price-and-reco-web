import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pickle
import pandas as pd

st.set_page_config(layout="wide")
st.title("Analytics and Insights")

with open("phones_with_image_path.pkl", "rb") as file:
    df = pickle.load(file)

total_phones = df.shape[0]
total_brands = df['brand'].nunique()
foldable_phones = df[df['foldable_display'] == 1].shape[0]
min_price = int(df['price'].min())
max_price = int(df['price'].max())
min_display_size = round(df['screen_size_inch'].min(), 1)
max_display_size = round(df['screen_size_inch'].max(), 1)
five_g_phones = df[df['has_5g'] == 1].shape[0]

price_range = f"Rs {min_price} - Rs {max_price}"
display_range = f"{min_display_size} inch - {max_display_size} inch"


col1, col2, col3 = st.columns(3)
col1.metric("Total Phones", total_phones)
col2.metric("Total Brands", total_brands)
col3.metric("Price Range", price_range)

col1, col2, col3 = st.columns(3)
col1.metric("Foldable Phones", foldable_phones)
col2.metric("5G Phones", five_g_phones)
col3.metric("Display Size Range", display_range)

st.header("Market and Brand Insights")
st.write()
st.write()
st.write()

# most popular smartphone brands
st.subheader("Number of Smartphones by Brand")
brands_grouped = df.groupby("brand")
brand_count_df = brands_grouped.size().sort_values(ascending = False).reset_index()
brand_count_df.columns = ['Brand', 'Count']
fig = px.bar(
    brand_count_df,
    x = 'Brand',
    y = 'Count',
    text = 'Count'
)
st.plotly_chart(fig, key = "popular brand")
st.markdown("#### Insights from the above chart")
st.markdown("Vivo, Realme, and Samsung lead the smartphone market in this dataset, each with over 400 models, "
            "indicating their strong presence and diverse offerings across price segments.")
st.markdown("Chinese brands like Vivo, Realme, Xiaomi, Oppo, and Tecno dominate the top rankings, reflecting "
            "their aggressive product strategy and popularity in emerging markets like India.")
st.markdown("Brands like Apple, Google, and Sony, despite global recognition, have relatively fewer "
            "entries (under 60), suggesting a focused or premium-only portfolio in contrast to volume-driven "
            "competitors.")
st.markdown("The presence of many low-volume brands (e.g., iKall, Doogee, Coolpad, etc.) suggests a fragmented tail "
            "in the market, with several niche or budget manufacturers contributing small shares.")
st.write("")
st.write("")

# top model by spec score
st.subheader("Top Model by Spec Score")
top_indices = brands_grouped['spec_score'].idxmax()
top_phones_df = (df.loc[top_indices][['brand', 'name', 'price', 'ram_gb', 'rom_gb', 'screen_size_inch', 'spec_score',
                                     'battery_capacity_mah', 'processor_brand', 'clock_speed']]
                 .reset_index(drop = True).set_index("brand"))
st.dataframe(top_phones_df)
st.write("")
st.write("")

# average rating by brand after filtering by average spec score
st.subheader('Average Rating by Brand')
avg_rating_df = df[df['spec_score'] > df['spec_score'].mean()].groupby("brand")['rating'].mean().sort_values(ascending = False).reset_index()
avg_rating_df['rating'] = avg_rating_df['rating'].round(2)
fig = px.bar(
    avg_rating_df,
    x = 'brand',
    y = 'rating',
    text = 'rating'
)
st.plotly_chart(fig, key = "avg rating spec")
st.markdown("#### Insights from the above chart")
st.markdown("Coolpad, Lenovo, and HTC lead in user satisfaction, each with average ratings above 4.5.")
st.markdown("Popular brands like Samsung, OnePlus, and Sony have slightly lower ratings (~4.3–4.34), indicating strong "
            "competition from lesser-known brands.")
st.markdown("Itel has the lowest average rating (4.1), suggesting possible concerns with quality or user experience.")
st.write("")
st.write("")

# brand comparison
st.subheader("Compare any two brands")
def compare_brands(brand1, brand2):
    brand1_df = brands_grouped.get_group(brand1).copy()
    brand2_df = brands_grouped.get_group(brand2).copy()
    brand1_df['price_to_performance'] = (1000 * brand1_df['spec_score']) / brand1_df['price']
    brand2_df['price_to_performance'] = (1000 * brand2_df['spec_score']) / brand2_df['price']

    total1 = brand1_df.shape[0]
    avg_price1 = "Rs " + str(brand1_df['price'].mean().round(2))
    avg_rating1 = brand1_df['rating'].mean().round(2)
    avg_spec_score1 = brand1_df['spec_score'].mean().round(2)
    most_expensive1 = brand1_df[brand1_df['price'] == brand1_df['price'].max()]['name'] + " (Rs " + str(brand1_df['price'].max()) + ")"
    most_expensive1 = most_expensive1.head(1).values[0]
    highest_spec_score1 = brand1_df[brand1_df['spec_score'] == brand1_df['spec_score'].max()]['name'] + " (Spec Score =  " + str(brand1_df['spec_score'].max()) + ")"
    highest_spec_score1 = highest_spec_score1.head(1).values[0]
    avg_price_to_performance_1 = brand1_df['price_to_performance'].mean().round(2)

    total2 = brand2_df.shape[0]
    avg_price2 = "Rs " + str(brand2_df['price'].mean().round(2))
    avg_rating2 = brand2_df['rating'].mean().round(2)
    avg_spec_score2 = brand2_df['spec_score'].mean().round(2)
    most_expensive2 = brand2_df[brand2_df['price'] == brand2_df['price'].max()]['name'] + " (Rs " + str(brand2_df['price'].max()) + ")"
    most_expensive2 = most_expensive2.head(1).values[0]
    highest_spec_score2 = brand2_df[brand2_df['spec_score'] == brand2_df['spec_score'].max()]['name'] + " (Spec Score =  " + str(brand2_df['spec_score'].max()) + ")"
    highest_spec_score2 = highest_spec_score2.head(1).values[0]
    avg_price_to_performance_2 = brand2_df['price_to_performance'].mean().round(2)

    comparison_df = pd.DataFrame({
        brand1 : [total1, avg_price1, avg_rating1, avg_spec_score1, most_expensive1, highest_spec_score1, avg_price_to_performance_1],
        brand2 : [total2, avg_price2, avg_rating2,  avg_spec_score2, most_expensive2, highest_spec_score2, avg_price_to_performance_2]
    },index=[
        "Total Models",
        "Average Price",
        "Average Rating",
        "Average Spec Score",
        "Most Expensive Model",
        "Highest Spec Score Model",
        "Average Price-to-Performance (per ₹1000)"
    ])
    return comparison_df


brand1 = st.selectbox("Select Brand 1", sorted(list(df['brand'].unique())))
brand2 = st.selectbox("Select Brand 2", sorted(list(df['brand'].unique())))
if st.button("Compare"):
    comp_df = compare_brands(brand1, brand2)
    st.dataframe(comp_df)
st.write("")
st.write("")


st.header("Feature Distribution and Trends")
st.write("")
st.write("")

# 4G vs 5G Smartphone Distribution
st.subheader('4G vs 5G Smartphone Distribution')
connectivity_df = df.groupby("has_5g").size().reset_index().set_index("has_5g")
connectivity_df.index = ['4G', '5G']
connectivity_df = connectivity_df.reset_index()
connectivity_df.columns = ['Network', 'Total Phones']
fig = px.pie(
    connectivity_df,
    values = 'Total Phones',
    names = 'Network',
)
st.plotly_chart(fig, key = "4gvs5g")
st.markdown("#### Insights from the above chart")
st.markdown("5G smartphones lead with a 53.7% share of the market.")
st.markdown("4G smartphones still hold a strong presence, making up 46.3% of the total.")
st.write("")
st.write("")


# foldable vs non foldable phones
st.subheader('Foldable vs Non-Foldable Smartphone Distribution')
foldable_dist_df = df.groupby("foldable_display").size().reset_index().set_index("foldable_display")
foldable_dist_df.index = ['Non-Foldable', 'Foldable']
foldable_dist_df = foldable_dist_df.reset_index()
foldable_dist_df.columns = ['Foldability', 'Total Phones']
fig = px.pie(
    foldable_dist_df,
    values = 'Total Phones',
    names = 'Foldability'
)
st.plotly_chart(fig, key = "foldablevsnon-foldable")

st.markdown("#### Insights from the above chart")
st.markdown("Non-foldable smartphones dominate the market with a huge 97.3% share.")
st.markdown("Foldable phones are very rare, making up only 2.66% of the total.")
st.write("")
st.write("")

# Battery Capacity Comparison: 5G vs Non-5G Smartphones
st.subheader("Battery Capacity Comparison: 5G vs Non-5G Smartphones (Outliers Removed)")
# filtering out extreme outliers
filtered_df = df[df['battery_capacity_mah'] <= 10000]
fig = px.box(
    filtered_df,
    x = 'battery_capacity_mah',
    color = 'has_5g',
    labels = {"has_5g" : "5G Support", "battery_capacity_mah" : "Battery Capacity (mAh)"}
)
st.plotly_chart(fig, key = "battery_comparison")

st.markdown("#### Insights from the above plot")
st.markdown("Non-5G smartphones generally have a wider range and higher median battery capacity compared to 5G phones.")
st.markdown("5G phones tend to cluster around 5000 mAh, indicating more standardization.")
st.markdown("Outliers are more frequent in non-5G models, including phones with very high battery capacities "
            "(7000–10000 mAh).")
st.write("")
st.write("")

# Display Refresh Rate Distribution by Display Type
st.subheader('Display Refresh Rate Distribution by Display Type')
temp_df = df[df['screen_type'] != 'OTHER']
fig = px.histogram(
    temp_df,
    x = 'screen_type',
    color = 'display_refresh_rate',
    category_orders = {"display_refresh_rate" : sorted(temp_df['display_refresh_rate'].unique())},
    labels = {"screen_type" : "Display Type", "display_refresh_rate" : "Refresh Rate (Hz)"},
    barmode = 'stack'
)
st.plotly_chart(fig, key = "display_refresh_rate_dist")
st.markdown("#### Insights from the above plot")
st.markdown("LCD displays are the most common and are primarily paired with 90Hz and 120Hz refresh rates, 90Hz being "
            "the most dominant.")
st.markdown("AMOLED and Super AMOLED displays are heavily dominated by 120Hz, indicating a strong preference for "
            "smoother visuals in these premium screens.")
st.markdown("While higher refresh rates like 144Hz, 165Hz, and even 240Hz are present, they are relatively rare and "
            "mainly appear with AMOLED/OLED panels.")
st.markdown("OLED displays are the least common but still support a variety of refresh rates, showcasing their "
            "high-end nature.")
st.write("")
st.write("")

# battery capacity vs fast charging watt
st.subheader("Relation between Battery Capacity and Fast Charging Watt")
fig = px.scatter(
    df[df['battery_capacity_mah'] <= 10000],
    x = 'battery_capacity_mah',
    y = 'fast_charging_watt'
)
st.plotly_chart(fig, key = "battery_charging_watt")
st.markdown("#### Insights from the above plot")
st.markdown("No Strong Correlation Between Battery Size and Fast Charging Wattage.")
st.markdown("Our analysis shows that smartphones with similar battery capacities can have drastically different "
            "fast charging speeds.")
st.markdown("This suggests that fast charging capability is not directly dependent on battery size, but likely "
            "influenced by brand priorities, price segments, or internal hardware limits.")
st.write("")
st.write("")


st.header("Price Analysis & Comparisons")
st.write("")
st.write("")

# price vs spec score
st.subheader("Price vs Spec Score")
fig = px.scatter(
    df,
    x = 'price',
    y = 'spec_score'
)
st.plotly_chart(fig, key = "price_vs_spec")
st.markdown("#### Insights from the above plot")
st.markdown("Under ₹30,000, there's no strong correlation between price and spec score — some budget phones offer "
            "great value, while others underperform for their price.")
st.markdown("Spec score increases quickly as price increases from low to mid-range (up to ₹50,000), showing that "
            "spending more gives you better overall features early on.")
st.markdown("After a point (around ₹50,000+), the spec score starts to level off, meaning paying more doesn't "
            "always give much better features.")
st.markdown("Most smartphones with very high prices (₹100K+) have scores between 90–100, but some cheaper phones "
            "also reach high scores, showing there are value-for-money options.")
st.markdown("A few phones have lower spec scores despite high prices, which could be older models or phones with "
            "niche features not captured by spec_score.")
st.write("")
st.write("")

# Average price by processor brand
st.subheader("Average Price by Processor Brand")
avg_price_processor_df = df.groupby("processor_brand")['price'].mean().reset_index()
avg_price_processor_df['price'] = avg_price_processor_df['price'].round(2)
fig = px.bar(
    avg_price_processor_df,
    x = 'processor_brand',
    y = 'price',
    text = 'price',
    labels = {"processor_brand" : "Processor Brand", "price" : "Average price (Rs)"}
)
st.plotly_chart(fig, key = 'price_vs_processor_brand')
st.markdown("#### Insights from the above chart")
st.markdown("Bionic and Tensor processors are used in the most expensive phones on average.")
st.markdown("Snapdragon and Kirin phones are mid-range in price.")
st.markdown("Helio, Unisoc, and Mediatek are found in budget phones.")
st.markdown("There’s a big price gap between Bionic and most other processors as bionic processors are used in iPhones "
            "which are known for their high cost.")
st.write("")
st.write("")

# price range distribution
st.subheader("Smartphone Price Range Distribution")
bins = [0, 10000, 20000, 30000, 40000, 50000, float('inf')]
labels = ["<10k", "10k-20k", "20k-30k", "30k-40k", "40k-50k", ">50k"]
df['price_range'] = pd.cut(df['price'], bins = bins, labels = labels, right = False)
price_counts = df['price_range'].value_counts().sort_index()
fig = px.bar(
    x = price_counts.index,
    y = price_counts.values,
    text = price_counts.values,
    labels = {'x' : "Price Range", 'y' : "Number of Phones"}
)
st.plotly_chart(fig, key = 'price_dist')
st.markdown("#### Insights from the above chart")
st.markdown("Most phones fall in the 10k–20k price range.")
st.markdown("20k–30k and <10k ranges have a similar number of phones.")
st.markdown("Very few phones are priced between 30k–50k.")
st.markdown("Surprisingly, >50k has more phones than the 30k–50k range.")
st.write("")
st.write("")

# Average Price by Display Type
st.subheader("Average Price by Display Type")
screen_price_df = df.groupby("screen_type")['price'].mean().reset_index()
screen_price_df['price'] = screen_price_df['price'].round(2)
fig = px.bar(
    screen_price_df,
    x = 'screen_type',
    y = 'price',
    text = 'price',
    labels = {"screen_type" : "Display Type", "price" : "Average Price (Rs)"}
)
st.plotly_chart(fig, key = 'avg_price_display')
st.markdown("#### Insights from the above chart")
st.markdown("OLED phones are the most expensive on average.")
st.markdown("LCD phones have the lowest average price.")
st.markdown("AMOLED and Super AMOLED phones cost more than LCD but less than OLED.")
st.markdown("Other display types fall in the mid-price range.")
st.write("")
st.write("")

# price vs battery_capacity
st.subheader("Relation between Price and battery Capacity")
fig = px.scatter(
    df,
    x = 'battery_capacity_mah',
    y = 'price'
)
st.plotly_chart(fig, key = 'price_battery_capacity_relation')
st.markdown("#### Insights from the above plot")
st.markdown("Most smartphones have battery capacities between 3000 and 7000 mAh.")
st.markdown("There's no clear link between higher battery capacity and higher price.")
st.markdown("Some low-priced phones even offer very high battery capacities (above 10,000 mAh).")
st.markdown("Premium phones often focus on other features instead of just battery size.")
st.write("")
st.write("")

# Average Price by RAM
st.subheader("Average Price by RAM Capacity")
ram_price_df = df.groupby("ram_gb")['price'].mean().reset_index()
ram_price_df['price'] = ram_price_df['price'].round(2)
fig = px.bar(
    ram_price_df,
    x = 'ram_gb',
    y = 'price',
    text = 'price',
    labels = {"ram_gb" : "RAM (GB)", "price" : "Average Price (Rs)"}
)
fig.update_xaxes(type='category')
st.plotly_chart(fig, key = 'avg_price_ram_capacity')
st.markdown("#### Insights from the above chart")
st.markdown("Average price increases steadily with higher RAM.")
st.markdown("Phones with 16 GB RAM are the most expensive on average.")
st.markdown("There's a sharp price jump from 8 GB to 12 GB RAM.")
st.markdown("Budget phones typically have 2–4 GB RAM.")
st.write("")
st.write("")

# Average Price by ROM
st.subheader("Average Price by ROM Capacity")
rom_price_df = df.groupby("rom_gb")['price'].mean().reset_index()
rom_price_df['price'] = rom_price_df['price'].round(2)
fig = px.bar(
    rom_price_df,
    x = 'rom_gb',
    y = 'price',
    text = 'price',
    labels = {"rom_gb" : "ROM (GB)", "price" : "Average Price (Rs)"}
)
fig.update_xaxes(type='category')
st.plotly_chart(fig, key = 'avg_price_rom_capacity')
st.markdown("#### Insights from the above chart")
st.markdown("Higher ROM (storage) clearly leads to higher phone prices.")
st.markdown("Prices rise sharply from 256 GB onward, especially at 512 GB and 1 TB.")
st.markdown("Phones with 16–64 GB ROM fall into the budget category.")
st.markdown("1 TB phones are rare and highly premium.")
st.write("")
st.write("")

# Average Price by Network Type
st.subheader('Average Price by Network Type')
temp_df = df.groupby("has_5g")['price'].mean().reset_index().set_index("has_5g")
temp_df['price'] = temp_df['price'].round(2)
temp_df.index = ['Non-5G', '5G']
temp_df = temp_df.reset_index()
temp_df.columns = ['Network', 'Average Price (Rs)']
fig = px.bar(
    temp_df,
    x = 'Network',
    y = 'Average Price (Rs)',
    text = 'Average Price (Rs)'
)
st.plotly_chart(fig, key = 'avg_price_network')
st.markdown("#### Insights from the above chart")
st.markdown("5G phones are significantly more expensive, with an average price of ₹36,528 compared to "
            "₹14,059 for non-5G phones.")
st.markdown("Network type is a strong indicator of pricing tier — 5G support clearly aligns with premium devices.")
st.write("")
st.write("")


st.header("Camera, RAM and Processor Core Insights")
st.write("")
st.write("")

# Distribution of Rear vs Front Primary Camera Megapixels
st.subheader("Distribution of Rear vs Front Primary Camera Megapixels")
fig = px.box(
    df.melt(value_vars = ['rear_primary_mp', 'front_primary_mp'], var_name = "Camera Type", value_name = "Megapixels"),
    x = "Megapixels",
    y = "Camera Type",
    labels = {"Megapixels" : "Megapixels (MP)", "Camera Type" : "Camera"}
)
st.plotly_chart(fig, key = 'rear_front_dist')
st.markdown("#### Insights from the above plot")
st.markdown("Rear cameras generally have much higher megapixels than front cameras.")
st.markdown("Most front cameras are between 8–32 MP, while rear cameras range wider, up to 200 MP.")
st.markdown("A few phones have extremely high rear camera megapixels, acting as outliers.")
st.markdown("Front camera specs are more consistent across phones than rear cameras.")
st.write("")
st.write("")

# RAM/ROM Configurations Popularity
st.subheader("Top 10 RAM+ROM Configurations Popularity")
df["ram_rom_combo"] = df['ram_gb'].astype(str) + "GB" + "+" + df['rom_gb'].astype(str) + "GB"
combo_counts = df['ram_rom_combo'].value_counts().head(10).reset_index()
fig = px.bar(
    combo_counts,
    x = 'ram_rom_combo',
    y = 'count',
    text = 'count',
    labels = {"ram_rom_combo" : "RAM+ROM Configurations", "count" : "Number of Phones"}
)
st.plotly_chart(fig, key = 'ram_rom_pop')
st.markdown("#### Insights from the above chart")
st.markdown("The most popular configuration is 8GB RAM + 128GB ROM, widely used across devices.")
st.markdown("Mid-range setups like 6GB/128GB and 4GB/64GB are also very common.")
st.markdown("High-end combos (12GB+256GB) are popular but less frequent.")
st.markdown("Entry-level configs like 2GB/32GB appear rarely in the dataset.")
st.write("")
st.write("")

#  Number of Rear Cameras vs. Front Cameras
st.subheader('Rear vs Front Camera Count Combinations')
temp_df = df.copy()
temp_df['num_rear_cameras'] = temp_df['num_rear_cameras'].astype(int).astype(str)
temp_df['num_front_cameras'] = temp_df['num_front_cameras'].astype(int).astype(str)

camera_combo = temp_df.groupby(['num_rear_cameras', 'num_front_cameras']).size().reset_index(name = 'count')

fig = px.density_heatmap(
    camera_combo,
    x = 'num_rear_cameras',
    y = 'num_front_cameras',
    z = 'count',
    color_continuous_scale = 'Blues',
    text_auto = True,
    labels = {"num_rear_cameras" : "Rear Cameras", "num_front_cameras" : "Front Cameras"}
)
st.plotly_chart(fig, key = 'rear_front_count_combo')
st.markdown("#### Insights from the above heatmap")
st.markdown("Most smartphones have 1 front camera paired with 2 or 3 rear cameras.")
st.markdown("Very few devices offer dual front cameras..")
st.markdown("Having 4 rear cameras is less common but still notable.")
st.markdown("Phones with 0 front cameras are rare in the dataset.")
st.write("")
st.write("")

processor_count = df.groupby("processor_core").size().reset_index(name = "count")
st.subheader("Processor Core Distribution")
fig = px.pie(
    processor_count,
    values = "count",
    names = "processor_core"
)
st.plotly_chart(fig, key = 'processor_core_distribution')
st.markdown("#### Insights from the above chart")
st.markdown("Octa-core processors dominate the market, powering 94.4% of the phones.")
st.markdown("Other core types (quad, hexa, nine) are extremely rare, together making up just 5.6%.")
st.write("")
st.write("")

# Average clock speed by processor core
st.subheader("Average Clock Speed by Processor Core")
processor_clock_df = df.groupby("processor_core")['clock_speed'].mean().reset_index()
processor_clock_df['clock_speed'] = processor_clock_df['clock_speed'].round(2)
fig = px.bar(
    processor_clock_df,
    x = 'processor_core',
    y = 'clock_speed',
    text = 'clock_speed',
    labels = {"processor_core" : "Processor Core", "clock_speed" : "Clock Speed (GHz)"}
)
st.plotly_chart(fig, key = 'avg_clock_processor_core')
st.markdown("#### Insights from the above chart")
st.markdown("Hexa-core processors have the highest average clock speed at 3.28 GHz.")
st.markdown("Octa-core and nine-core are slower than Hexa-core at 2.4 GHz and 3.0 GHz, respectively.")
st.markdown("Quad-core chips are the slowest, averaging 1.68 GHz.")
st.markdown("More cores don’t always mean higher speed.")
st.write("")
st.write("")


# Correlation Heatmap
st.header("Correlation Heatmap")
# Compute correlation matrix
corr_matrix = df.corr(numeric_only = True).round(2)

fig = go.Figure(data = go.Heatmap(
    x = corr_matrix.columns,
    y = corr_matrix.columns,
    z = corr_matrix.values,
    zmin = -1,
    zmax = 1,
    colorscale = 'RdBu_r',
    colorbar_title = 'Correlation',
    text = corr_matrix.values,
    texttemplate = "%{text}",
    hovertemplate = "Correlation between %{y} and %{x} : %{z}"
))

fig.update_layout(
    title = 'Correlation Heatmap',
    xaxis_tickangle = 45,
    width = 800,
    height = 800
)
st.plotly_chart(fig, key = 'corr_heatmap')

st.markdown("#### Insights from the above heatmap")
st.markdown("Price is positively correlated with spec score (0.59), RAM (0.61), and ROM (0.65) — better hardware "
            "strongly influences phone pricing.")
st.markdown("Clock speed also has strong positive correlation with spec score (0.73) and RAM (0.68) — faster "
            "processors often come with more RAM and better overall specs.")
st.markdown("Expandable memory support has a negative correlation with price (-0.51) — higher-end phones are "
            "less likely to support expandable storage.")
st.markdown("Spec score is a reliable summary metric — it correlates well with most performance indicators "
            "like RAM, ROM, clock speed, and even fast charging.")
st.markdown("Front and rear camera megapixels have very weak correlation with price — camera resolution "
            "alone doesn’t drive phone pricing.")



