"""
card_art.py — one inline-SVG illustration per company, replacing the old
chart-screenshot thumbnail on the homepage cards. Each draws on the site's
existing colour tokens (so it always matches the theme) and nods at that
project's real narrative thread rather than being generic stock art.

All five share a 400x260 viewBox and sit on the card's existing dark
navy-deep background (set in components.css), so only light strokes are
needed here — no background rect.
"""

_WRAP_OPEN = '<svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">'
_WRAP_CLOSE = "</svg>"


def _wrap(label, body):
    return _WRAP_OPEN.format(label=label) + body + _WRAP_CLOSE


def hearthstead():
    """House silhouette with a magnifying glass over one highlighted roof
    section — echoes flagging one suspicious result inside an aggregate trend."""
    body = """
      <polygon points="130,150 200,90 270,150" fill="none" stroke="var(--teal-light)" stroke-width="4" stroke-linejoin="round"/>
      <rect x="145" y="150" width="110" height="70" fill="none" stroke="var(--teal-light)" stroke-width="4"/>
      <rect x="185" y="180" width="30" height="40" fill="none" stroke="var(--teal-light)" stroke-width="3"/>
      <polygon points="188,112 200,92 212,112" fill="var(--teal)"/>
      <circle cx="248" cy="108" r="26" fill="none" stroke="var(--teal)" stroke-width="6"/>
      <line x1="267" y1="127" x2="291" y2="151" stroke="var(--teal)" stroke-width="7" stroke-linecap="round"/>
    """
    return _wrap("A house with a magnifying glass highlighting one section of the roof", body)


def arden():
    """Supply-chain nodes flowing toward a vehicle, one node highlighted —
    echoes tracing exactly where the chain breaks down."""
    body = """
      <line x1="60" y1="130" x2="245" y2="130" stroke="var(--teal-light)" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>
      <circle cx="70" cy="130" r="14" fill="none" stroke="var(--teal-light)" stroke-width="4"/>
      <circle cx="155" cy="130" r="14" fill="var(--teal)"/>
      <circle cx="240" cy="130" r="14" fill="none" stroke="var(--teal-light)" stroke-width="4"/>
      <g>
        <rect x="270" y="115" width="90" height="28" rx="8" fill="none" stroke="var(--teal-light)" stroke-width="4"/>
        <rect x="288" y="100" width="45" height="20" rx="6" fill="none" stroke="var(--teal-light)" stroke-width="4"/>
        <circle cx="290" cy="146" r="9" fill="var(--navy-deep)" stroke="var(--teal-light)" stroke-width="4"/>
        <circle cx="342" cy="146" r="9" fill="var(--navy-deep)" stroke="var(--teal-light)" stroke-width="4"/>
      </g>
    """
    return _wrap("Supply-chain nodes flowing toward a vehicle, with one node highlighted", body)


def westborough():
    """A balance scale in equilibrium — six competing cost pressures, fairly
    weighed; also echoes the project's strict anonymity/fairness stance."""
    body = """
      <line x1="200" y1="60" x2="200" y2="190" stroke="var(--teal-light)" stroke-width="5"/>
      <rect x="170" y="190" width="60" height="10" rx="3" fill="var(--teal-light)"/>
      <line x1="110" y1="90" x2="290" y2="90" stroke="var(--teal-light)" stroke-width="5" stroke-linecap="round"/>
      <circle cx="200" cy="90" r="7" fill="var(--teal)"/>
      <line x1="110" y1="90" x2="110" y2="128" stroke="var(--teal-light)" stroke-width="3"/>
      <path d="M85 128 Q110 155 135 128" fill="none" stroke="var(--teal)" stroke-width="5" stroke-linecap="round"/>
      <line x1="290" y1="90" x2="290" y2="128" stroke="var(--teal-light)" stroke-width="3"/>
      <path d="M265 128 Q290 155 315 128" fill="none" stroke="var(--teal)" stroke-width="5" stroke-linecap="round"/>
    """
    return _wrap("A balance scale in equilibrium", body)


def aerovista():
    """A row of falling dominoes — the most literal metaphor of the five,
    for delay propagation once a buffer is exhausted."""
    body = """
      <g stroke="var(--teal-light)" stroke-width="3" fill="none">
        <rect x="55" y="150" width="18" height="70" rx="3" transform="rotate(-30 64 220)"/>
        <rect x="100" y="140" width="18" height="72" rx="3" transform="rotate(-15 109 212)"/>
        <rect x="150" y="130" width="18" height="82" rx="3"/>
        <rect x="200" y="130" width="18" height="82" rx="3"/>
        <rect x="250" y="130" width="18" height="82" rx="3"/>
        <rect x="300" y="130" width="18" height="82" rx="3" fill="var(--teal)" stroke="var(--teal)"/>
      </g>
    """
    return _wrap("A row of dominoes falling in sequence", body)


def albion():
    """A rising trend line with one spike, alongside a shield — the storm
    episode sitting on the steadier underlying trend, plus the insurance sector."""
    body = """
      <polyline points="50,195 95,182 140,168 168,112 196,162 244,142 292,122 340,102"
                fill="none" stroke="var(--teal)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="168" cy="112" r="6" fill="var(--teal-light)"/>
      <path d="M310 48 L342 61 L342 90 Q342 120 310 135 Q278 120 278 90 L278 61 Z"
            fill="none" stroke="var(--teal-light)" stroke-width="4" stroke-linejoin="round"/>
    """
    return _wrap("A steadily rising trend line with one spike, alongside a shield", body)


CARD_ART = {
    "hearthstead": hearthstead,
    "arden": arden,
    "westborough": westborough,
    "aerovista": aerovista,
    "albion": albion,
}
