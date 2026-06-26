with open("index.html", "r") as f:
    content = f.read()

new_styles = """
      /* Center the new hero label */
      .home-hero-content {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        height: 100vh !important;
        width: 100% !important;
      }
      .home-hero-left-content {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
      }
      .hero-label-wrap {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
      }
    </style>
"""

content = content.replace("</style>", new_styles)
with open("index.html", "w") as f:
    f.write(content)
