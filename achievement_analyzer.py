import re

def analyze_achievements(resume_text):
    """
    Analyze achievements and quantifiable metrics in resume.
    
    Returns:
        dict: Achievement metrics including quantified achievements
    """
    achievements = {
        "total_achievements": 0,
        "quantified_achievements": 0,
        "performance_metrics": [],
        "impact_keywords": [],
        "achievement_score": 0,
        "has_metrics": False
    }
    
    resume_lower = resume_text.lower()
    
    # Action verbs indicating achievements
    action_verbs = [
        "improved", "increased", "reduced", "optimized", "accelerated",
        "enhanced", "achieved", "delivered", "generated", "launched",
        "developed", "created", "designed", "implemented", "solved",
        "streamlined", "maximized", "minimized", "transformed", "boosted"
    ]
    
    # Count action verbs as indicators of achievements
    achievement_count = 0
    for verb in action_verbs:
        count = len(re.findall(r'\b' + verb + r'\b', resume_lower))
        achievement_count += count
    
    achievements["total_achievements"] = achievement_count
    
    # Look for quantified metrics (numbers followed by units or percentages)
    metric_patterns = [
        r'\d+%',  # Percentages
        r'\$\d+[KM]?',  # Money
        r'\d+\s*(ms|seconds|minutes|hours|days|weeks|months|years)',  # Time
        r'\d+x',  # Multipliers
        r'\d+\+\s*(users|clients|downloads|projects)'  # Quantities
    ]
    
    quantified_count = 0
    for pattern in metric_patterns:
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        quantified_count += len(matches)
        achievements["performance_metrics"].extend(matches)
    
    achievements["quantified_achievements"] = quantified_count
    achievements["has_metrics"] = quantified_count > 0
    
    # Impact keywords
    impact_keywords = [
        "user satisfaction", "productivity", "efficiency", "quality",
        "performance", "revenue", "cost savings", "market", "growth",
        "scale", "optimization", "automation", "innovation"
    ]
    
    for keyword in impact_keywords:
        if keyword in resume_lower:
            achievements["impact_keywords"].append(keyword)
    
    # Calculate achievement score (0-100)
    # More achievements + more quantified metrics = higher score
    achievement_score = min(100, (achievement_count * 3) + (quantified_count * 5))
    achievements["achievement_score"] = min(100, achievement_score)
    
    return achievements
