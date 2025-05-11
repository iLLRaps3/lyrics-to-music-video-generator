"""
Modern, sleek interface for the viral money content generator.
Features a professional design with custom styling and interactive elements.
"""

import gradio as gr
from money_video_generator import MoneyContentGenerator
import os
from typing import Tuple, Dict
import json

# Custom CSS for a modern, sleek look
custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #1a1a1a, #2d2d2d) !important;
    font-family: 'Arial', sans-serif; /* Default font for the interface */
}

.gr-button {
    background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    font-family: 'Arial', sans-serif; /* Font for buttons */
}

.title {
    color: #00c6ff !important;
    text-align: center !important;
    font-size: 2.5em !important;
    margin: 20px !important;
    text-shadow: 0 2px 10px rgba(0,198,255,0.3) !important;
    font-family: 'Georgia', serif; /* Font for titles */
}


.gr-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(0,114,255,0.4) !important;
}

.gr-input, .gr-dropdown, .gr-radio {
    background: #1e1e1e !important;
    color: white !important;
    border: 2px solid #333 !important;
    border-radius: 10px !important;
}

.gr-form {
    background: #1e1e1e !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 10px !important;
}

.title {
    color: #00c6ff !important;
    text-align: center !important;
    font-size: 2.5em !important;
    margin: 20px !important;
    text-shadow: 0 2px 10px rgba(0,198,255,0.3) !important;
}

.output-text {
    background: #1e1e1e !important;
    color: white !important;
    padding: 15px !important;
    border-radius: 10px !important;
    font-family: 'Monaco', monospace !important;
    margin-top: 10px !important;
}

.tips {
    color: #00c6ff !important;
    font-size: 0.9em !important;
    margin: 20px !important;
    padding: 15px !important;
    background: rgba(0,0,0,0.2) !important;
    border-radius: 10px !important;
}
"""

def generate_content(
    method: str,
    amount: str,
    timeframe: str,
    duration: str,
    platform: str
) -> Tuple[str, str, str]:
    """Generate content and format it beautifully."""
    
    # Initialize the generator
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not set", "", "Error: Please set your API key"
        
    generator = MoneyContentGenerator(api_key)
    
    try:
        # Generate the content
        content = generator.generate_money_content(method, amount, timeframe, duration)
        
        # Parse the content into sections
        content_dict = {
            "hook": "",
            "script": "",
            "strategy": ""
        }
        
        sections = content.split("\n\n")
        for section in sections:
            if "HOOK" in section:
                content_dict["hook"] = section
            elif "SCRIPT STRUCTURE" in section:
                content_dict["script"] = section
            else:
                content_dict["strategy"] += section + "\n\n"

        # Format for specific platform
        platform_content = f"""
💰 {platform.upper()} CONTENT STRATEGY 💰

{content_dict['hook']}

📝 CONTENT STRUCTURE:
{content_dict['script']}

🎯 STRATEGY:
{content_dict['strategy']}
"""
        
        # Generate platform-specific elements
        titles = generator._generate_titles(method, amount, timeframe)
        descriptions = generator._generate_descriptions(method, amount, timeframe)
        
        platform = platform.lower()
        platform_specific = f"""
🎥 OPTIMIZED FOR {platform.upper()}:

📋 TITLE:
{titles[platform]}

📝 DESCRIPTION:
{descriptions[platform]}
"""
        
        # Save the strategy
        strategy_file = f"money_strategy_{method.lower().replace(' ', '_')}_{platform}.json"
        strategy_data = {
            "method": method,
            "amount": amount,
            "timeframe": timeframe,
            "platform": platform,
            "content": content_dict,
            "title": titles[platform],
            "description": descriptions[platform]
        }
        
        with open(strategy_file, 'w') as f:
            json.dump(strategy_data, f, indent=4)

        return platform_content, platform_specific, f"Strategy saved to {strategy_file}"
        
    except Exception as e:
        return f"Error generating content: {str(e)}", "", "Error occurred"

# Create the interface
with gr.Blocks(css=custom_css) as interface:
    gr.HTML("<h1 class='title'>💰 Viral Money Content Generator 💰</h1>")
    
    with gr.Row():
        with gr.Column():
            method = gr.Dropdown(
                choices=[
                    "AI Tools",
                    "Freelancing",
                    "Social Media Marketing",
                    "Dropshipping",
                    "Affiliate Marketing",
                    "Custom Method"
                ],
                label="Money-Making Method",
                value="AI Tools"
            )
            
            amount = gr.Textbox(
                label="Earnings Amount",
                placeholder="e.g., $1,000",
                value="$1,000"
            )
            
            timeframe = gr.Dropdown(
                choices=["Day", "Week", "Month", "Year"],
                label="Timeframe",
                value="Week"
            )
            
            duration = gr.Radio(
                choices=["short", "long"],
                label="Content Duration",
                value="short",
                info="Short: 30-60s, Long: 3-5min"
            )
            
            platform = gr.Radio(
                choices=["TikTok", "YouTube", "Instagram"],
                label="Target Platform",
                value="TikTok",
                info="Select your primary platform"
            )

            generate_btn = gr.Button(
                "Generate Viral Strategy 🚀",
                variant="primary"
            )

    with gr.Row():
        content_output = gr.Textbox(
            label="Content Strategy",
            lines=15,
            elem_classes=["output-text"]
        )
        
        platform_output = gr.Textbox(
            label="Platform Optimization",
            lines=15,
            elem_classes=["output-text"]
        )

    save_status = gr.Textbox(
        label="Save Status",
        lines=1
    )

    # Connect the interface
    generate_btn.click(
        generate_content,
        inputs=[method, amount, timeframe, duration, platform],
        outputs=[content_output, platform_output, save_status]
    )

    gr.HTML("""
        <div class='tips'>
            <h3>🎯 Tips for Best Results</h3>
            <ol>
                <li>Be specific with your method</li>
                <li>Use realistic earnings</li>
                <li>Include proof elements</li>
                <li>Focus on value delivery</li>
            </ol>
            
            <h3>💡 Need Help?</h3>
            <p>Check MONEY_CONTENT_GUIDE.md for detailed instructions</p>
        </div>
    """)

# Launch the interface
if __name__ == "__main__":
    interface.launch(
        share=True,
        debug=True
    )
