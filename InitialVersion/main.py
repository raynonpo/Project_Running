import pandas as pd
from agent.Analyst import DataAnalyst
from agent.Predictor import IndependentLapPredictor
from agent.Coach import PerformanceCoach
from agent.LLM import OllamaGarminAgent


def load_database():
    try:
        return pd.read_csv("data/raw_activities.csv")
    except FileNotFoundError:
        # Fallback to sample data if not found
        mock_data = {
            'activity_id': [1, 2, 3, 4, 5],
            'type': ['Easy Run', 'Intervals', 'Long Run', 'Easy Run', 'Race'],
            'distance_km': [5.0, 8.0, 12.0, 5.2, 10.0],
            'pace_min_km': [6.0, 5.15, 6.30, 5.95, 4.90],
            'heart_rate_bpm': [142, 168, 145, 140, 172],
            'cadence_rpm': [168, 174, 166, 169, 178]
        }
        return pd.DataFrame(mock_data)


def main():
    df = load_database()

    # 1. Compile all analytical facts first using our Python back-end
    analyst = DataAnalyst(df)
    predictor = IndependentLapPredictor(df)
    coach = PerformanceCoach(df)

    # Bundle data insights together to feed into the LLM context layer
    data_context = {
        "overall_highlights": analyst.get_overall_highlights().to_dict(),
        "categorical_counts": analyst.get_categorical_unique_counts(),
        "data_schema_summary": analyst.get_data_summary(),
        "predicted_10k_baseline": predictor.predict_next_run(10.0),  # standard baseline prediction
        "preliminary_coaching_insights": coach.generate_suggestions()
    }

    # 2. Initialize the Ollama Agent
    # Change "llama3" to "mistral", "phi3", etc., depending on what you have pulled
    agent = OllamaGarminAgent(model_name="llama3")

    print("=== 🤖 OLLAMA-POWERED GARMIN AGENT ONLINE ===")
    print("Ask me anything about your training, metrics summaries, predictions, or pacing adjustments.")
    print("Type 'exit' to quit.\n")
    print("💡 Example things to ask:")
    print(" - 'Can you summarize my data highlights and tell me how my cadence looks?'")
    print(" - 'Predict my finish time if I run an event of 15km next week.'")
    print(" - 'Give me 3 training suggestions based on my average heart rate.'\n")

    while True:
        user_query = input("You 🏃‍♂️: ").strip()
        if user_query.lower() in ['exit', 'quit']:
            print("Agent signing off!")
            break

        if not user_query:
            continue

        print("\nThinking... 🧠")
        # Ollama evaluates the query combining Python analytical backend execution with LLM reasoning
        ai_response = agent.chat_with_context(user_query, data_context)
        print(f"\nAgent 🤖:\n{ai_response}\n")
        print("-" * 50)


if __name__ == "__main__":
    main()
