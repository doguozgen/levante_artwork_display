# Levante Artwork Display

A minimal Odoo 19 Community addon that adds a standalone, fullscreen artwork label at:

```text
/shop/<product-slug>/qr
/shop/<product-slug>/qr/
```

The QR code points to the normal public product page:

```text
https://levante.art/shop/<product-slug>
```

## What is displayed

- Product brand name (`product.product_brand_id.name`) as the artist
- Product brand description (`product.product_brand_id.description`)
- Product name (`product.template.name`) as the artwork title
- A native Odoo-generated QR code for the canonical Levante product URL

No price, stock state, images, logo, navigation, footer, internal notes, costs, suppliers, or other product fields are exposed.

## Eligibility and access

The route returns 404 unless the product is:

- active;
- saleable;
- published on the current website;
- assigned to the current website/company when restricted;
- assigned an OCA Product Brand.

Sold and zero-stock artworks remain visible because stock is intentionally not checked.

## Data safety

The addon adds no fields and performs no writes to products or brands. It is a read-only HTTP route and standalone QWeb template.

## Dependencies

- `website_sale`
- OCA `product_brand` 19.0

## Important deployment note

This addon contains a Python HTTP controller. Odoo's **Apps → Import Module** wizard only accepts importable data modules (XML, i18n and static assets), so that wizard cannot install this exact dynamic route.

Deploy this folder through Cloudpepper's Git Addons mechanism, then update the Apps List and install **Levante Artwork Display**.
