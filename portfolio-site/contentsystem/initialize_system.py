"""
Initialization and test script for the Viral Content Creation System.
This script sets up the database, initializes required data, and runs a test query.
"""

import os
from database_manager import ContentDatabaseManager
from main import ViralContentSystem
from initial_hashtags import initialize_hashtag_database
from viral_techniques import ViralTechniques

def test_system_setup():
    """Test the system setup and run a sample content creation request."""
    print("=== Testing Viral Content Creation System ===\n")
    
    # Initialize database
    print("1. Initializing database...")
    db_manager = ContentDatabaseManager()
    initialize_hashtag_database(db_manager)
    print("✓ Database initialized successfully\n")

    # Verify hashtag data
    print("2. Verifying hashtag data...")
    tiktok_tags = db_manager.get_platform_hashtags('tiktok')
    youtube_tags = db_manager.get_platform_hashtags('youtube')
    instagram_tags = db_manager.get_platform_hashtags('instagram')
    
    if tiktok_tags and youtube_tags and instagram_tags:
        print("✓ Hashtag data verified successfully")
        print(f"  - TikTok hashtags: {len(tiktok_tags) if tiktok_tags else 0}")
        print(f"  - YouTube hashtags: {len(youtube_tags) if youtube_tags else 0}")
        print(f"  - Instagram hashtags: {len(instagram_tags) if instagram_tags else 0}\n")
    else:
        print("✗ Error: Hashtag data verification failed\n")

    # Load viral techniques
    print("3. Loading viral techniques...")
    techniques = ViralTechniques()
    hook_patterns = techniques.get_hook_patterns()
    pattern_interrupts = techniques.get_pattern_interrupts()
    retention_strategies = techniques.get_retention_strategies()
    
    if hook_patterns and pattern_interrupts and retention_strategies:
        print("✓ Viral techniques loaded successfully")
        print(f"  - Hook patterns: {len(hook_patterns)}")
        print(f"  - Pattern interrupts: {len(pattern_interrupts)}")
        print(f"  - Retention strategies: {len(retention_strategies)}\n")
    else:
        print("✗ Error: Viral techniques loading failed\n")

    # Test content creation system
    print("4. Testing content creation system...")
    try:
        # Check if GROQ_API_KEY is set
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("✗ Error: GROQ_API_KEY environment variable not set")
            print("  Please set your Groq API key before running the system\n")
            return

        content_system = ViralContentSystem(api_key)
        print("✓ Content creation system initialized successfully\n")

        # Run test query
        print("5. Running test query...")
        test_topic = "5 Life-Changing Morning Habits"
        print(f"Test topic: '{test_topic}'")
        
        response_generator = content_system.process_content_request(test_topic)
        print("\nTest Response Preview:")
        print("-" * 50)
        for response in response_generator:
            print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 50)
        print("✓ Test query completed successfully\n")

    except Exception as e:
        print(f"✗ Error during system test: {str(e)}\n")

    print("=== System Setup Complete ===")
    print("""
Next Steps:
1. Run 'python main.py' to start the Gradio interface
2. Enter your video topic or concept
3. Get your viral content strategy!
    """)

def main():
    """Main function to run the system setup and test."""
    try:
        test_system_setup()
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        print("Please check the error message above and try again.")

if __name__ == "__main__":
    main()
