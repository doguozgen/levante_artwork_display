# Levante Artwork Display — Cloudpepper repository

This repository contains the Odoo addon in the required nested structure:

```text
repository-root/
└── levante_artwork_display/
    ├── __init__.py
    ├── __manifest__.py
    ├── controllers/
    ├── static/
    └── views/
```

Version `19.0.1.1.0` adds the Sales Price and the `Year`, `Technique`, `Material`, and `Size` product attributes to the fullscreen tablet page.


## Version 1.2

- Shows a circular red **SOLD** badge when Odoo's native website stock logic marks the product variant as sold out.
- Uses the visitor's active website pricelist/currency for the QR display price, matching the normal product page.
- Keeps the layout responsive for iPad Air landscape and portrait fallback.
