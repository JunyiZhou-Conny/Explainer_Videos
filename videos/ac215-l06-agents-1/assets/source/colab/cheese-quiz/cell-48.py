# --- Fun Facts data ---
PAVLOS_FUN_FACTS = [
    "Mozzarella is the most consumed cheese in the U.S., largely due to pizza.",
    "Gruyère and Emmental are classics for fondue thanks to their smooth melt.",
    "Aging boosts sharpness; 12-month cheddar has nuttier, deeper flavors.",
    "High-moisture cheeses (young gouda, fontina, jack) melt especially evenly.",
    "Rind-on bries are edible; the rind adds mushroomy, earthy notes.",
    "Salt helps control moisture and rind formation during cheesemaking.",
    "Browned spots on grilled cheese = Maillard reaction (not caramelization).",
    "American slices are engineered to melt at lower temperatures.",
    "Fresh cheeses (ricotta, chèvre) soften but don’t stretch like mozzarella.",
    "Taleggio’s washed rind brings savory depth and melts well.",
]

def pavlos_fun_fact():
  return {
      "fact": random.choice(PAVLOS_FUN_FACTS),
      "generated_at": int(time.time())
  }

# ✅ Define a Tool
@function_tool(name_override="pavlos_fun_fact_tool")
async def pavlos_fun_fact_tool() -> dict:
  """Return one random fun fact from Pavlos about cheese. Call multiple times if you want several facts."""
  return pavlos_fun_fact()

# Test tool
print(pavlos_fun_fact())
print(pavlos_fun_fact())
print(pavlos_fun_fact())
