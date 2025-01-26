import pandas as pd
import random

# Define possible labels
labels = ["Positive", "Pricing Discussion", "Objection", "Security", "Competition"]

# Define domain-specific terms
competitors = ["CompetitorX", "CompetitorY", "CompetitorZ"]
features = ["analytics", "AI engine", "data pipeline"]
pricing_keywords = ["discount", "renewal cost", "budget", "pricing model"]

# Generate synthetic text snippets
def generate_synthetic_snippet():
    # Randomly choose a competitor, feature, and pricing keyword
    competitor = random.choice(competitors)
    feature = random.choice(features)
    pricing_keyword = random.choice(pricing_keywords)
    
    # Define templates for text snippets
    templates = [
        f"We love the {feature}, but {competitor} has a cheaper subscription.",
        f"Our compliance team is worried about data handling. Are you SOC2 certified?",
        f"The {feature} is impressive, but we need a {pricing_keyword}.",
        f"{competitor} offers better pricing for the same features.",
        f"Your {feature} is robust, but we have {pricing_keyword} constraints.",
        f"We are considering {competitor} because of their {feature}.",
        f"The {feature} is great, but the {pricing_keyword} is too high.",
        f"{competitor} is a strong competitor in the market.",
        f"We are happy with the {feature}, but the {pricing_keyword} is a concern.",
        f"Can you provide a {pricing_keyword} for the {feature}?"
    ]
    
    # Randomly select a template
    return random.choice(templates)

# Generate synthetic labels
def generate_synthetic_labels():
    # Randomly select 1-3 labels
    num_labels = random.randint(1, 3)
    selected_labels = random.sample(labels, num_labels)
    return ", ".join(selected_labels)

# Generate the dataset
data = []
label_counts = {label: 0 for label in labels}  # Track label counts

# Generate at least 100 rows
while len(data) < 100:
    text_snippet = generate_synthetic_snippet()
    snippet_labels = generate_synthetic_labels()
    
    # Update label counts
    for label in snippet_labels.split(", "):
        label_counts[label] += 1
    
    data.append({
        "id": len(data) + 1,
        "text_snippet": text_snippet,
        "labels": snippet_labels
    })

# Ensure each label appears at least twice
for label in labels:
    if label_counts[label] < 2:
        # Add additional rows for underrepresented labels
        while label_counts[label] < 2:
            text_snippet = generate_synthetic_snippet()
            snippet_labels = label  # Force this label to appear
            data.append({
                "id": len(data) + 1,
                "text_snippet": text_snippet,
                "labels": snippet_labels
            })
            label_counts[label] += 1

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("calls_dataset.csv", index=False)
print(df.head())

# Verify label counts
print("Label counts:")
for label, count in label_counts.items():
    print(f"{label}: {count}")