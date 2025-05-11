"""
Initial hashtag data for different platforms.
This file provides seed data for the hashtag database.
"""

TIKTOK_HASHTAGS = {
    "trending": [
        "fyp", "foryou", "foryoupage", "viral", "trending", "tiktok", "tiktokviral",
        "trend", "viralvideo", "explore", "fypシ", "viral", "trending", "followme",
        "follow", "like", "share", "comment", "duet", "stitch"
    ],
    "engagement": [
        "community", "support", "share", "comment", "like", "follow", "duet",
        "stitch", "collab", "reaction", "reply", "greenscreen", "pov", "storytime",
        "relatable", "funny", "comedy", "humor", "entertainment", "fun"
    ],
    "content_type": [
        "tutorial", "howto", "tips", "advice", "lifehack", "hack", "diy", "learn",
        "education", "knowledge", "information", "facts", "truth", "reality", "expose",
        "reveal", "secret", "hidden", "unknown", "discovery"
    ],
    "emotional": [
        "motivation", "inspiration", "mindset", "growth", "success", "goals", "dream",
        "believe", "faith", "hope", "love", "happiness", "joy", "peace", "healing",
        "mental", "emotional", "spiritual", "mindfulness", "wellness"
    ],
    "niche": [
        "business", "entrepreneur", "money", "finance", "investing", "crypto",
        "stocks", "realestate", "marketing", "sales", "startup", "smallbusiness",
        "sidehustle", "passive", "income", "wealth", "rich", "millionaire",
        "billionaire", "success"
    ]
}

YOUTUBE_HASHTAGS = {
    "general": [
        "YouTuber", "Video", "NewVideo", "Subscribe", "YouTube", "Creator",
        "Content", "Channel", "Vlog", "Viral", "Trending", "Popular", "New",
        "Hot", "Best", "Top", "Amazing", "Awesome", "Incredible", "Must Watch"
    ],
    "engagement": [
        "Like", "Comment", "Share", "Subscribe", "Notification", "Bell",
        "Support", "Follow", "Community", "Fans", "Viewers", "Audience",
        "Growth", "Engagement", "Interactive", "Discussion", "Debate",
        "Opinion", "Reaction", "Response"
    ],
    "content_specific": [
        "HowTo", "Tutorial", "Guide", "Tips", "Advice", "Help", "Learn",
        "Education", "Knowledge", "Information", "Facts", "Truth", "Reality",
        "Review", "Analysis", "Breakdown", "Explanation", "Understanding",
        "Insight", "Perspective"
    ]
}

INSTAGRAM_HASHTAGS = {
    "general": [
        "instagram", "instagood", "love", "follow", "like", "photooftheday",
        "photography", "beautiful", "art", "picoftheday", "fashion", "nature",
        "happy", "cute", "travel", "style", "instadaily", "followme", "reels",
        "trending"
    ],
    "engagement": [
        "like4like", "follow4follow", "likeforlikes", "followforfollowback",
        "instalike", "l4l", "f4f", "likes", "followback", "following",
        "followers", "likeforfollow", "followforfollow", "likeforlike",
        "likesforlikes", "likeback", "likeforlikeback", "followalways",
        "followforlike", "followtrain"
    ],
    "content": [
        "reels", "instareels", "reelitfeelit", "reelsinstagram", "reelsvideo",
        "reelsindia", "reelkarofeelkaro", "reelstagram", "reelsofinstagram",
        "instagramreels", "newreels", "reelsviral", "viralreels", "trending",
        "trendingreels", "explorepage", "explore", "viral", "trend", "trending"
    ]
}

def initialize_hashtag_database(db_manager):
    """
    Initialize the database with hashtag data for each platform.
    
    Args:
        db_manager: Instance of ContentDatabaseManager
    """
    # Store TikTok hashtags
    all_tiktok_tags = []
    for category, tags in TIKTOK_HASHTAGS.items():
        all_tiktok_tags.extend(tags)
    db_manager.store_hashtags('tiktok', list(set(all_tiktok_tags)))

    # Store YouTube hashtags
    all_youtube_tags = []
    for category, tags in YOUTUBE_HASHTAGS.items():
        all_youtube_tags.extend(tags)
    db_manager.store_hashtags('youtube', list(set(all_youtube_tags)))

    # Store Instagram hashtags
    all_instagram_tags = []
    for category, tags in INSTAGRAM_HASHTAGS.items():
        all_instagram_tags.extend(tags)
    db_manager.store_hashtags('instagram', list(set(all_instagram_tags)))

def get_platform_hashtags(platform: str) -> dict:
    """
    Get hashtags for a specific platform.
    
    Args:
        platform (str): Platform name ('tiktok', 'youtube', or 'instagram')
        
    Returns:
        dict: Dictionary of hashtags by category
    """
    platform = platform.lower()
    if platform == 'tiktok':
        return TIKTOK_HASHTAGS
    elif platform == 'youtube':
        return YOUTUBE_HASHTAGS
    elif platform == 'instagram':
        return INSTAGRAM_HASHTAGS
    else:
        raise ValueError(f"Unknown platform: {platform}")

def get_trending_hashtags(platform: str, limit: int = 20) -> list:
    """
    Get trending hashtags for a specific platform.
    
    Args:
        platform (str): Platform name
        limit (int): Number of hashtags to return
        
    Returns:
        list: List of trending hashtags
    """
    hashtags = get_platform_hashtags(platform)
    if platform == 'tiktok':
        return hashtags['trending'][:limit]
    elif platform == 'youtube':
        return hashtags['general'][:limit]
    elif platform == 'instagram':
        return hashtags['general'][:limit]
    else:
        raise ValueError(f"Unknown platform: {platform}")
