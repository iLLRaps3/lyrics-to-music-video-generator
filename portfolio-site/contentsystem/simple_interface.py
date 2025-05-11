"""
Simple and reliable interface for the viral money content generator.
"""

import gradio as gr
from money_video_generator import MoneyContentGenerator
import os
from database_manager import ContentDatabaseManager
from credit_manager import CreditManager

db_manager = ContentDatabaseManager()
credit_manager = CreditManager()

def check_credits(username, feature, cost):
    return credit_manager.check_credits(username, feature, cost)

def deduct_credits(username, feature, cost):
    credit_manager.deduct_credits(username, feature, cost)

def generate_content(username, method, amount, timeframe, duration, platform):
    """Generate viral money-making content with credit check."""
    try:
        # Check credits for content generation feature
        cost = 1  # Define cost per content generation
        has_credits, error = check_credits(username, 'content_generation', cost)
        if not has_credits:
            return error, "Insufficient credits"

        # Deduct credits before generation
        deduct_credits(username, 'content_generation', cost)

        # Initialize generator
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "Error: Please set GROQ_API_KEY environment variable", ""
            
        generator = MoneyContentGenerator(api_key)
        
        # Generate content
        content = generator.generate_money_content(
            method=method,
            amount=amount,
            timeframe=timeframe,
            duration=duration
        )
        
        return content, f"Content generated successfully for {platform}!"
    except Exception as e:
        return f"Error: {str(e)}", "Generation failed"

# Create a simple interface
demo = gr.Interface(
    fn=generate_content,
    inputs=[
        gr.Textbox(label="Username"),
        gr.Dropdown(
            choices=["AI Tools", "Freelancing", "Social Media Marketing", "Dropshipping"],
            label="Money-Making Method",
            value="AI Tools"
        ),
        gr.Textbox(label="Earnings Amount", value="$1,000"),
        gr.Dropdown(
            choices=["Day", "Week", "Month"],
            label="Timeframe",
            value="Week"
        ),
        gr.Radio(
            choices=["short", "long"],
            label="Content Duration",
            value="short"
        ),
        gr.Radio(
            choices=["TikTok", "YouTube", "Instagram"],
            label="Platform",
            value="TikTok"
        )
    ],
    outputs=[
        gr.Textbox(label="Generated Content", lines=10),
        gr.Textbox(label="Status")
    ],
    title="💰 Viral Money Content Generator",
    description="Create viral content about making money online",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="orange",
        neutral_hue="slate",
        text_size=gr.themes.sizes.text_lg,
    ),
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch(share=True)
