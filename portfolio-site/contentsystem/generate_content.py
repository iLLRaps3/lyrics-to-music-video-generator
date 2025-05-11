"""
Command-line interface for generating viral money-making content.
"""

from money_video_generator import MoneyContentGenerator
import os
import json
from datetime import datetime

def main():
    print("\n=== 💰 Viral Money Content Generator 💰 ===\n")
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: Please set your GROQ_API_KEY environment variable first.")
        return

    # Initialize generator
    generator = MoneyContentGenerator(api_key)
    
    # Get user inputs
    print("Choose your money-making method:")
    methods = [
        "AI Tools",
        "Freelancing",
        "Social Media Marketing",
        "Dropshipping",
        "Affiliate Marketing"
    ]
    
    for i, method in enumerate(methods, 1):
        print(f"{i}. {method}")
    print("6. Custom Method")
    
    choice = input("\nEnter your choice (1-6): ")
    if choice == "6":
        method = input("Enter your custom method: ")
    else:
        try:
            method = methods[int(choice)-1]
        except:
            method = "AI Tools"
    
    amount = input("\nEnter earnings amount (e.g., $1,000): ") or "$1,000"
    
    print("\nChoose timeframe:")
    print("1. Day")
    print("2. Week")
    print("3. Month")
    timeframe = input("Enter your choice (1-3): ")
    timeframe_map = {"1": "Day", "2": "Week", "3": "Month"}
    timeframe = timeframe_map.get(timeframe, "Week")
    
    print("\nChoose content duration:")
    print("1. Short (30-60 seconds)")
    print("2. Long (3-5 minutes)")
    duration = input("Enter your choice (1-2): ")
    duration = "short" if duration == "1" else "long"
    
    print("\nChoose platform:")
    print("1. TikTok")
    print("2. YouTube")
    print("3. Instagram")
    platform = input("Enter your choice (1-3): ")
    platform_map = {"1": "TikTok", "2": "YouTube", "3": "Instagram"}
    platform = platform_map.get(platform, "TikTok")
    
    print("\nGenerating viral content strategy...")
    print("This may take a moment...\n")
    
    try:
        # Generate content using positional arguments
        content = generator.generate_money_content(method, amount, timeframe, duration)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"money_strategy_{method.lower().replace(' ', '_')}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== Viral Money Content Strategy ===\n")
            f.write(f"Method: {method}\n")
            f.write(f"Amount: {amount}\n")
            f.write(f"Timeframe: {timeframe}\n")
            f.write(f"Duration: {duration}\n")
            f.write(f"Platform: {platform}\n")
            f.write("\n=== Content Strategy ===\n\n")
            f.write(content)
        
        # Display results
        print("=== Generated Content Strategy ===\n")
        print(content)
        print(f"\nStrategy has been saved to: {filename}")
        
        # Save metadata
        meta_filename = f"money_strategy_{method.lower().replace(' ', '_')}_{timestamp}.json"
        metadata = {
            "method": method,
            "amount": amount,
            "timeframe": timeframe,
            "duration": duration,
            "platform": platform,
            "timestamp": timestamp,
            "content_file": filename
        }
        
        with open(meta_filename, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        print(f"Metadata has been saved to: {meta_filename}")
        
    except Exception as e:
        print(f"\nError generating content: {str(e)}")
        return
    
    print("\nWould you like to:")
    print("1. Generate another strategy")
    print("2. Exit")
    
    choice = input("\nEnter your choice (1-2): ")
    if choice == "1":
        print("\n" + "="*50 + "\n")
        main()
    else:
        print("\nThank you for using the Viral Money Content Generator! 💰")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
