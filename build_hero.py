import re

# Read the HTML file
html_file = 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS to append to the <head>
HERO_CSS = """
    <style>
      /* --- Cornerstone Digital Hero Redesign --- */
      .csd-hero-section {
        position: relative;
        width: 100%;
        min-height: 100vh;
        display: flex;
        align-items: center;
        overflow: hidden;
        padding-top: 80px;
      }
      
      .csd-hero-bg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 1;
      }
      
      .csd-hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, rgba(10,10,10,0.95) 0%, rgba(10,10,10,0.8) 50%, rgba(10,10,10,0.1) 100%);
        z-index: 2;
      }
      
      .csd-hero-container {
        position: relative;
        z-index: 3;
        width: 100%;
        max-width: 1300px;
        margin: 0 auto;
        padding: 0 5%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
      }
      
      .csd-hero-prehead-wrapper {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 24px;
        animation: fadeUp 1s ease 0.2s both;
      }
      
      .csd-hero-prehead-line {
        width: 2px;
        height: 40px;
        background-color: #F7C324;
      }
      
      .csd-hero-prehead-text {
        font-family: inherit;
        font-size: 14px;
        line-height: 1.5;
        letter-spacing: 0.15em;
        font-weight: 600;
        text-transform: uppercase;
      }
      
      .csd-prehead-white { color: #FFFFFF; }
      .csd-prehead-yellow { color: #F7C324; }
      
      .csd-hero-headline {
        font-family: inherit;
        font-size: 5.5rem;
        line-height: 1.05;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0 0 32px 0;
        text-transform: uppercase;
        letter-spacing: -0.02em;
        animation: fadeUp 1s ease 0.4s both;
      }
      
      .csd-headline-yellow { color: #F7C324; }
      
      .csd-hero-body {
        font-size: 1.25rem;
        line-height: 1.6;
        color: #D1D5DB;
        margin: 0 0 48px 0;
        max-width: 600px;
        animation: fadeUp 1s ease 0.6s both;
      }
      
      .csd-hero-cta-group {
        display: flex;
        align-items: center;
        gap: 24px;
        margin-bottom: 48px;
        animation: fadeUp 1s ease 0.8s both;
      }
      
      .csd-btn-primary {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background-color: #F7C324;
        color: #000000;
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 18px 32px;
        border-radius: 6px;
        text-decoration: none;
        transition: all 0.3s ease;
      }
      
      .csd-btn-primary:hover {
        background-color: #FFD242;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(247, 195, 36, 0.3);
      }
      
      .csd-btn-secondary {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: transparent;
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 16px 32px;
        border: 2px solid #F7C324;
        border-radius: 6px;
        text-decoration: none;
        transition: all 0.3s ease;
      }
      
      .csd-btn-secondary:hover {
        background-color: rgba(247, 195, 36, 0.1);
        transform: translateY(-2px);
      }
      
      .csd-hero-trust-row {
        display: flex;
        align-items: center;
        gap: 16px;
        animation: fadeUp 1s ease 1s both;
      }
      
      .csd-hero-avatars {
        display: flex;
        align-items: center;
      }
      
      .csd-hero-avatars img {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: 2px solid #1A1A1A;
        margin-left: -12px;
        object-fit: cover;
      }
      
      .csd-hero-avatars img:first-child {
        margin-left: 0;
      }
      
      .csd-hero-trust-text {
        font-size: 14px;
        color: #A1A1AA;
        font-weight: 500;
      }
      
      @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
      }
      
      @keyframes pulseGlow {
        0% { transform: translateX(0); opacity: 1; }
        50% { transform: translateX(4px); opacity: 0.8; }
        100% { transform: translateX(0); opacity: 1; }
      }
      
      .csd-btn-icon {
        animation: pulseGlow 2s infinite ease-in-out;
      }
      
      /* Nav hover overrides */
      .nav-link:hover, .nav-dropdown-toggle:hover {
        color: #F7C324 !important;
        transition: color 0.3s ease;
      }
      
      /* Responsive */
      @media screen and (max-width: 991px) {
        .csd-hero-headline { font-size: 4.5rem; }
      }
      
      @media screen and (max-width: 767px) {
        .csd-hero-section {
          padding-top: 100px;
          align-items: flex-start;
        }
        .csd-hero-overlay {
          background: linear-gradient(180deg, rgba(10,10,10,0.95) 0%, rgba(10,10,10,0.8) 50%, rgba(10,10,10,0.3) 100%);
        }
        .csd-hero-headline { font-size: 3.5rem; margin-bottom: 24px; }
        .csd-hero-cta-group {
          flex-direction: column;
          align-items: stretch;
          width: 100%;
          gap: 16px;
        }
        .csd-btn-primary, .csd-btn-secondary { width: 100%; }
        .csd-hero-body { margin-bottom: 32px; font-size: 1.15rem; }
      }
      
      @media screen and (max-width: 479px) {
        .csd-hero-headline { font-size: 2.75rem; }
        .csd-hero-body { font-size: 1.1rem; }
        .csd-hero-trust-row {
          flex-direction: column;
          align-items: flex-start;
          gap: 12px;
        }
        .csd-hero-avatars img {
          width: 32px;
          height: 32px;
        }
      }
    </style>
"""

# New HTML
HERO_HTML = """
    <section class="csd-hero-section">
      <img class="csd-hero-bg" src="/assets/images/hero_bg_dark.png" alt="Digital Growth Background" loading="lazy" />
      <div class="csd-hero-overlay"></div>
      
      <div class="csd-hero-container">
        <!-- Pre-heading -->
        <div class="csd-hero-prehead-wrapper">
          <div class="csd-hero-prehead-line"></div>
          <div class="csd-hero-prehead-text">
            <span class="csd-prehead-white">BUILDING THE FOUNDATION</span><br/>
            <span class="csd-prehead-yellow">FOR DIGITAL GROWTH</span>
          </div>
        </div>
        
        <!-- Main Headline -->
        <h1 class="csd-hero-headline">
          GROW YOUR<br/>
          BUSINESS<br/>
          <span class="csd-headline-yellow">DIGITALLY</span>
        </h1>
        
        <!-- Body Text -->
        <p class="csd-hero-body">
          Data-driven strategies. Scalable solutions.<br/>
          Measurable growth.
        </p>
        
        <!-- CTA Buttons -->
        <div class="csd-hero-cta-group">
          <a href="/contact" class="csd-btn-primary">
            BOOK A DISCOVERY CALL
            <svg class="csd-btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <a href="/projects" class="csd-btn-secondary">
            SEE OUR WORK
          </a>
        </div>
        
        <!-- Social Proof Row -->
        <div class="csd-hero-trust-row">
          <div class="csd-hero-avatars">
            <img src="https://cdn.prod.website-files.com/69f5c8889d124099c0296270/69ff0fecbe1ee5019157cb77_profile%20(2).avif" alt="Avatar 1" />
            <img src="https://cdn.prod.website-files.com/69f5c8889d124099c0296270/69ff0fec6664598b87746bb0_profile%20(3).avif" alt="Avatar 2" />
            <img src="https://cdn.prod.website-files.com/69f5c8889d124099c0296270/69ff0fec7e0e2e192cf45c7b_profile%20(1).avif" alt="Avatar 3" />
          </div>
          <div class="csd-hero-trust-text">
            Trusted by growth-focused companies
          </div>
        </div>
      </div>
    </section>
"""

# Apply CSS
if 'csd-hero-section' not in content:
    content = content.replace('</head>', HERO_CSS + '\n</head>')

# Replace old hero section
old_hero_pattern = r'<section class="home-hero-section">.*?</section>'
content = re.sub(old_hero_pattern, HERO_HTML, content, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Hero section successfully replaced.")
