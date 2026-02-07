"""
STUDY HUB - Educational Skills to Semester-wise Syllabi Generator
Ultimate Premium UI with Full Customization & Advanced Settings
Uses IBM Granite 3.3 2B via Ollama API
"""

import streamlit as st
import requests
import json
from typing import List, Dict
import time
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "granite3.1-dense:2b"

# Background Theme Presets
BACKGROUND_THEMES = {
    "Purple Gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "Ocean Blue": "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)",
    "Sunset Orange": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
    "Forest Green": "linear-gradient(135deg, #134e5e 0%, #71b280 100%)",
    "Rose Pink": "linear-gradient(135deg, #f857a6 0%, #ff5858 100%)",
    "Night Sky": "linear-gradient(135deg, #000428 0%, #004e92 100%)",
    "Cosmic Purple": "linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%)",
    "Mint Fresh": "linear-gradient(135deg, #00b4db 0%, #0083b0 100%)",
    "Golden Hour": "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)",
    "Deep Space": "linear-gradient(135deg, #141e30 0%, #243b55 100%)",
    "Cherry Blossom": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)",
    "Aurora": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def call_ollama(prompt: str, temperature: float = 0.7) -> str:
    """Call Ollama API with IBM Granite model"""
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "temperature": temperature
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to Ollama. Make sure Ollama is running on localhost:11434")
        return ""
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return ""
    except Exception as e:
        st.error(f"❌ Error calling Ollama: {str(e)}")
        return ""


def generate_syllabus(skills: List[str], num_semesters: int, program_name: str, 
                     program_type: str, additional_info: str, detail_level: str,
                     include_prerequisites: bool, include_resources: bool) -> Dict:
    """Generate comprehensive semester-wise syllabus from skills"""
    
    skills_text = ", ".join(skills)
    
    detail_instruction = {
        "Brief": "Keep it concise and high-level",
        "Standard": "Provide balanced detail",
        "Comprehensive": "Include extensive details, examples, and explanations"
    }
    
    prereq_text = "- Prerequisites and recommended background" if include_prerequisites else ""
    resources_text = "- Required Resources: textbooks, software, tools" if include_resources else ""
    
    prompt = f"""You are an expert curriculum designer. Create a detailed, comprehensive semester-wise syllabus.

Program Name: {program_name}
Program Type: {program_type}
Number of Semesters: {num_semesters}
Skills to Cover: {skills_text}
Detail Level: {detail_instruction[detail_level]}
Additional Requirements: {additional_info if additional_info else "None"}

Generate a detailed syllabus with the following structure:

1. PROGRAM OVERVIEW
- Program duration
- Learning objectives
- Target audience
{prereq_text}

2. For EACH SEMESTER (Semester 1 to {num_semesters}):
   SEMESTER [NUMBER]: [NAME]
   - Duration: [weeks]
   - Focus Areas: [main topics]
   
   COURSES:
   Course 1: [Course Name]
   - Credits: [number]
   - Description: [brief description]
   - Topics Covered:
     • [Topic 1]
     • [Topic 2]
     • [Topic 3]
   - Skills Developed: [skills from the input list]
   - Assessment Methods: [how students are evaluated]
   {resources_text}
   
   Course 2: [Course Name]
   [Same structure as above]
   
   [Continue for 3-4 courses per semester]

3. SKILL PROGRESSION MAP
- Show how skills build across semesters

4. CAREER PATHWAYS
- Potential career outcomes
- Job roles and opportunities

Please provide a comprehensive, well-structured response."""

    with st.spinner("🤖 Granite AI is generating your syllabus..."):
        response = call_ollama(prompt, temperature=0.7)
    
    if not response:
        return None
    
    return {
        "program_name": program_name,
        "program_type": program_type,
        "num_semesters": num_semesters,
        "skills": skills,
        "syllabus_content": response,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "detail_level": detail_level
    }


def enhance_course_details(course_name: str, skills: List[str]) -> str:
    """Generate detailed course content for a specific course"""
    
    prompt = f"""You are a curriculum specialist. Create detailed course content for:

Course: {course_name}
Related Skills: {", ".join(skills)}

Provide:
1. COURSE DESCRIPTION (2-3 paragraphs)
2. LEARNING OUTCOMES (5-7 specific outcomes)
3. WEEKLY BREAKDOWN (12-15 weeks):
   Week 1: [Topic] - [What students will learn]
   Week 2: [Topic] - [What students will learn]
   [Continue...]
4. ASSESSMENT STRUCTURE:
   - Assignment types
   - Project details
   - Exam format
5. REQUIRED RESOURCES:
   - Textbooks/materials
   - Software/tools
   - Online resources

Be specific and detailed."""

    return call_ollama(prompt, temperature=0.6)


def analyze_skill_gap(current_skills: List[str], target_program: str) -> str:
    """Analyze skill gaps for a target program"""
    
    prompt = f"""You are a career advisor and skill gap analyst.

Current Skills: {", ".join(current_skills)}
Target Program: {target_program}

Analyze:
1. SKILL GAP ANALYSIS
   - Skills the person already has
   - Skills they need to acquire
   - Priority level for each missing skill

2. LEARNING PATHWAY
   - Recommended learning sequence
   - Estimated time to acquire each skill
   - Resources and courses

3. CAREER READINESS SCORE
   - Rate current readiness (0-100%)
   - Key areas to focus on
   - Timeline to become job-ready

Be specific and actionable."""

    return call_ollama(prompt, temperature=0.6)


def generate_study_schedule(num_semesters: int, courses_per_semester: int, 
                           hours_per_week: int) -> str:
    """Generate a personalized study schedule"""
    
    prompt = f"""You are a study planner expert. Create a detailed study schedule.

Program Duration: {num_semesters} semesters
Courses per Semester: {courses_per_semester}
Available Hours per Week: {hours_per_week}

Create:
1. WEEKLY TIME ALLOCATION
   - Hours per course
   - Study sessions breakdown
   - Break times

2. SEMESTER MILESTONES
   - Week-by-week goals
   - Assignment deadlines
   - Exam preparation schedule

3. PRODUCTIVITY TIPS
   - Best practices for time management
   - Study techniques
   - Work-life balance strategies

Be practical and specific."""

    return call_ollama(prompt, temperature=0.6)


def compare_programs(program1: str, program2: str) -> str:
    """Compare two educational programs"""
    
    prompt = f"""You are an education consultant. Compare these two programs:

Program 1: {program1}
Program 2: {program2}

Provide:
1. CURRICULUM COMPARISON
   - Core subjects
   - Specialization areas
   - Hands-on vs theory

2. CAREER OUTCOMES
   - Job roles for each
   - Salary expectations
   - Industry demand

3. RECOMMENDATION
   - Who should choose Program 1
   - Who should choose Program 2
   - Key decision factors

Be objective and detailed."""

    return call_ollama(prompt, temperature=0.6)


def generate_learning_roadmap(skills: List[str], timeline_weeks: int) -> str:
    """Generate a learning roadmap"""
    
    prompt = f"""You are a learning path designer. Create a roadmap to master these skills:

Skills: {", ".join(skills)}
Timeline: {timeline_weeks} weeks

Create:
1. PHASE-BY-PHASE BREAKDOWN
   - What to learn each phase
   - Projects to build
   - Milestones to achieve

2. RESOURCE RECOMMENDATIONS
   - Online courses
   - Books and tutorials
   - Practice platforms

3. PROGRESS TRACKING
   - How to measure progress
   - Portfolio projects
   - Certification goals

Be practical and motivating."""

    return call_ollama(prompt, temperature=0.6)


def generate_css(theme_bg, anim_speed, fonts, card_style, show_animations):
    """Generate CSS with proper escaping"""
    
    # Determine colors based on card style
    if card_style == "Glassmorphism":
        card_bg = "rgba(255, 255, 255, 0.1)"
        card_border = "rgba(255, 255, 255, 0.2)"
        card_shadow = "0.1"
        text_color = "white"
        metric_color = "white"
        metric_label_color = "rgba(255, 255, 255, 0.8)"
    else:
        card_bg = "rgba(255, 255, 255, 0.95)"
        card_border = "rgba(0, 0, 0, 0.1)"
        card_shadow = "0.05"
        text_color = "#333"
        metric_color = "#333"
        metric_label_color = "rgba(0, 0, 0, 0.6)"
    
    # Animation keyframes
    gradient_anim = ""
    slideup_anim = ""
    shimmer_anim = ""
    float_anim = ""
    fadein_anim = ""
    popin_anim = ""
    pulse_anim = ""
    slideinright_anim = ""
    shake_anim = ""
    blink_anim = ""
    
    if show_animations:
        gradient_anim = "animation: gradientShift 15s ease infinite;"
        slideup_anim = "animation: slideUp 0.6s ease-out;"
        shimmer_anim = "animation: shimmer 3s infinite, float 3s ease-in-out infinite;"
        fadein_anim = "animation: fadeIn 1s ease-out 0.3s backwards;"
        popin_anim = "animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);"
        pulse_anim = "animation: pulse 2s ease-in-out infinite;"
        slideinright_anim = "animation: slideInRight 0.5s ease-out;"
        shake_anim = "animation: shake 0.5s ease-out;"
        blink_anim = "animation: blink 2s ease-in-out infinite;"
        
        gradient_anim_def = """
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        """
        slideup_anim_def = """
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        """
        shimmer_anim_def = """
        @keyframes shimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        """
        float_anim_def = """
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        """
        fadein_anim_def = """
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        """
        popin_anim_def = """
        @keyframes popIn {
            0% { opacity: 0; transform: scale(0) rotate(-180deg); }
            100% { opacity: 1; transform: scale(1) rotate(0deg); }
        }
        """
        pulse_anim_def = """
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 255, 255, 0.2); }
            50% { box-shadow: 0 0 35px rgba(255, 255, 255, 0.4); }
        }
        """
        slideinright_anim_def = """
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(50px); }
            to { opacity: 1; transform: translateX(0); }
        }
        """
        shake_anim_def = """
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        """
        blink_anim_def = """
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        """
    else:
        gradient_anim_def = slideup_anim_def = shimmer_anim_def = ""
        float_anim_def = fadein_anim_def = popin_anim_def = ""
        pulse_anim_def = slideinright_anim_def = shake_anim_def = blink_anim_def = ""
    
    transition = f"transition: all {anim_speed} cubic-bezier(0.68, -0.55, 0.265, 1.55);" if show_animations else ""
    backdrop_filter = "backdrop-filter: blur(10px);" if card_style == "Glassmorphism" else ""
    
    transform_hover_card = "transform: translateY(-10px) scale(1.02);" if show_animations else ""
    transform_hover_button = "transform: translateY(-5px) scale(1.05);" if show_animations else ""
    transform_hover_skill = "transform: translateY(-5px) scale(1.1) rotate(2deg);" if show_animations else ""
    transform_hover_tab = "transform: translateY(-2px);" if show_animations else ""
    transform_hover_download = "transform: translateY(-5px);" if show_animations else ""
    transform_active = "transform: scale(0.95);" if show_animations else ""
    transform_focus = "transform: translateY(-2px);" if show_animations else ""
    transform_sidebar = "transform: translateX(5px);" if show_animations else ""
    transform_tab_selected = "transform: scale(1.05);" if show_animations else ""
    
    css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        * {{
            font-family: 'Poppins', sans-serif;
            {transition}
            font-size: {fonts["base"]};
        }}
        
        .stApp {{
            background: {theme_bg};
            {gradient_anim}
            background-size: 400% 400%;
        }}
        
        {gradient_anim_def}
        
        .glass-card {{
            background: {card_bg};
            {backdrop_filter}
            border-radius: 20px;
            border: 1px solid {card_border};
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, {card_shadow});
            {slideup_anim}
            color: {text_color};
        }}
        
        {slideup_anim_def}
        
        .glass-card:hover {{
            {transform_hover_card}
            box-shadow: 0 15px 45px rgba(0, 0, 0, 0.2);
            border-color: {card_border};
        }}
        
        .main-header {{
            font-size: {fonts["header"]};
            font-weight: 800;
            background: linear-gradient(45deg, #fff, #ffd700, #fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0;
            {shimmer_anim}
            background-size: 200% 200%;
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
        }}
        
        {shimmer_anim_def}
        {float_anim_def}
        
        .sub-header {{
            font-size: {fonts["sub"]};
            color: rgba(255, 255, 255, 0.9);
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 300;
            {fadein_anim}
            letter-spacing: 2px;
        }}
        
        {fadein_anim_def}
        
        .skill-tag {{
            display: inline-block;
            padding: 0.5rem 1.2rem;
            margin: 0.3rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 25px;
            color: white;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            border: 2px solid rgba(255, 255, 255, 0.3);
            {popin_anim}
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }}
        
        {popin_anim_def}
        
        .skill-tag:hover {{
            {transform_hover_skill}
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }}
        
        .stButton>button {{
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 15px;
            padding: 0.8rem 2rem;
            font-size: 1.1rem;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }}
        
        .stButton>button:hover {{
            {transform_hover_button}
            box-shadow: 0 10px 35px rgba(102, 126, 234, 0.6);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }}
        
        .stButton>button:active {{
            {transform_active}
        }}
        
        input, textarea, select {{
            background: {card_bg if card_style == "Glassmorphism" else "white"} !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px !important;
            padding: 0.8rem !important;
            color: #333 !important;
            font-size: 1rem !important;
        }}
        
        input:focus, textarea:focus, select:focus {{
            border-color: #667eea !important;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
            {transform_focus}
            background: white !important;
        }}
        
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        section[data-testid="stSidebar"] .stButton>button {{
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(5px);
        }}
        
        section[data-testid="stSidebar"] .stButton>button:hover {{
            background: rgba(255, 255, 255, 0.3);
            {transform_sidebar}
        }}
        
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 700;
            color: {metric_color};
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {metric_label_color};
            font-weight: 500;
        }}
        
        .metric-card {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            {pulse_anim}
        }}
        
        {pulse_anim_def}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 15px;
            backdrop-filter: blur(5px);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 12px 24px;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background: rgba(255, 255, 255, 0.2);
            {transform_hover_tab}
        }}
        
        .stTabs [aria-selected="true"] {{
            background: rgba(255, 255, 255, 0.3) !important;
            {transform_tab_selected}
        }}
        
        .stDownloadButton>button {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border-radius: 12px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            box-shadow: 0 5px 20px rgba(17, 153, 142, 0.4);
        }}
        
        .stDownloadButton>button:hover {{
            {transform_hover_download}
            box-shadow: 0 10px 35px rgba(17, 153, 142, 0.6);
        }}
        
        .stSuccess {{
            background: rgba(56, 239, 125, 0.2);
            border-left: 5px solid #38ef7d;
            {slideinright_anim}
        }}
        
        .stError {{
            background: rgba(239, 68, 68, 0.2);
            border-left: 5px solid #ef4444;
            {shake_anim}
        }}
        
        {slideinright_anim_def}
        {shake_anim_def}
        
        .stInfo {{
            background: rgba(102, 126, 234, 0.2);
            border-left: 5px solid #667eea;
            border-radius: 10px;
        }}
        
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
            margin: 2rem 0;
        }}
        
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, #667eea, #764ba2);
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, #764ba2, #667eea);
        }}
        
        .status-online {{
            width: 12px;
            height: 12px;
            background: #38ef7d;
            border-radius: 50%;
            display: inline-block;
            {blink_anim}
            box-shadow: 0 0 10px #38ef7d;
        }}
        
        {blink_anim_def}
        
        .settings-section {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .settings-section:hover {{
            background: rgba(255, 255, 255, 0.15);
        }}
        </style>
    """
    return css


# ============================================
# STREAMLIT UI
# ============================================

def main():
    # Page configuration
    st.set_page_config(
        page_title="STUDY HUB - AI Academic Planner",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'generated_syllabus' not in st.session_state:
        st.session_state.generated_syllabus = None
    if 'skills_list' not in st.session_state:
        st.session_state.skills_list = []
    if 'syllabus_history' not in st.session_state:
        st.session_state.syllabus_history = []
    if 'theme' not in st.session_state:
        st.session_state.theme = "Purple Gradient"
    if 'animation_speed' not in st.session_state:
        st.session_state.animation_speed = "Normal"
    if 'card_style' not in st.session_state:
        st.session_state.card_style = "Glassmorphism"
    if 'font_size' not in st.session_state:
        st.session_state.font_size = "Medium"
    if 'show_animations' not in st.session_state:
        st.session_state.show_animations = True
    if 'auto_save' not in st.session_state:
        st.session_state.auto_save = True
    
    # Get animation speed
    animation_speeds = {
        "Slow": "0.8s",
        "Normal": "0.4s",
        "Fast": "0.2s"
    }
    anim_speed = animation_speeds[st.session_state.animation_speed]
    
    # Get font sizes
    font_sizes = {
        "Small": {"base": "0.9rem", "header": "3.5rem", "sub": "1.2rem"},
        "Medium": {"base": "1rem", "header": "4.5rem", "sub": "1.5rem"},
        "Large": {"base": "1.1rem", "header": "5.5rem", "sub": "1.8rem"}
    }
    fonts = font_sizes[st.session_state.font_size]
    
    # Generate and apply CSS
    css = generate_css(
        BACKGROUND_THEMES[st.session_state.theme],
        anim_speed,
        fonts,
        st.session_state.card_style,
        st.session_state.show_animations
    )
    st.markdown(css, unsafe_allow_html=True)
    
    # Animated Header
    st.markdown('<h1 class="main-header">🎓 STUDY HUB</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ Your Smart Companion for Organized Learning ✨</p>', unsafe_allow_html=True)
    
    # Sidebar with Settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings & Control Panel")
        st.markdown("---")
        
        # Settings Tabs
        settings_tab1, settings_tab2 = st.tabs(["🎨 Appearance", "🔧 Advanced"])
        
        with settings_tab1:
            st.markdown('<div class="settings-section">', unsafe_allow_html=True)
            st.markdown("#### Background Theme")
            new_theme = st.selectbox(
                "Choose Theme",
                options=list(BACKGROUND_THEMES.keys()),
                index=list(BACKGROUND_THEMES.keys()).index(st.session_state.theme),
                label_visibility="collapsed"
            )
            if new_theme != st.session_state.theme:
                st.session_state.theme = new_theme
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="settings-section">', unsafe_allow_html=True)
            st.markdown("#### Card Style")
            new_card_style = st.radio(
                "Card Style",
                ["Glassmorphism", "Solid"],
                index=0 if st.session_state.card_style == "Glassmorphism" else 1,
                label_visibility="collapsed",
                horizontal=True
            )
            if new_card_style != st.session_state.card_style:
                st.session_state.card_style = new_card_style
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="settings-section">', unsafe_allow_html=True)
            st.markdown("#### Font Size")
            new_font_size = st.select_slider(
                "Font Size",
                options=["Small", "Medium", "Large"],
                value=st.session_state.font_size,
                label_visibility="collapsed"
            )
            if new_font_size != st.session_state.font_size:
                st.session_state.font_size = new_font_size
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="settings-section">', unsafe_allow_html=True)
            st.markdown("#### Animation Speed")
            new_speed = st.select_slider(
                "Speed",
                options=["Slow", "Normal", "Fast"],
                value=st.session_state.animation_speed,
                label_visibility="collapsed"
            )
            if new_speed != st.session_state.animation_speed:
                st.session_state.animation_speed = new_speed
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="settings-section">', unsafe_allow_html=True)
            new_animations = st.toggle("Enable Animations", st.session_state.show_animations)
            if new_animations != st.session_state.show_animations:
                st.session_state.show_animations = new_animations
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with settings_tab2:
            st.markdown('<div class="settings-section">', unsafe_allow_html=True)
            st.markdown("#### Auto-Save")
            st.session_state.auto_save = st.toggle("Auto-save generated content", st.session_state.auto_save)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="settings-section">', unsafe_allow_html=True)
            st.markdown("#### Export Format")
            export_format = st.radio(
                "Default export format",
                ["TXT", "MD", "PDF"],
                horizontal=True,
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="settings-section">', unsafe_allow_html=True)
            st.markdown("#### AI Temperature")
            ai_temp = st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1, label_visibility="collapsed")
            st.caption("Higher = More creative")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Ollama Status
        st.markdown("#### 🔌 System Status")
        try:
            test_response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if test_response.status_code == 200:
                st.markdown('<span class="status-online"></span> Ollama Connected', unsafe_allow_html=True)
                models = test_response.json().get('models', [])
                model_names = [m.get('name', '') for m in models]
                if MODEL_NAME in model_names or any(MODEL_NAME in name for name in model_names):
                    st.success(f"✅ {MODEL_NAME} Ready")
                else:
                    st.warning(f"⚠️ Model not found")
            else:
                st.error("❌ Connection Failed")
        except:
            st.error("❌ Ollama Offline")
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("#### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold;color:white;'>{len(st.session_state.skills_list)}</div><div style='color:rgba(255,255,255,0.8);font-size:0.85rem;'>Skills</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold;color:white;'>{len(st.session_state.syllabus_history)}</div><div style='color:rgba(255,255,255,0.8);font-size:0.85rem;'>Generated</div></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Sample Skills
        st.markdown("#### 💡 Quick Add Skills")
        sample_skills = [
            "Python Programming", "Data Structures", "Machine Learning",
            "Web Development", "Database Design", "Cloud Computing",
            "UI/UX Design", "Project Management", "DevOps",
            "Cybersecurity", "Mobile App Development", "Data Analytics"
        ]
        
        for skill in sample_skills:
            if st.button(f"➕ {skill}", key=f"sample_{skill}", use_container_width=True):
                if skill not in st.session_state.skills_list:
                    st.session_state.skills_list.append(skill)
                    st.rerun()
        
        st.markdown("---")
        st.markdown("#### 🗑️ Actions")
        if st.button("Clear All Skills", use_container_width=True):
            st.session_state.skills_list = []
            st.rerun()
        
        if st.button("Reset All Settings", use_container_width=True):
            st.session_state.theme = "Purple Gradient"
            st.session_state.animation_speed = "Normal"
            st.session_state.card_style = "Glassmorphism"
            st.session_state.font_size = "Medium"
            st.session_state.show_animations = True
            st.rerun()
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📝 Generate Syllabus", 
        "📄 View Result", 
        "🔍 Course Deep Dive",
        "📊 Skill Gap Analysis",
        "📅 Study Schedule",
        "⚖️ Program Comparison",
        "🗺️ Learning Roadmap"
    ])
    
    # TAB 1: Generate Syllabus
    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🎯 Program Configuration")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            program_name = st.text_input(
                "Program Name",
                placeholder="e.g., Bachelor of Computer Science, Data Science Bootcamp",
                help="Enter the name of your educational program"
            )
        
        with col2:
            program_type = st.selectbox(
                "Program Type",
                ["Degree Program", "Certificate Program", "Bootcamp", "Professional Course", "Online Course"]
            )
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            num_semesters = st.number_input(
                "Number of Semesters",
                min_value=1,
                max_value=10,
                value=4,
                help="How many semesters should this program span?"
            )
        
        with col4:
            detail_level = st.selectbox(
                "Detail Level",
                ["Brief", "Standard", "Comprehensive"],
                index=1
            )
        
        with col5:
            st.write("")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 💡 Skills Portfolio")
        
        # Skill input
        col_input, col_add = st.columns([4, 1])
        with col_input:
            new_skill = st.text_input(
                "Add a skill",
                placeholder="Type a skill and click Add",
                label_visibility="collapsed",
                key="skill_input"
            )
        with col_add:
            if st.button("➕ Add", use_container_width=True, key="add_skill_btn"):
                if new_skill and new_skill not in st.session_state.skills_list:
                    st.session_state.skills_list.append(new_skill)
                    st.rerun()
        
        # Display current skills
        if st.session_state.skills_list:
            st.markdown("**Your Skills:**")
            skills_html = "<div style='margin: 1rem 0;'>"
            for skill in st.session_state.skills_list:
                skills_html += f'<span class="skill-tag">✨ {skill}</span>'
            skills_html += "</div>"
            st.markdown(skills_html, unsafe_allow_html=True)
            
            # Remove skills
            st.markdown("**Remove Skills:**")
            cols = st.columns(min(len(st.session_state.skills_list), 4))
            for idx, skill in enumerate(st.session_state.skills_list):
                with cols[idx % 4]:
                    if st.button(f"❌ {skill}", key=f"remove_{idx}"):
                        st.session_state.skills_list.remove(skill)
                        st.rerun()
        else:
            st.info("👆 Add skills using the input above or quick add from sidebar")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Advanced Options")
        
        col1, col2 = st.columns(2)
        with col1:
            include_prerequisites = st.checkbox("Include Prerequisites", True)
        with col2:
            include_resources = st.checkbox("Include Learning Resources", True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Additional Requirements")
        
        additional_info = st.text_area(
            "Extra Details",
            placeholder="e.g., Focus on hands-on projects, Include industry certifications, Emphasize practical applications...",
            height=120,
            label_visibility="collapsed"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Generate button
        if st.button("🚀 Generate Comprehensive Syllabus", use_container_width=True, type="primary"):
            if not program_name:
                st.error("❌ Please enter a program name")
            elif len(st.session_state.skills_list) == 0:
                st.error("❌ Please add at least one skill")
            else:
                result = generate_syllabus(
                    st.session_state.skills_list,
                    num_semesters,
                    program_name,
                    program_type,
                    additional_info,
                    detail_level,
                    include_prerequisites,
                    include_resources
                )
                
                if result:
                    st.session_state.generated_syllabus = result
                    st.session_state.syllabus_history.append({
                        'name': program_name,
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("✨ Syllabus generated successfully! Check the 'View Result' tab.")
                    st.balloons()
    
    # TAB 2: View Result
    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        if st.session_state.generated_syllabus:
            result = st.session_state.generated_syllabus
            
            st.markdown("### 📊 Syllabus Overview")
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📚 Program", result['program_name'][:20] + "...")
            with col2:
                st.metric("📅 Semesters", result['num_semesters'])
            with col3:
                st.metric("💡 Skills", len(result['skills']))
            with col4:
                st.metric("📝 Detail", result['detail_level'])
            
            st.caption(f"⏰ Generated: {result['generated_at']}")
            
            st.markdown("---")
            
            # Syllabus content
            st.markdown("### 📖 Full Syllabus")
            st.markdown(result['syllabus_content'])
            
            st.markdown("---")
            
            # Download button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Download Syllabus",
                    data=result['syllabus_content'],
                    file_name=f"{result['program_name'].replace(' ', '_')}_syllabus.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
        else:
            st.info("👈 Generate a syllabus first in the 'Generate Syllabus' tab")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # TAB 3: Course Deep Dive
    with tab3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🔬 Detailed Course Analysis")
        
        course_name_input = st.text_input(
            "Course Name",
            placeholder="e.g., Introduction to Machine Learning, Web Development Fundamentals"
        )
        
        selected_skills = st.multiselect(
            "Related Skills",
            options=st.session_state.skills_list if st.session_state.skills_list else ["Python", "JavaScript", "SQL"],
            help="Select skills this course should cover"
        )
        
        if st.button("🔍 Generate Detailed Course Content", use_container_width=True):
            if course_name_input and selected_skills:
                with st.spinner("🔬 Analyzing course structure..."):
                    detailed_content = enhance_course_details(course_name_input, selected_skills)
                if detailed_content:
                    st.markdown("---")
                    st.markdown(detailed_content)
                    
                    st.markdown("---")
                    st.download_button(
                        label="📥 Download Course Details",
                        data=detailed_content,
                        file_name=f"{course_name_input.replace(' ', '_')}_details.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ Please enter a course name and select at least one skill")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # TAB 4: Skill Gap Analysis
    with tab4:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 Skill Gap Analysis")
        
        st.info("💡 Analyze what skills you need to acquire for your target program")
        
        target_program = st.text_input(
            "Target Program/Career",
            placeholder="e.g., Machine Learning Engineer, Full Stack Developer"
        )
        
        if st.button("📈 Analyze Skill Gap", use_container_width=True):
            if target_program and st.session_state.skills_list:
                with st.spinner("📊 Analyzing your skill profile..."):
                    analysis = analyze_skill_gap(st.session_state.skills_list, target_program)
                if analysis:
                    st.markdown("---")
                    st.markdown(analysis)
                    
                    st.markdown("---")
                    st.download_button(
                        label="📥 Download Analysis",
                        data=analysis,
                        file_name=f"skill_gap_analysis_{target_program.replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ Please add your current skills and enter a target program")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # TAB 5: Study Schedule
    with tab5:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📅 Personalized Study Schedule")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            schedule_semesters = st.number_input("Semesters", 1, 10, 4, key="schedule_sem")
        with col2:
            courses_per_sem = st.number_input("Courses/Semester", 2, 8, 4, key="schedule_courses")
        with col3:
            hours_per_week = st.slider("Hours/Week", 10, 60, 30, key="schedule_hours")
        
        if st.button("📅 Generate Study Schedule", use_container_width=True):
            with st.spinner("📅 Creating your personalized schedule..."):
                schedule = generate_study_schedule(schedule_semesters, courses_per_sem, hours_per_week)
            if schedule:
                st.markdown("---")
                st.markdown(schedule)
                
                st.markdown("---")
                st.download_button(
                    label="📥 Download Schedule",
                    data=schedule,
                    file_name="study_schedule.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # TAB 6: Program Comparison
    with tab6:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚖️ Compare Programs")
        
        st.info("💡 Get detailed comparison between two educational programs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            program1 = st.text_input(
                "Program 1",
                placeholder="e.g., Computer Science Degree"
            )
        
        with col2:
            program2 = st.text_input(
                "Program 2",
                placeholder="e.g., Data Science Bootcamp"
            )
        
        if st.button("⚖️ Compare Programs", use_container_width=True):
            if program1 and program2:
                with st.spinner("⚖️ Comparing programs..."):
                    comparison = compare_programs(program1, program2)
                if comparison:
                    st.markdown("---")
                    st.markdown(comparison)
                    
                    st.markdown("---")
                    st.download_button(
                        label="📥 Download Comparison",
                        data=comparison,
                        file_name=f"comparison_{program1.replace(' ', '_')}_vs_{program2.replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ Please enter both program names")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # TAB 7: Learning Roadmap
    with tab7:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🗺️ Learning Roadmap Generator")
        
        st.info("💡 Create a step-by-step roadmap to master your skills")
        
        timeline_weeks = st.slider(
            "Learning Timeline (weeks)",
            min_value=4,
            max_value=52,
            value=12,
            help="How many weeks do you have to learn these skills?"
        )
        
        if st.button("🗺️ Generate Learning Roadmap", use_container_width=True):
            if st.session_state.skills_list:
                with st.spinner("🗺️ Creating your personalized learning roadmap..."):
                    roadmap = generate_learning_roadmap(st.session_state.skills_list, timeline_weeks)
                if roadmap:
                    st.markdown("---")
                    st.markdown(roadmap)
                    
                    st.markdown("---")
                    st.download_button(
                        label="📥 Download Roadmap",
                        data=roadmap,
                        file_name=f"learning_roadmap_{timeline_weeks}_weeks.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ Please add skills first in the 'Generate Syllabus' tab")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: rgba(255, 255, 255, 0.8); padding: 2rem;'>
            <p style='font-size: 1.1rem; font-weight: 500;'>Powered by IBM Granite 3.3 2B via Ollama</p>
            <p style='font-size: 0.9rem; opacity: 0.7;'>STUDY HUB © 2026 - Transforming Education Through AI ✨</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()