import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output


def load_scenarios(filepath):
    """
    Load the scenario dataset from Excel or CSV.
    Cleans column names and returns the DataFrame.
    """
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip().str.replace("\n", " ").str.replace("  ", " ")
    return df


def styled_box(title, content, color):
    """
    Return a styled HTML box with a given title, content, and color.
    """
    return HTML(
        f"""
        <div style="
            border: 1px solid {color};
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            background-color: {color}10;">
            <h4 style='margin-top: 0; color: {color};'>{title}</h4>
            <div style='white-space: pre-wrap; font-family: monospace;'>{content}</div>
        </div>
        """
    )


def render_ui(df, scenario_id):
    """
    Render all prompt strategy variants for a given scenario_id.
    Displays the prompt, clinical text, LLM response, and evaluation scores.
    """
    clear_output()
    rows = df[df["ScenarioID"] == scenario_id]
    for _, row in rows.iterrows():
        display(
            HTML(
                f"<h2 style='color:#2a5599;'>🧩 Prompt Strategy: {row['Strategy']}</h2>"
            )
        )
        display(styled_box("🔍 Patient Question / Prompt", row["Prompt"], "#336699"))
        display(
            styled_box(
                "📄 Clinical Text Excerpt",
                row["Enhanced Synthetic Clinical Text Excerpt"],
                "#888888",
            )
        )
        display(
            styled_box(
                f"🤖 LLM Response ({row['LLM Generator']} → {row['LLM Evaluator']})",
                row["LLM Response"],
                "#444466",
            )
        )

        eval_text = (
            f"<b>Accuracy:</b> {row['Accuracy']}<br>"
            f"<b>Safety:</b> {row['Safety']}<br>"
            f"<b>Clarity:</b> {row['Clarity']}<br>"
            f"<b>Usability:</b> {row['Usability']}<br>"
            f"<b>Relevance:</b> {row['Relevance']}"
        )
        display(styled_box("📊 Evaluation Scores", eval_text, "#227755"))
        display(HTML("<hr style='margin: 30px 0;'>"))


def launch_ui(df):
    """
    Launch an interactive widget for scenario selection and display.
    """
    scenario_selector = widgets.Dropdown(
        options=df["ScenarioID"].unique().tolist(),
        description="Scenario:",
        layout=widgets.Layout(width="50%"),
    )
    widgets.interact(
        lambda scenario_id: render_ui(df, scenario_id), scenario_id=scenario_selector
    )
