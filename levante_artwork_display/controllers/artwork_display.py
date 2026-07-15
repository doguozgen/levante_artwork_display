from urllib.parse import urlencode

from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


PUBLIC_BASE_URL = "https://levante.art"
ENGLISH_LANG_CODE = "en_US"
DISPLAY_ATTRIBUTE_NAMES = ("size", "technique", "material", "year")


class LevanteArtworkDisplayController(http.Controller):
    """Public, read-only museum-label display for an eCommerce product."""

    @http.route(
        [
            '/shop/<model("product.template"):product>/qr',
            '/shop/<model("product.template"):product>/qr/',
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
        readonly=True,
    )
    def artwork_display(self, product, **_kwargs):
        website = request.website

        # Read through sudo only after resolving the requested record, then expose
        # solely the explicitly selected public fields below. This route performs
        # no create/write/unlink operation on products, attributes, or brands.
        product_en = product.sudo().with_context(
            website_id=website.id,
            lang=ENGLISH_LANG_CODE,
        )

        if not self._is_public_artwork(product_en, website):
            raise NotFound()

        brand_en = product_en.product_brand_id.sudo().with_context(
            lang=ENGLISH_LANG_CODE,
        )
        artwork_attributes = self._extract_display_attributes(product_en)

        # Use the exact same website pricing context as the normal product page.
        # request.pricelist reflects the visitor's selected website currency/pricelist,
        # while _get_combination_info also applies the website tax display and fiscal position.
        product_variant = product_en.product_variant_id.sudo().with_context(
            website_id=website.id,
            lang=ENGLISH_LANG_CODE,
        )
        combination_info = product_en._get_combination_info(
            product_id=product_variant.id,
            add_qty=1.0,
        )
        display_price = combination_info["price"]
        display_currency = combination_info["currency"]

        # Match Odoo's native eCommerce sold-out calculation exactly. This returns
        # False for untracked products and products allowed to sell out of stock.
        is_sold = product_variant._is_sold_out()

        product_path = product_en.website_url or (
            f"/shop/{request.env['ir.http']._slug(product_en)}"
        )
        product_url = f"{PUBLIC_BASE_URL.rstrip('/')}/{product_path.lstrip('/')}"

        qr_query = urlencode(
            {
                "barcode_type": "QR",
                "value": product_url,
                "width": 520,
                "height": 520,
                "quiet": 1,
                "barLevel": "H",
            }
        )
        qr_image_url = f"/report/barcode/?{qr_query}"

        response = request.render(
            "levante_artwork_display.artwork_display_page",
            {
                "product": product_en,
                "product_name": product_en.name,
                "artist_name": brand_en.name,
                "artist_description": brand_en.description,
                "artwork_size": artwork_attributes["size"],
                "artwork_technique": artwork_attributes["technique"],
                "artwork_material": artwork_attributes["material"],
                "artwork_year": artwork_attributes["year"],
                "display_price": display_price,
                "display_currency": display_currency,
                "is_sold": is_sold,
                "product_url": product_url,
                "qr_image_url": qr_image_url,
            },
        )
        response.headers["Cache-Control"] = "no-store, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive"
        return response

    @staticmethod
    def _extract_display_attributes(product):
        """Return the four approved attribute values without changing records."""
        values_by_name = {name: False for name in DISPLAY_ATTRIBUTE_NAMES}

        for line in product.attribute_line_ids:
            attribute_name = (line.attribute_id.name or "").strip().casefold()
            if attribute_name not in values_by_name:
                continue

            value_names = [
                value_name
                for value_name in (
                    (value.name or "").strip() for value in line.value_ids
                )
                if value_name
            ]
            if value_names:
                values_by_name[attribute_name] = " / ".join(value_names)

        return values_by_name

    @staticmethod
    def _is_public_artwork(product, website):
        """Allow only active, published, saleable products with an artist."""
        if not product.exists():
            return False
        if not product.active or not product.sale_ok:
            return False
        if not product.is_published or not product.product_brand_id:
            return False

        # Respect the product's website restriction when one is configured.
        product_website = getattr(product, "website_id", False)
        if product_website and product_website != website:
            return False

        # Keep products isolated to the company of the current website.
        if product.company_id and product.company_id != website.company_id:
            return False

        return True
