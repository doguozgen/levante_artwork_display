# Levante Artwork Display

Fullscreen, read-only artwork information pages for Odoo 19 Community.

## Route

For a published product with an OCA Product Brand:

- Product: `/shop/<product-slug>`
- Tablet display: `/shop/<product-slug>/qr`
- The QR code points back to the normal product URL.

Both the route with and without a trailing slash are supported.

## Displayed information

- Artist name from `product_brand_id.name`
- Artist description from `product_brand_id.description`
- Artwork name from `product.template.name`
- Sales price from `product.template.list_price`
- Currency from `product.template.currency_id`
- Attribute values whose English attribute names are exactly:
  - `Year`
  - `Technique`
  - `Material`
  - `Size`

Attribute-name matching is case-insensitive. Missing attribute values are hidden.

## Safety

The addon does not create, write, or delete products, brands, attributes, or attribute values. It only reads approved public display fields.

## Dependencies

- `website_sale`
- `product_brand` from OCA/brand 19.0

## License

AGPL-3.0


## Version 1.2

- Shows a circular red **SOLD** badge when Odoo's native website stock logic marks the product variant as sold out.
- Uses the visitor's active website pricelist/currency for the QR display price, matching the normal product page.
- Keeps the layout responsive for iPad Air landscape and portrait fallback.
