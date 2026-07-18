# Site generator

`build_site.py` generates every page of the harmonix-glass mockup from
`harmonix-earn-glass.html` (the home-page source, kept here as a copy).

To regenerate after edits:

    cd tools
    cp harmonix-earn-glass.html verichains.svg shieldify.svg ..  # expected in cwd
    python3 build_site.py   # expects OUT dir ../  — run from repo root:
    # From the repo root with the three files alongside build_site.py:
    #   python3 build_site.py   (SRC and OUT paths are relative)

Pages: index, perps, swap, stake, protection, stake-har, portfolio,
analytics, referral, points + assets/style.css.
