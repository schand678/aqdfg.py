  # Average price per car make
st.subheader("Average Price by Car Make")
avg_price_by_make = df.groupby('make')['price'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
avg_price_by_make.plot(kind='bar', color='purple', ax=ax)
ax.set_title('Average Price by Car Make')
ax.set_xlabel('Car Make')
ax.set_ylabel('Average Price ($)')
st.pyplot(fig)

