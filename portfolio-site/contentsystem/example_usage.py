"""
Example usage of the Viral Content Creation System.
This script demonstrates various ways to use the system for different content types.
"""

import os
from main import ViralContentSystem
from database_manager import ContentDatabaseManager
from viral_techniques import ViralTechniques

def print_section(title):
    """Print a formatted section title."""
    print("\n" + "="*50)
    print(title)
    print("="*50 + "\n")

def example_short_form_content():
    """Example of creating short-form content (TikTok/Reels)."""
    print_section("Short-Form Content Example (TikTok/Reels)")
    
    topic = """
    Create a viral TikTok about 'How I Made $5000 in One Week with AI Tools'
    Target audience: Young entrepreneurs and tech enthusiasts
    Style: Educational with a hint of shock value
    """
    
    print("Input Topic:")
    print(topic)
    print("\nGenerating content strategy...")
    
    for response in content_system.process_content_request(topic):
        print("\nGenerated Strategy:")
        print(response)

def example_long_form_content():
    """Example of creating long-form content (YouTube)."""
    print_section("Long-Form Content Example (YouTube)")
    
    topic = """
    Create a 5-minute YouTube video about 'The Dark Side of Social Media Success'
    Target audience: Content creators and social media managers
    Style: Investigative and revealing
    Include: Expert insights and data points
    """
    
    print("Input Topic:")
    print(topic)
    print("\nGenerating content strategy...")
    
    for response in content_system.process_content_request(topic):
        print("\nGenerated Strategy:")
        print(response)

def example_educational_content():
    """Example of creating educational content."""
    print_section("Educational Content Example")
    
    topic = """
    Create a tutorial series on 'Mastering Python in 30 Days'
    Platform: Mixed (YouTube main content, TikTok/Reels for tips)
    Target audience: Beginner programmers
    Style: Step-by-step with practical examples
    """
    
    print("Input Topic:")
    print(topic)
    print("\nGenerating content strategy...")
    
    for response in content_system.process_content_request(topic):
        print("\nGenerated Strategy:")
        print(response)

def example_trending_topic():
    """Example of creating content around a trending topic."""
    print_section("Trending Topic Example")
    
    topic = """
    Create content about 'The Latest AI Tool Everyone's Talking About'
    Platforms: All (TikTok, YouTube, Instagram)
    Style: News/Commentary with demonstration
    Goal: Maximize viral potential while providing value
    """
    
    print("Input Topic:")
    print(topic)
    print("\nGenerating content strategy...")
    
    for response in content_system.process_content_request(topic):
        print("\nGenerated Strategy:")
        print(response)

def example_viral_techniques():
    """Demonstrate available viral techniques."""
    print_section("Available Viral Techniques")
    
    techniques = ViralTechniques()
    
    print("1. Hook Patterns:")
    for name, description in techniques.get_hook_patterns().items():
        print(f"- {name}: {description}")
    
    print("\n2. Pattern Interrupts:")
    for name, description in techniques.get_pattern_interrupts().items():
        print(f"- {name}: {description}")
    
    print("\n3. Platform Best Practices:")
    practices = techniques.get_platform_best_practices()
    for platform, details in practices.items():
        print(f"\n{platform.upper()}:")
        for category, items in details.items():
            print(f"  {category}:")
            for item in items:
                print(f"    - {item}")

def main():
    """Run all examples."""
    # Check for API key
    if not os.getenv("GROQ_API_KEY"):
        print("Error: Please set your GROQ_API_KEY environment variable first.")
        return

    global content_system
    content_system = ViralContentSystem(os.getenv("GROQ_API_KEY"))

    print_section("Viral Content Creation System Examples")
    print("This script will demonstrate various ways to use the system.")
    print("Each example will generate a complete content strategy.")
    
    # Run examples
    example_short_form_content()
    example_long_form_content()
    example_educational_content()
    example_trending_topic()
    example_viral_techniques()

    print_section("Examples Complete")
    print("""
Tips for Best Results:
1. Be specific about your target audience
2. Include desired style and tone
3. Specify any particular techniques or approaches you want to use
4. Mention any specific platform requirements
5. Include any relevant trending topics or hashtags

For more examples and documentation, refer to the README.md file.
    """)

if __name__ == "__main__":
    main()
