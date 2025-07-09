import streamlit as st
from typing import Dict, Any

class ThemeManager:
    def __init__(self):
        pass
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Get shadcn-inspired dark color palette"""
        return {
            'background': '#0A0A0A',
            'foreground': '#FAFAFA',
            'card': '#161616',
            'card_foreground': '#FAFAFA',
            'popover': '#161616',
            'popover_foreground': '#FAFAFA',
            'primary': '#FAFAFA',
            'primary_foreground': '#0A0A0A',
            'secondary': '#262626',
            'secondary_foreground': '#FAFAFA',
            'muted': '#262626',
            'muted_foreground': '#A1A1AA',
            'accent': '#262626',
            'accent_foreground': '#FAFAFA',
            'destructive': '#DC2626',
            'destructive_foreground': '#FAFAFA',
            'border': '#262626',
            'input': '#262626',
            'ring': '#D4D4D8',
            'chart_1': '#E11D48',
            'chart_2': '#0EA5E9',
            'chart_3': '#22C55E',
            'chart_4': '#F59E0B',
            'chart_5': '#8B5CF6',
        }
    
    def get_modern_css(self) -> str:
        """Generate shadcn-inspired CSS"""
        colors = self.get_theme_colors()
        
        return f"""
        :root {{
            --background: {colors['background']};
            --foreground: {colors['foreground']};
            --card: {colors['card']};
            --card-foreground: {colors['card_foreground']};
            --popover: {colors['popover']};
            --popover-foreground: {colors['popover_foreground']};
            --primary: {colors['primary']};
            --primary-foreground: {colors['primary_foreground']};
            --secondary: {colors['secondary']};
            --secondary-foreground: {colors['secondary_foreground']};
            --muted: {colors['muted']};
            --muted-foreground: {colors['muted_foreground']};
            --accent: {colors['accent']};
            --accent-foreground: {colors['accent_foreground']};
            --destructive: {colors['destructive']};
            --destructive-foreground: {colors['destructive_foreground']};
            --border: {colors['border']};
            --input: {colors['input']};
            --ring: {colors['ring']};
            --chart-1: {colors['chart_1']};
            --chart-2: {colors['chart_2']};
            --chart-3: {colors['chart_3']};
            --chart-4: {colors['chart_4']};
            --chart-5: {colors['chart_5']};
            --radius: 0.5rem;
        }}

        .stApp {{
            background-color: var(--background);
            color: var(--foreground);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}

        .main-header {{
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }}

        .main-header h1 {{
            color: var(--foreground);
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            line-height: 1.2;
        }}

        .main-header p {{
            color: var(--muted-foreground);
            font-size: 1.125rem;
            margin: 0;
        }}

        .musicsynth-tagline {{
            color: var(--muted-foreground);
            font-size: 1rem !important;
            margin-top: 0.5rem !important;
            font-style: italic;
        }}

        .stButton > button {{
            background-color: var(--primary);
            color: var(--primary-foreground);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s ease;
            cursor: pointer;
            min-height: 2.5rem;
        }}

        .stButton > button:hover {{
            background-color: var(--primary);
            opacity: 0.9;
        }}

        .stButton > button:focus {{
            outline: 2px solid var(--ring);
            outline-offset: 2px;
        }}

        .musicsynth-card {{
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin: 1rem 0;
            color: var(--card-foreground);
        }}

        .musicsynth-card h3 {{
            color: var(--foreground);
            font-size: 1.25rem;
            font-weight: 600;
            margin: 0 0 0.75rem 0;
            line-height: 1.3;
        }}

        .musicsynth-card p {{
            color: var(--muted-foreground);
            margin: 0;
            line-height: 1.5;
        }}

        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }}

        .feature-item {{
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            text-align: center;
            transition: all 0.2s ease;
        }}

        .feature-item:hover {{
            background-color: var(--accent);
        }}

        .feature-icon {{
            font-size: 2rem;
            margin-bottom: 1rem;
            display: block;
        }}

        .feature-title {{
            color: var(--foreground);
            font-size: 1.125rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        }}

        .feature-description {{
            color: var(--muted-foreground);
            font-size: 0.875rem;
            margin: 0;
        }}

        .stats-card {{
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin: 0.75rem 0;
            text-align: center;
        }}

        .stats-number {{
            color: var(--foreground);
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        }}

        .stats-label {{
            color: var(--muted-foreground);
            font-size: 0.75rem;
            margin: 0.25rem 0 0 0;
            text-transform: uppercase;
            font-weight: 500;
            letter-spacing: 0.05em;
        }}

        .auth-container {{
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 2rem;
            margin: 2rem auto;
            max-width: 24rem;
        }}

        .stTextInput > div > div > input {{
            background-color: var(--input);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 0.75rem;
            color: var(--foreground);
            font-size: 0.875rem;
            transition: border-color 0.2s ease;
        }}

        .stTextInput > div > div > input:focus {{
            border-color: var(--ring);
            outline: 2px solid var(--ring);
            outline-offset: 2px;
        }}

        .stTextInput > label {{
            color: var(--foreground);
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }}

        .stFileUploader {{
            background-color: var(--card);
            border: 2px dashed var(--border);
            border-radius: var(--radius);
            padding: 2rem;
            text-align: center;
            transition: border-color 0.2s ease;
        }}

        .stFileUploader:hover {{
            border-color: var(--muted-foreground);
        }}

        .sidebar-user {{
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1rem;
            margin: 1rem 0;
            text-align: center;
        }}

        .sidebar-user h3 {{
            color: var(--foreground);
            font-size: 1rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        }}

        .sidebar-user p {{
            color: var(--muted-foreground);
            font-size: 0.875rem;
            margin: 0;
        }}

        .stTabs > div > div {{
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 0.25rem;
            margin: 1rem 0;
        }}

        .stTabs > div > div > div {{
            background-color: transparent;
            border-radius: calc(var(--radius) - 0.125rem);
            padding: 0.5rem 1rem;
            margin: 0.125rem;
            color: var(--muted-foreground);
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .stTabs > div > div > div[aria-selected="true"] {{
            background-color: var(--primary);
            color: var(--primary-foreground);
        }}

        .stAlert {{
            border-radius: var(--radius);
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid var(--border);
        }}

        .stSuccess {{
            background-color: var(--card);
            color: var(--chart-3);
            border-color: var(--chart-3);
        }}

        .stError {{
            background-color: var(--card);
            color: var(--destructive);
            border-color: var(--destructive);
        }}

        .stMarkdown {{
            color: var(--foreground);
        }}

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: var(--foreground);
            font-weight: 600;
        }}

        .stMarkdown code {{
            background-color: var(--muted);
            color: var(--foreground);
            padding: 0.25rem 0.5rem;
            border-radius: calc(var(--radius) - 0.125rem);
            font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.875rem;
        }}

        .stVideo {{
            border-radius: var(--radius);
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        .password-requirements {{
            background-color: var(--muted);
            border-radius: var(--radius);
            padding: 1rem;
            margin: 1rem 0;
        }}

        .password-requirements h4 {{
            color: var(--foreground);
            font-size: 0.875rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        }}

        .password-requirements ul {{
            color: var(--muted-foreground);
            font-size: 0.875rem;
            margin: 0;
            padding-left: 1rem;
        }}

        .developer-note {{
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: center;
        }}

        .developer-note h4 {{
            color: var(--foreground);
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        }}

        .developer-note p {{
            color: var(--muted-foreground);
            margin: 0;
        }}

        .musicsynth-fade-in {{
            animation: fadeIn 0.3s ease-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(0.5rem); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .musicsynth-slide-in {{
            animation: slideIn 0.3s ease-out;
        }}

        @keyframes slideIn {{
            from {{ transform: translateX(-1rem); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}

        /* Streamlit specific overrides */
        .stSelectbox > div > div {{
            background-color: var(--input);
            border: 1px solid var(--border);
            border-radius: var(--radius);
        }}

        .stSelectbox > div > div > div {{
            color: var(--foreground);
        }}

        .stNumberInput > div > div > input {{
            background-color: var(--input);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            color: var(--foreground);
        }}

        .stTextArea > div > div > textarea {{
            background-color: var(--input);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            color: var(--foreground);
        }}

        .stSpinner {{
            border-color: var(--muted-foreground) !important;
        }}

        .stProgress > div > div {{
            background-color: var(--primary);
        }}

        .stProgress > div {{
            background-color: var(--secondary);
        }}
        """
    
    def apply_theme(self):
        """Apply shadcn-inspired theme to the Streamlit app"""
        st.markdown(f"<style>{self.get_modern_css()}</style>", unsafe_allow_html=True)


# Global theme manager instance
theme_manager = ThemeManager()


def apply_modern_theme():
    """Apply shadcn-inspired theme to the app"""
    theme_manager.apply_theme() 