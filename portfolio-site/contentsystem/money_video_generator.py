"""
Specialized script generator for viral money-making content.
This script creates optimized content specifically for videos about making money online.
"""

from viral_techniques import ViralTechniques
from platform_optimizer import PlatformOptimizer
from money_content_templates import MoneyContentTemplates
import os
import random

class MoneyContentGenerator:
    def __init__(self, api_key: str):
        """Initialize the generator with necessary components."""
        self.api_key = api_key
        self.techniques = ViralTechniques()
        self.optimizer = PlatformOptimizer()
        self.templates = MoneyContentTemplates()

    def generate_hook(self, method: str, amount: str, timeframe: str) -> str:
        """Generate an attention-grabbing hook."""
        hook_templates = self.templates.get_hook_templates()
        hook_type = random.choice(list(hook_templates.keys()))
        hook_template = random.choice(hook_templates[hook_type])
        return hook_template.format(method=method, amount=amount, timeframe=timeframe)

    def generate_script(self, method: str, amount: str, timeframe: str, duration: str = "short") -> dict:
        """Generate a complete video script."""
        structure = self.templates.get_script_structures()
        script_type = "short_form" if duration == "short" else "long_form"
        
        # Get enhancers and triggers
        enhancers = self.templates.get_content_enhancers()
        triggers = self.templates.get_psychological_triggers()
        credibility = self.templates.get_credibility_builders()
        objection_handlers = self.templates.get_objection_handlers()
        
        # Build the script
        script = {
            "title": self._generate_titles(method, amount, timeframe),
            "hook": self.generate_hook(method, amount, timeframe),
            "structure": structure[script_type],
            "visual_elements": random.sample(enhancers["visual_elements"], 3),
            "psychological_triggers": {
                k: random.choice(v) for k, v in triggers.items()
            },
            "credibility_elements": random.sample(credibility, 3),
            "objection_handling": {
                k: random.choice(v) for k, v in objection_handlers.items()
            },
            "cta": self._generate_cta(method),
            "descriptions": self._generate_descriptions(method, amount, timeframe)
        }
        
        return script

    def _generate_titles(self, method: str, amount: str, timeframe: str) -> dict:
        """Generate platform-specific titles."""
        title_templates = self.templates.get_title_templates()
        titles = {}
        for platform, templates in title_templates.items():
            titles[platform] = random.choice(templates).format(
                method=method, amount=amount, timeframe=timeframe
            )
        return titles

    def _generate_cta(self, method: str) -> str:
        """Generate a call-to-action."""
        cta_templates = self.templates.get_cta_templates()
        return random.choice(cta_templates).format(method=method)

    def _generate_descriptions(self, method: str, amount: str, timeframe: str) -> dict:
        """Generate platform-specific descriptions."""
        desc_templates = self.templates.get_description_templates()
        descriptions = {}
        for platform, template in desc_templates.items():
            descriptions[platform] = template.format(
                method=method, amount=amount, timeframe=timeframe
            )
        return descriptions

    def generate_money_content(self, method: str = "AI Tools", 
                             amount: str = "$1,000", 
                             timeframe: str = "Week",
                             duration: str = "short") -> str:
        """Generate complete viral content about making money online."""
        
        # Generate the complete script
        script = self.generate_script(method, amount, timeframe, duration)
        
        # Format the content for presentation
        content = f"""
=== Viral Money-Making Content Strategy ===

📱 PLATFORM-SPECIFIC TITLES
TikTok: {script['title']['tiktok']}
YouTube: {script['title']['youtube']}
Instagram: {script['title']['instagram']}

🎯 HOOK
{script['hook']}

📝 SCRIPT STRUCTURE
"""
        # Add script structure
        for section, timing in script['structure'].items():
            content += f"{section.upper()}: {timing}\n"

        content += f"""
🎬 VISUAL ELEMENTS TO INCLUDE
""" + "\n".join(f"- {element}" for element in script['visual_elements'])

        content += f"""

💡 PSYCHOLOGICAL TRIGGERS
""" + "\n".join(f"- {k.upper()}: {v}" for k, v in script['psychological_triggers'].items())

        content += f"""

🎯 CREDIBILITY BUILDERS
""" + "\n".join(f"- {element}" for element in script['credibility_elements'])

        content += f"""

❓ OBJECTION HANDLING
""" + "\n".join(f"- {k.upper()}: {v}" for k, v in script['objection_handling'].items())

        content += f"""

📢 CALL TO ACTION
{script['cta']}

📋 PLATFORM-SPECIFIC DESCRIPTIONS

=== TikTok ===
{script['descriptions']['tiktok']}

=== YouTube ===
{script['descriptions']['youtube']}

=== Instagram ===
{script['descriptions']['instagram']}
"""

        return content

if __name__ == "__main__":
    # Example usage
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: Please set GROQ_API_KEY environment variable")
    else:
        generator = MoneyContentGenerator(api_key)
        content = generator.generate_money_content(
            method="AI Tools",
            amount="$5,000",
            timeframe="Week",
            duration="short"
        )
        print(content)
