def analyze_languages(resume_text):
    """
    Detect programming and natural languages in resume.
    
    Returns:
        dict: Language analysis with programming and natural languages
    """
    languages_info = {
        "programming_languages": [],
        "markup_languages": [],
        "scripting_languages": [],
        "natural_languages": [],
        "total_languages": 0
    }
    
    resume_lower = resume_text.lower()
    
    # Programming Languages
    programming_langs = [
        "python", "java", "c", "c++", "c#", "ruby", "php", "go", "rust",
        "kotlin", "swift", "objective-c", "scala", "elixir", "haskell",
        "perl", "r", "matlab", "vb.net"
    ]
    
    for lang in programming_langs:
        if lang in resume_lower:
            languages_info["programming_languages"].append(lang.title())
    
    # Markup & Template Languages
    markup_langs = [
        "html", "xml", "json", "yaml", "markdown", "latex", "tex"
    ]
    
    for lang in markup_langs:
        if lang in resume_lower:
            languages_info["markup_languages"].append(lang.upper())
    
    # Scripting Languages
    scripting_langs = [
        "bash", "shell", "powershell", "javascript", "typescript", "lua"
    ]
    
    for lang in scripting_langs:
        if lang in resume_lower:
            languages_info["scripting_languages"].append(lang.title())
    
    # Natural Languages
    natural_langs = {
        "english": "English",
        "spanish": "Spanish",
        "french": "French",
        "german": "German",
        "chinese": "Chinese",
        "japanese": "Japanese",
        "korean": "Korean",
        "hindi": "Hindi",
        "russian": "Russian",
        "arabic": "Arabic"
    }
    
    for keyword, lang_name in natural_langs.items():
        if keyword in resume_lower:
            languages_info["natural_languages"].append(lang_name)
    
    # Calculate total unique languages
    all_langs = (languages_info["programming_languages"] + 
                languages_info["markup_languages"] + 
                languages_info["scripting_languages"] + 
                languages_info["natural_languages"])
    languages_info["total_languages"] = len(set(all_langs))
    
    return languages_info
