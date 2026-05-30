# Paleta de diseno oficial de StudioTrack y helpers de estilo.
# Centralizar los colores aqui evita repetir hex codes por todo el codigo.

COLORS = {
    "bg_primary": "#0a0a0f",
    "bg_surface": "#13131a",
    "bg_card": "#1a1a24",
    "accent_purple": "#7F77DD",
    "accent_teal": "#1D9E75",
    "accent_coral": "#D85A30",
    "accent_amber": "#EF9F27",
    "text_primary": "#e8e8f0",
    "text_muted": "#8888a0",
    "border": "rgba(255,255,255,0.07)",
}

FONT_DISPLAY = "Syne, sans-serif"
FONT_BODY = "'IBM Plex Mono', monospace"

# Estilos reutilizables.
CARD_STYLE = {
    "background": COLORS["bg_card"],
    "border": f"1px solid {COLORS['border']}",
    "border_radius": "16px",
    "padding": "1.5em",
}

BTN_PRIMARY = {
    "background": COLORS["accent_purple"],
    "color": "white",
    "border_radius": "10px",
    "padding": "0.75em 1.5em",
    "font_family": FONT_BODY,
    "font_weight": "600",
    "cursor": "pointer",
    "_hover": {"opacity": "0.85"},
}